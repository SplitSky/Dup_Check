#!/bin/bash

# Function to uninstall Python3 (if installed via Homebrew)
uninstall_python3() {
    if brew list python &>/dev/null; then
        echo "Uninstalling Python3..."
        brew uninstall python
    else
        echo "Python3 is not installed via Homebrew."
    fi
}

# Function to uninstall Homebrew
uninstall_homebrew() {
    if command -v brew &>/dev/null; then
        echo "Uninstalling Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
    else
        echo "Homebrew is not installed."
    fi
}

# Main script execution
echo "Starting cleanup..."

remove_repo
uninstall_python3
uninstall_homebrew
remove_xcode_tools

echo "Cleanup complete."
