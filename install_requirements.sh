#!/bin/bash

# This script installs required dependencies for the project.

# How to run this script:
## chmod +x install_requirements.sh
## ./install_requirements.sh

echo "Starting installation of required dependencies..."

# Step 1: Ensure Git submodules are initialized and updated
echo "Initializing and updating Git submodules..."
git pull
git submodule init
git submodule update
echo "Git submodules are up-to-date."

# Detect OS
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
   OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
   OS="MacOS"
elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
   OS="Windows"
else
   echo "Unsupported OS."
   exit 1
fi

echo "Detected OS: $OS"

# Install Python and Pip
install_python_pip() {
   echo "Installing Python and Pip..."
   case "$OS" in
      Linux)
         sudo apt update
         sudo apt install python3 python3-pip -y
         ;;
      MacOS)
         brew install python3
         ;;
      Windows)
         echo "Please install Python manually from https://www.python.org/downloads/ or use Chocolatey:"
         echo "choco install python3"
         ;;
   esac
   echo "Python and Pip installation complete."
}

# Install Git
install_git() {
   echo "Installing Git..."
   case "$OS" in
      Linux)
         sudo apt update
         sudo apt install git -y
         ;;
      MacOS)
         brew install git
         ;;
      Windows)
         echo "Please install Git manually from https://git-scm.com/downloads."
         ;;
   esac
   echo "Git installation complete."
}

# Install Make
install_make() {
   echo "Installing Make..."
   case "$OS" in
      Linux)
         sudo apt update
         sudo apt install make -y
         ;;
      MacOS)
         brew install make
         ;;
      Windows)
         echo "Please install Make as part of a Unix-like environment (e.g., Cygwin or WSL) or download from https://www.gnu.org/software/make/#download."
         ;;
   esac
   echo "Make installation complete."
}

# Install Maven
install_maven() {
   echo "Installing Apache Maven..."
   case "$OS" in
      Linux)
         sudo apt update
         sudo apt install maven -y
         ;;
      MacOS)
         brew install maven
         ;;
      Windows)
         echo "Please install Maven manually from https://maven.apache.org/download.cgi or use Chocolatey:"
         echo "choco install maven"
         ;;
   esac
   echo "Maven installation complete."
}

# Set up .env file
setuo_env_file() {
   if [[ -f ".env-example" ]]; then
      echo "Copying .env-example to .env..."
      cp .env-example .env
      echo ".env file created. Please fill in your API keys and tokens."
   else
      echo ".env-example file not found. Creating .env file manually..."
      touch .env-example
      echo "GEMINI_API_KEY=" > .env-example
      echo 'GITHUB_TOKEN=""' >> .env-example
      setuo_env_file
   fi
   echo "Read the .env file section in the README.md for more information on how to fill in the required API keys and Tokens."
}

# Run installation functions
install_python_pip
install_git
install_make
install_maven
setuo_env_file

echo "All required dependencies have been installed (or instructions provided)."
