"""
Personal Computer Checking System
----------------------------------
A simple CLI tool to:
1. Input/store PC specs
2. Check for possible bottleneck (CPU vs GPU mismatch)
3. Check basic part compatibility
4. Troubleshoot common PC problems
"""

# ---------- Global storage for specs ----------
specs = {
    "cpu": "",
    "cpu_tier": 0,      # 1 = low, 2 = mid, 3 = high, 4 = enthusiast
    "gpu": "",
    "gpu_tier": 0,
    "ram_gb": 0,
    "ram_type": "",     # DDR4 / DDR5
    "storage_gb": 0,
    "motherboard_ram_type": "",  # what RAM type the board supports
    "psu_watt": 0,
    "cpu_socket": "",
    "motherboard_socket": "",
}

# Simple reference tiers (you can expand these lists anytime)
# NOTE: get_tier() checks "low" keywords before "mid" keywords, so any
# specific chip listed under "low" here (even if it also contains a
# generic "mid" keyword like "ryzen 5") will correctly match low first.
CPU_TIERS = {
    "low": [
        # Generic low-end families (Intel)
        "i3", "celeron", "pentium", "atom", "core 2 duo", "core 2 quad",
        "pentium gold", "pentium silver", "celeron g", "celeron n",
        # Generic low-end families (AMD)
        "ryzen 3", "athlon", "athlon 3000g", "athlon 200ge", "athlon 220ge",
        "athlon 240ge", "athlon 3000ge", "athlon gold", "athlon silver",
        "fx", "sempron", "a4-", "a6-", "a8-", "a10-", "a12-",
        # Intel Core i3 - all generations
        "i3-380m", "i3-2100", "i3-2120", "i3-3220", "i3-3240", "i3-4130",
        "i3-4150", "i3-4160", "i3-4170", "i3-6100", "i3-6300", "i3-6320",
        "i3-7100", "i3-7300", "i3-7350k", "i3-8100", "i3-8300", "i3-8350k",
        "i3-9100", "i3-9300", "i3-9350k", "i3-10100", "i3-10105", "i3-10300",
        "i3-10320", "i3-10325", "i3-11100", "i3-12100", "i3-12300",
        "i3-13100", "i3-14100",
        # AMD Ryzen 3 - all generations
        "ryzen 3 1200", "ryzen 3 1300x",
        "ryzen 3 2200g", "ryzen 3 2200u", "ryzen 3 2300u", "ryzen 3 2300x",
        "ryzen 3 3100", "ryzen 3 3200g", "ryzen 3 3200u", "ryzen 3 3250u",
        "ryzen 3 3300u", "ryzen 3 3300x",
        "ryzen 3 4300g", "ryzen 3 4300u",
        "ryzen 3 5300g", "ryzen 3 5300u", "ryzen 3 5400u", "ryzen 3 5425u",
        "ryzen 3 7320u", "ryzen 3 7330u", "ryzen 3 7440u",
        # Older / weaker Intel Core i5 (below roughly a Ryzen 5 5600G)
        "i5-2400", "i5-2500", "i5-2500k", "i5-3330", "i5-3450", "i5-3470",
        "i5-3570", "i5-4430", "i5-4460", "i5-4570", "i5-4590", "i5-4670",
        "i5-6400", "i5-6500", "i5-6600", "i5-7400", "i5-7500", "i5-7600",
        "i5-8250u", "i5-8265u", "i5-8400", "i5-8500", "i5-8600",
        "i5-9400", "i5-9400f", "i5-9500", "i5-9600",
        # Older / weaker AMD Ryzen 5
        "ryzen 5 1400", "ryzen 5 1500x", "ryzen 5 1600", "ryzen 5 1600x",
        "ryzen 5 2400g", "ryzen 5 2500u", "ryzen 5 2600", "ryzen 5 2600x",
        "ryzen 5 3400g", "ryzen 5 3450u", "ryzen 5 3500", "ryzen 5 3500u",
        "ryzen 5 3550h", "ryzen 5 3600", "ryzen 5 3600x",
        "ryzen 5 4500u", "ryzen 5 4600g", "ryzen 5 4600u", "ryzen 5 4600h",
        # Intel N-series / mobile low power
        "n95", "n100", "n200", "n305",
    ],
    "mid": [
        # Generic mid-range families
        "i5", "ryzen 5", "core ultra 5",
        # Intel Core i5 - newer / mainstream desktop & laptop chips
        "i5-9600k", "i5-10400", "i5-10500", "i5-10600", "i5-10600k",
        "i5-11400", "i5-11500", "i5-11600", "i5-11600k",
        "i5-12400", "i5-12500", "i5-12600", "i5-12600k",
        "i5-13400", "i5-13500", "i5-13600", "i5-13600k",
        "i5-14400", "i5-14500", "i5-14600", "i5-14600k",
        # Older Intel i7 that now perform closer to modern i5 (kept mid, not high)
        "i7-2600", "i7-3770", "i7-4770", "i7-6700", "i7-7700",
        # AMD Ryzen 5 - mainstream / newer
        "ryzen 5 5600", "ryzen 5 5600g", "ryzen 5 5600x", "ryzen 5 5600x3d",
        "ryzen 5 5625u",
        "ryzen 5 7600", "ryzen 5 7600x", "ryzen 5 7530u", "ryzen 5 7535u",
        "ryzen 5 7640u", "ryzen 5 7645hx",
        "ryzen 5 8500g", "ryzen 5 8600g",
        "ryzen 5 9600", "ryzen 5 9600x",
    ],
    "high": [
        # Generic high-end families
        "i7", "ryzen 7", "core ultra 7",
        # Intel Core i7 - mainstream & newer
        "i7-8700", "i7-8700k", "i7-9700", "i7-9700k",
        "i7-10700", "i7-10700k", "i7-10750h",
        "i7-11700", "i7-11700k", "i7-11800h",
        "i7-12700", "i7-12700k", "i7-12700h",
        "i7-13700", "i7-13700k", "i7-13700h",
        "i7-14700", "i7-14700k",
        # AMD Ryzen 7 - mainstream & newer
        "ryzen 7 1700", "ryzen 7 1700x", "ryzen 7 1800x",
        "ryzen 7 2700", "ryzen 7 2700x",
        "ryzen 7 3700x", "ryzen 7 3800x", "ryzen 7 3800xt",
        "ryzen 7 4700g", "ryzen 7 4800h", "ryzen 7 4800u",
        "ryzen 7 5700g", "ryzen 7 5700x", "ryzen 7 5700x3d", "ryzen 7 5800x",
        "ryzen 7 5800x3d", "ryzen 7 5800h", "ryzen 7 5825u",
        "ryzen 7 7700", "ryzen 7 7700x", "ryzen 7 7735hs", "ryzen 7 7745hx",
        "ryzen 7 7800x3d", "ryzen 7 7840u", "ryzen 7 7840hs",
        "ryzen 7 8700g",
        "ryzen 7 9700x", "ryzen 7 9800x3d",
    ],
    "enthusiast": [
        # Generic enthusiast / HEDT families
        "i9", "ryzen 9", "threadripper", "xeon w", "core ultra 9",
        # Intel Core i9
        "i9-9900k", "i9-9900ks",
        "i9-10850k", "i9-10900", "i9-10900k", "i9-10980xe",
        "i9-11900", "i9-11900k", "i9-11980hk",
        "i9-12900", "i9-12900k", "i9-12900ks", "i9-12900h",
        "i9-13900", "i9-13900k", "i9-13900ks", "i9-13980hx",
        "i9-14900", "i9-14900k", "i9-14900ks",
        # AMD Ryzen 9
        "ryzen 9 3900x", "ryzen 9 3900xt", "ryzen 9 3950x",
        "ryzen 9 4900h", "ryzen 9 4900hs",
        "ryzen 9 5900x", "ryzen 9 5900xt", "ryzen 9 5950x", "ryzen 9 5980hx",
        "ryzen 9 7900x", "ryzen 9 7900x3d", "ryzen 9 7940hs",
        "ryzen 9 7945hx", "ryzen 9 7950x", "ryzen 9 7950x3d",
        "ryzen 9 8945hs", "ryzen 9 8945hx",
        "ryzen 9 9900x", "ryzen 9 9950x", "ryzen 9 9950x3d",
        # Threadripper / HEDT
        "threadripper 1900x", "threadripper 1920x", "threadripper 1950x",
        "threadripper 2950x", "threadripper 2990wx",
        "threadripper 3960x", "threadripper 3970x", "threadripper 3990x",
        "threadripper 7960x", "threadripper 7970x", "threadripper 7980x",
    ],
}

