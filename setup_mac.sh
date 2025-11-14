#!/bin/bash

echo "========================================"
echo "FullControl Workshop Setup - macOS/Linux"
echo "========================================"
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MINICONDA_DIR="$SCRIPT_DIR/Miniconda3"

# Detect architecture
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]] || [[ "$ARCH" == "aarch64" ]]; then
    INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
    echo "Detected: Apple Silicon (ARM64)"
elif [[ "$(uname)" == "Darwin" ]]; then
    INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    echo "Detected: Intel Mac"
else
    INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo "Detected: Linux x86_64"
fi

INSTALLER="$SCRIPT_DIR/miniconda_installer.sh"

# Check if Miniconda is already installed in the workshop folder
if [ -f "$MINICONDA_DIR/bin/conda" ]; then
    echo "[OK] Miniconda already installed locally"
else
    echo "[1/3] Downloading Miniconda installer..."
    echo "This may take a few minutes..."
    curl -L "$INSTALLER_URL" -o "$INSTALLER"
    
    if [ ! -f "$INSTALLER" ]; then
        echo "[ERROR] Failed to download Miniconda installer"
        echo "Please check your internet connection and try again"
        exit 1
    fi
    
    echo "[OK] Download complete"
    echo
    
    echo "[2/3] Installing Miniconda locally (this takes a few minutes)..."
    echo "Installing to: $MINICONDA_DIR"
    bash "$INSTALLER" -b -p "$MINICONDA_DIR"
    
    if [ ! -f "$MINICONDA_DIR/bin/conda" ]; then
        echo "[ERROR] Miniconda installation failed"
        exit 1
    fi
    
    echo "[OK] Miniconda installed"
    rm "$INSTALLER"
    echo
fi

echo "[3/3] Creating fullcontrol_env environment..."

# Check if environment already exists
source "$MINICONDA_DIR/bin/activate" fullcontrol_env 2>/dev/null
if [ $? -eq 0 ]; then
    echo "[OK] Environment 'fullcontrol_env' already exists"
else
    # Create the environment
    source "$MINICONDA_DIR/bin/activate"
    conda env create -f "$SCRIPT_DIR/environment.yml"
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create environment"
        echo "Please check environment.yml and try again"
        exit 1
    fi
    
    echo "[OK] Environment created successfully"
fi

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "You can now run the workshop with: ./run_mac.sh"
echo
