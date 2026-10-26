PERSONAL COMPUTER CHECKING SYSTEM, WEB DESIGN VERSION

This project adapts the supplied Python PC Checker logic to the dark web interface shown in the reference design.

Requirements:
- Python 3.10 or newer
- Flask

Run on Windows:
1. Extract this folder.
2. Open Command Prompt or the VS Code terminal in this folder.
3. Install Flask:  py -m pip install flask
4. Start the site:  py app.py
5. Open http://127.0.0.1:5000 in your browser.

Included:
- app.py: Flask server and API endpoints
- pc_checker_logic.py: copy of your original Python CLI code, reused for CPU/GPU tier matching and troubleshooting guide
- templates/index.html: the page layout
- static/style.css: dark UI styling
- static/script.js: page navigation, form actions, and saved specs

Notes:
- "Save Specs" currently saves the form values in the browser's local storage, not in MySQL/XAMPP.
- Bottleneck and compatibility checks use the logic from the Python project.
- The PSU estimate is a rough rule from the original code, not a guarantee of power-supply safety.