GPU_TIERS = {
    "low": [
        # Integrated / entry Nvidia
        "gt 1030", "gt 730", "gt 720", "gt 710", "gt 630", "gt 610",
        "mx110", "mx130", "mx150", "mx230", "mx250", "mx330", "mx350", "mx450", "mx550", "mx570",
        "gtx 745", "gtx 750", "gtx 750 ti", "gtx 950", "gtx 960",
        "gtx 1050", "gtx 1050 ti", "gtx 1060 3gb",
        "rtx 3050 laptop", "rtx 2050 laptop",
        # Entry AMD
        "rx 550", "rx 560", "rx 570", "rx 6400", "rx 6500 xt",
        "hd 6450", "hd 7450", "r5 230", "r7 240", "r7 250",
        # Integrated graphics (APU / iGPU)
        "vega 3", "vega 6", "vega 8", "vega 11",
        "radeon graphics",  # generic AMD APU integrated graphics label
        "iris xe", "iris plus", "uhd graphics", "hd graphics",
        # Entry Intel Arc
        "arc a310", "arc a380",
    ],
    "mid": [
        "gtx 1060", "gtx 1070", "gtx 1070 ti", "gtx 1080",
        "gtx 1650", "gtx 1650 super", "gtx 1660", "gtx 1660 super", "gtx 1660 ti",
        "rtx 2060", "rtx 2060 super",
        "rtx 3050", "rtx 3060", "rtx 3060 laptop",
        "rtx 4060", "rtx 4060 laptop", "rtx 4060 ti",
        "rtx 5060",
        "rx 470", "rx 480", "rx 570", "rx 580", "rx 590",
        "rx 5500 xt", "rx 5600 xt", "rx 5700",
        "rx 6600", "rx 6600 xt", "rx 6650 xt",
        "rx 7600", "rx 7600 xt",
        "rx 9060 xt",
        "arc a580", "arc a750", "arc b570",
    ],
    "high": [
        "gtx 1080 ti",
        "rtx 2070", "rtx 2070 super", "rtx 2080", "rtx 2080 super", "rtx 2080 ti",
        "rtx 3060 ti", "rtx 3070", "rtx 3070 ti", "rtx 3070 laptop",
        "rtx 4070", "rtx 4070 laptop", "rtx 4070 ti", "rtx 4070 ti super", "rtx 4070 super",
        "rtx 5070", "rtx 5070 ti",
        "rx 5700 xt",
        "rx 6700 xt", "rx 6750 xt", "rx 6800",
        "rx 7700 xt", "rx 7800 xt",
        "rx 9070", "rx 9070 xt",
        "arc a770", "arc b580",
    ],
    "enthusiast": [
        "rtx 3080", "rtx 3080 ti", "rtx 3080 laptop",
        "rtx 3090", "rtx 3090 ti",
        "rtx 4080", "rtx 4080 super", "rtx 4080 laptop", "rtx 4090", "rtx 4090 laptop",
        "rtx 5080", "rtx 5090",
        "rx 6900 xt", "rx 6950 xt",
        "rx 7900 xt", "rx 7900 xtx",
        "radeon vii",
    ],
}


