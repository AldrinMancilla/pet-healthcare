from flask import Flask, render_template, request, jsonify
from pc_checker_logic import get_tier, CPU_TIERS, GPU_TIERS, TROUBLESHOOT_GUIDE

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/bottleneck")
def bottleneck():
    data = request.get_json(force=True)
    cpu = str(data.get("cpu", "")).strip()
    gpu = str(data.get("gpu", "")).strip()
    ct = get_tier(cpu, CPU_TIERS) if cpu else 0
    gt = get_tier(gpu, GPU_TIERS) if gpu else 0
    if not ct or not gt:
        return jsonify(ok=False, result="CPU or GPU not recognized. Try entering a more common model name.")
    diff = ct - gt
    if diff == 0:
        result = "Good match! CPU and GPU are in the same performance tier."
    elif abs(diff) == 1:
        result = "Minor imbalance, but generally fine for most use cases."
    elif diff >= 2:
        result = "Possible GPU bottleneck: your CPU is much stronger than your GPU. The GPU may hold back overall performance."
    else:
        result = "Possible CPU bottleneck: your GPU is much stronger than your CPU. The CPU may hold back overall performance, especially in games."
    return jsonify(ok=True, result=result, cpu_tier=ct, gpu_tier=gt)

@app.post("/api/compatibility")
def compatibility():
    d = request.get_json(force=True)
    issues = []
    cpu_socket = str(d.get("cpu_socket", "")).strip().upper()
    board_socket = str(d.get("motherboard_socket", "")).strip().upper()
    ram_type = str(d.get("ram_type", "")).strip().upper()
    board_ram = str(d.get("motherboard_ram_type", "")).strip().upper()
    psu = int(d.get("psu_watt") or 0)
    gpu = str(d.get("gpu", "")).strip()
    gt = get_tier(gpu, GPU_TIERS) if gpu else 0
    if cpu_socket and board_socket and cpu_socket != board_socket:
        issues.append(f"CPU socket ({cpu_socket}) does not match motherboard socket ({board_socket}).")
    if ram_type and board_ram and ram_type != board_ram:
        issues.append(f"RAM type ({ram_type}) is not supported by motherboard (supports {board_ram}).")
    needed = 300
    if gt == 2: needed += 150
    elif gt == 3: needed += 250
    elif gt == 4: needed += 350
    if psu and psu < needed:
        issues.append(f"PSU might be underpowered. Estimated need: about {needed}W, you have {psu}W.")
    if not issues:
        result = "No obvious compatibility issues found!"
    else:
        result = "Possible issues found:\n" + "\n".join("• " + x for x in issues)
    return jsonify(ok=True, result=result, issues=issues, estimated_watt_needed=needed)

@app.get("/api/troubleshoot/<choice>")
def troubleshoot(choice):
    if choice not in TROUBLESHOOT_GUIDE:
        return jsonify(ok=False, result="Invalid choice.")
    problem, steps = TROUBLESHOOT_GUIDE[choice]
    return jsonify(ok=True, problem=problem, steps=steps)

if __name__ == "__main__":
    app.run(debug=True)
