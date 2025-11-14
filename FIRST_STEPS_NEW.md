# FullControl Workshop - First Steps

Welcome! This workshop includes everything you need to start creating G-code with FullControl and Marimo. No prior Python installation or experience required.

---

## Quick Start

### Windows

1. **First time setup:** Double-click `setup_windows.bat`
   - Downloads and installs Miniconda locally in this folder
   - Creates the workshop environment with all dependencies
   - Takes 5-10 minutes (one time only)

2. **Run the workshop:** Double-click `run_windows.bat`
   - Launches the Marimo interactive editor
   - Opens in your default browser

### macOS / Linux

1. **First time setup:** Open Terminal in this folder and run:
   ```bash
   chmod +x setup_mac.sh run_mac.sh
   ./setup_mac.sh
   ```
   - Downloads and installs Miniconda locally in this folder
   - Creates the workshop environment with all dependencies
   - Takes 5-10 minutes (one time only)

2. **Run the workshop:**
   ```bash
   ./run_mac.sh
   ```
   - Launches the Marimo interactive editor
   - Opens in your default browser

---

## What Gets Installed

Everything is installed **locally in this workshop folder** - no system-wide changes:

```
fullcontrol-workshop/
│
├─ Miniconda3/           # Local Python installation (created by setup)
├─ environment.yml       # Defines Python packages to install
├─ app.py                # Your workshop notebook
│
├─ setup_windows.bat     # One-time setup (Windows)
├─ setup_mac.sh          # One-time setup (macOS/Linux)
├─ run_windows.bat       # Launch workshop (Windows)
└─ run_mac.sh            # Launch workshop (macOS/Linux)
```

**Installed packages:**
- Python 3.12
- Marimo (interactive notebook environment)
- FullControl (G-code generation library)

---

## Using Marimo

Once the workshop launches in your browser:

- **Edit code cells** - Changes update automatically
- **Run cells** - Click play button or press Shift+Enter
- **Experiment** - Try modifying the FullControl examples
- **Auto-save** - Your changes are saved automatically

---

## Troubleshooting

### Setup script fails or hangs

- **Check internet connection** - Setup downloads ~500MB
- **Disable antivirus temporarily** - May block the installer
- **Run as administrator** (Windows) - Right-click → "Run as administrator"
- **Check disk space** - Need at least 2GB free

### "Permission denied" on macOS/Linux

Make the scripts executable:
```bash
chmod +x setup_mac.sh run_mac.sh
```

### Workshop won't start after setup

The setup script will tell you if something went wrong. If needed, delete the `Miniconda3` folder and run setup again:

**Windows:**
```powershell
Remove-Item -Recurse -Force .\Miniconda3
.\setup_windows.bat
```

**macOS/Linux:**
```bash
rm -rf ./Miniconda3
./setup_mac.sh
```

### Browser doesn't open automatically

Look for a URL in the terminal (usually `http://localhost:2718`) and open it manually.

### Need to update packages

```bash
# Windows - run from the workshop folder
.\Miniconda3\Scripts\activate.bat fullcontrol_env
pip install --upgrade marimo
pip install --upgrade git+https://github.com/FullControlXYZ/fullcontrol

# macOS/Linux - run from the workshop folder
source ./Miniconda3/bin/activate fullcontrol_env
pip install --upgrade marimo
pip install --upgrade git+https://github.com/FullControlXYZ/fullcontrol
```

---

## Why This Approach?

**Isolated Environment:** Everything installs locally in the workshop folder, avoiding conflicts with existing Python installations or system packages.

**No Admin Rights:** Setup doesn't require administrator permissions (though it may help on some Windows systems).

**Reproducible:** Everyone gets the same Python version and package versions, regardless of their system setup.

**Clean Removal:** Just delete the `Miniconda3` folder to completely remove the installation.

---

## Tips

✅ **Run setup once** - Only needed the first time  
✅ **Keep files together** - Don't move files outside this folder  
✅ **Save your work** - Marimo auto-saves to `app.py`  
✅ **Experiment freely** - You can always re-run setup if something breaks  

---

## Learn More

- **FullControl Documentation:** https://github.com/FullControlXYZ/fullcontrol
- **Marimo Documentation:** https://docs.marimo.io
- **Miniconda Documentation:** https://docs.anaconda.com/miniconda