def get_tier(name, tier_dict):
    """Return tier number (1-4) based on keyword match, else 0 if unknown."""
    name = name.lower()
    order = ["low", "mid", "high", "enthusiast"]
    for i, level in enumerate(order, start=1):
        for keyword in tier_dict[level]:
            if keyword in name:
                return i
    return 0


# ---------- Feature 1: Input Specs ----------
def input_specs():
    print("\n--- Enter Your PC Specs ---")
    specs["cpu"] = input("CPU (e.g. Ryzen 5 5600, i7 12700): ")
    specs["cpu_tier"] = get_tier(specs["cpu"], CPU_TIERS)

    specs["cpu_socket"] = input("CPU Socket (e.g. AM4, LGA1700): ").upper()

    specs["gpu"] = input("GPU (e.g. RTX 3060, RX 6600): ")
    specs["gpu_tier"] = get_tier(specs["gpu"], GPU_TIERS)

    specs["ram_gb"] = int(input("RAM size in GB (e.g. 16): ") or 0)
    specs["ram_type"] = input("RAM type (DDR4/DDR5): ").upper()

    specs["motherboard_socket"] = input("Motherboard Socket (e.g. AM4, LGA1700): ").upper()
    specs["motherboard_ram_type"] = input("Motherboard supported RAM type (DDR4/DDR5): ").upper()

    specs["storage_gb"] = int(input("Storage size in GB (e.g. 512): ") or 0)
    specs["psu_watt"] = int(input("PSU wattage (e.g. 550): ") or 0)

    print("\nSpecs saved successfully!\n")


