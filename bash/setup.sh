#!/bin/bash

# Function to check for and install Xcode Command Line Tools
install_xcode_tools() {
    if ! xcode-select --print-path &>/dev/null; then
        echo "Xcode Command Line Tools not found. We need git! Installing..."
        xcode-select --install
        read -p "Press [Enter] once the Xcode Command Line Tools installation is complete."
    else
        echo "Xcode Command Line Tools are already installed."
    fi
}

# Function to check for and install Homebrew
install_homebrew() {
    if ! command -v brew &>/dev/null; then
        echo "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed."
    fi
}

# Function to check for and install Python3
install_python3() {
    if ! command -v python3 &>/dev/null; then
        echo "Python3 not found. Installing..."
        brew install python
    else
        echo "Python3 is already installed."
    fi
}

# Function to clone the GitHub repository
clone_repo() {
    REPO_URL=$1
    if [ -d "./repo" ]; then
        echo "Repository already cloned."
    else
        echo "Cloning repository..."
        git clone "$REPO_URL" repo
    fi
}

# Function to create a virtual environment and install dependencies
setup_virtualenv() {
    cd repo
    if [ ! -d "./venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Function to execute the Python code
run_python_code() {
    echo "Running Python code..."
    python driver.py  # Make sure the script filename is correct
}

# Main script execution
echo "Starting setup..."
echo "This shouldn't take long..."

install_xcode_tools
install_homebrew
echo "You have a package manager now!"
install_python3
echo "You have python now!"

REPO_URL="git@github.com:SplitSky/Dup_Check.git"  # Replace with your GitHub repository URL
clone_repo "$REPO_URL"
echo "You got my code!"
setup_virtualenv
echo "Python environment setup done!"
# run_python_code

echo "Setup complete."
