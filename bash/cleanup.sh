#!/bin/bash

# Function to remove the cloned GitHub repository
remove_repo() {
    if [ -d "./repo" ]; then
        echo "Removing cloned repository..."
        rm -rf ./repo
    else
        echo "No repository found to remove."
    fi
}

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

# Function to remove Xcode Command Line Tools (if installed)
remove_xcode_tools() {
    if xcode-select --print-path &>/dev/null; then
        echo "Removing Xcode Command Line Tools..."
        sudo rm -rf /Library/Developer/CommandLineTools
        sudo xcode-select --reset
    else
        echo "Xcode Command Line Tools are not installed."
    fi
}

# Main script execution
echo "Starting cleanup..."

remove_repo
uninstall_python3
uninstall_homebrew
remove_xcode_tools

echo "Cleanup complete."