# ---------- Feature 2: Bottleneck Check ----------
def check_bottleneck():
    if specs["cpu_tier"] == 0 or specs["gpu_tier"] == 0:
        print("\nCan't check bottleneck: CPU or GPU not recognized. "
              "Try entering more common model names.")
        return

    diff = specs["cpu_tier"] - specs["gpu_tier"]

    print("\n--- Bottleneck Check ---")
    if diff == 0:
        print("Good match! CPU and GPU are in the same performance tier.")
    elif diff == 1 or diff == -1:
        print("Minor imbalance, but generally fine for most use cases.")
    elif diff >= 2:
        print("Possible GPU bottleneck: your CPU is much stronger than your GPU.")
        print("-> The GPU may hold back overall performance.")
    elif diff <= -2:
        print("Possible CPU bottleneck: your GPU is much stronger than your CPU.")
        print("-> The CPU may hold back overall performance, especially in games.")


# ---------- Feature 3: Compatibility Check ----------
def check_compatibility():
    print("\n--- Compatibility Check ---")
    issues = []

    # Socket check
    if specs["cpu_socket"] and specs["motherboard_socket"]:
        if specs["cpu_socket"] != specs["motherboard_socket"]:
            issues.append(
                f"CPU socket ({specs['cpu_socket']}) does not match "
                f"motherboard socket ({specs['motherboard_socket']})."
            )

    # RAM type check
    if specs["ram_type"] and specs["motherboard_ram_type"]:
        if specs["ram_type"] != specs["motherboard_ram_type"]:
            issues.append(
                f"RAM type ({specs['ram_type']}) is not supported by "
                f"motherboard (supports {specs['motherboard_ram_type']})."
            )

    # PSU wattage rough estimate
    estimated_watt_needed = 300  # base system
    if specs["gpu_tier"] == 2:
        estimated_watt_needed += 150
    elif specs["gpu_tier"] == 3:
        estimated_watt_needed += 250
    elif specs["gpu_tier"] == 4:
        estimated_watt_needed += 350

    if specs["psu_watt"] and specs["psu_watt"] < estimated_watt_needed:
        issues.append(
            f"PSU might be underpowered. Estimated need: ~{estimated_watt_needed}W, "
            f"you have {specs['psu_watt']}W."
        )

    if issues:
        print("Found possible issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No obvious compatibility issues found!")


# ---------- Feature 4: Troubleshooting ----------
TROUBLESHOOT_GUIDE = {
    "1": ("PC won't turn on",
          ["Check if the power cable is properly plugged in.",
           "Check the PSU switch is set to ON (I, not O).",
           "Try a different power outlet.",
           "Reseat the RAM and check for beep codes."]),
    "2": ("No display / black screen",
          ["Make sure monitor cable is connected to the GPU, not motherboard (if you have a GPU).",
           "Reseat the GPU and RAM.",
           "Try a different monitor cable/port.",
           "Check if the GPU needs extra power connectors."]),
    "3": ("PC randomly restarts or shuts down",
          ["Check CPU/GPU temperatures for overheating.",
           "Check if PSU wattage is enough for your components.",
           "Update or reinstall GPU drivers.",
           "Test RAM using memtest86."]),
    "4": ("Slow performance / lag",
          ["Check for background apps eating CPU/RAM (Task Manager).",
           "Check storage: is it near full or still using HDD instead of SSD?",
           "Check for overheating causing thermal throttling.",
           "Update drivers and OS."]),
    "5": ("Blue screen (BSOD)",
          ["Note the error code shown on the blue screen.",
           "Update or roll back recent driver updates.",
           "Run memory diagnostic (memtest86) to check RAM.",
           "Check for recently installed hardware/software conflicts."]),
}


def troubleshoot():
    print("\n--- Troubleshooting Menu ---")
    for key, (problem, _) in TROUBLESHOOT_GUIDE.items():
        print(f"{key}. {problem}")
    choice = input("Select a problem number: ")

    if choice in TROUBLESHOOT_GUIDE:
        problem, steps = TROUBLESHOOT_GUIDE[choice]
        print(f"\nSuggested steps for: {problem}")
        for i, step in enumerate(steps, start=1):
            print(f"{i}. {step}")
    else:
        print("Invalid choice.")


# ---------- Main Menu ----------
def main():
    while True:
        print("\n===== Personal Computer Checking System =====")
        print("1. Input Specs")
        print("2. Check Bottleneck")
        print("3. Check Compatibility")
        print("4. Troubleshoot")

        choice = input("Choose an option: ")

        if choice == "1":
            input_specs()
        elif choice == "2":
            check_bottleneck()
        elif choice == "3":
            check_compatibility()
        elif choice == "4":
            troubleshoot()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()