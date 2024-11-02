#!/bin/bash

# This script installs required dependencies for the project.

# How to run this script:
## chmod +x install_requirements.sh
## ./install_requirements.sh

echo "Welcome to the installation script for the project."
echo "This script will install the required dependencies for the project, including Python, Pip, Git, Make, and Maven."
echo "Please ensure you have the necessary permissions to install software on your system."

# Ensure the Project is up-to-date
echo "Pulling the latest changes from the repository..."
git pull
echo "The project is up-to-date."

# Ensure Git submodules are initialized and updated
echo "Initializing and updating Git submodules..."
git submodule init
git submodule update
echo "Git submodules are up-to-date."

# Detect OS
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
   OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
   OS="MacOS"
elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]] || [[ "$OSTYPE" == "win32" ]]; then
   OS="Windows"
else
   echo "Unsupported OS."
   exit 1
fi

echo "Detected OS: $OS"

# Function to check if a command exists
command_exists() {
   command -v "$1" &> /dev/null
}

# Install Python and Pip
install_python_pip() {
   if command_exists python3 && command_exists pip3; then
      echo "Python and Pip are already installed."
   else
      echo "Installing Python and Pip..."
      case "$OS" in
         Linux)
            sudo apt update
            sudo apt install python3 python3-pip python3-venv -y
            ;;
         MacOS)
            # Install Python 3 using Homebrew
            brew install python
            # Ensure pip and venv are also installed with Python
            python3 -m ensurepip --upgrade
            python3 -m pip install --upgrade pip
            python3 -m pip install virtualenv
            ;;
         Windows)
            # Check if Python is installed using Chocolatey
            if ! command_exists python; then
               echo "Installing Python using Chocolatey..."
               echo "This requires Chocolatey to be installed."
               choco install python --params "/InstallDir:C:\Python39" -y
            fi
            # Ensure pip is installed
            if ! command_exists pip; then
               echo "Installing pip..."
               curl -sS https://bootstrap.pypa.io/get-pip.py | python
            fi
            # Install virtualenv
            pip install --user virtualenv
            ;;
      esac
      echo "Python and Pip installation complete."
   fi
}

# Install C/C++ Compiler
install_c_cpp_compiler() {
   if command_exists gcc && command_exists g++; then
      echo "C/C++ are already installed."
   else
      echo "Installing C/C++ Compiler..."
      case "$OS" in
         Linux)
            sudo apt install build-essential -y
            ;;
         MacOS)
            echo "Build tools are included with Xcode Command Line Tools. Installing..."
            xcode-select --install
            ;;
         Windows)
            echo "Please install build tools manually using MinGW from https://sourceforge.net/projects/mingw/." 
            ;;
      esac
      echo "C/C++ Compiler installation complete."
   fi
}

# Function to check if Java is installed and install it if not
install_java() {
   if ! command -v java &> /dev/null; then
      echo "Java is not installed. Installing Java..."
      case "$OS" in
         Linux)
            sudo apt install -y default-jdk
            ;;
         MacOS)
            brew install openjdk
            ;;
         Windows)
            echo "Please install Java manually on Windows from https://www.java.com/"
            exit 1
            ;;
      esac
      echo "Java installation complete."
   else
      echo "Java is already installed."
   fi
}

# Function to set JAVA_HOME if not already set
setup_java_home() {
   if [[ -z "$JAVA_HOME" ]]; then
      echo "JAVA_HOME is not set. Attempting to configure it automatically..."
      JAVA_VERSION=$(java -version 2>&1 | awk -F[\"._] '/version/ {print $2}')
      
      case "$OS" in
         Linux)
            JAVA_HOME_CANDIDATE=$(ls /usr/lib/jvm | grep -E "java-?$JAVA_VERSION" | head -n 1)
            if [[ -n "$JAVA_HOME_CANDIDATE" ]]; then
               export JAVA_HOME="/usr/lib/jvm/$JAVA_HOME_CANDIDATE"
               echo "JAVA_HOME set to $JAVA_HOME"

               # Add JAVA_HOME to .bashrc or .zshrc
               SHELL_CONFIG="$HOME/.bashrc"
               if [[ $SHELL == *"zsh"* ]]; then
                  SHELL_CONFIG="$HOME/.zshrc"
               fi

               # Check if JAVA_HOME is already in the config file
               if ! grep -q "export JAVA_HOME=" "$SHELL_CONFIG"; then
                  echo "export JAVA_HOME=\"$JAVA_HOME\"" >> "$SHELL_CONFIG"
                  echo "Added JAVA_HOME to $SHELL_CONFIG."
               else
                  echo "JAVA_HOME is already set in $SHELL_CONFIG."
               fi

               # Source the config file
               source "$SHELL_CONFIG"
               echo "Sourced $SHELL_CONFIG to apply changes."
            else
               echo "No matching Java installation found in /usr/lib/jvm for Java version $JAVA_VERSION."
               echo "Please set JAVA_HOME manually."
            fi
            ;;
         MacOS)
            JAVA_HOME=$(/usr/libexec/java_home -v "$JAVA_VERSION" 2>/dev/null)
            if [[ -n "$JAVA_HOME" ]]; then
               export JAVA_HOME
               echo "JAVA_HOME set to $JAVA_HOME"

               # Add JAVA_HOME to .bashrc or .zshrc
               SHELL_CONFIG="$HOME/.bashrc"
               if [[ $SHELL == *"zsh"* ]]; then
                  SHELL_CONFIG="$HOME/.zshrc"
               fi

               # Check if JAVA_HOME is already in the config file
               if ! grep -q "export JAVA_HOME=" "$SHELL_CONFIG"; then
                  echo "export JAVA_HOME=\"$JAVA_HOME\"" >> "$SHELL_CONFIG"
                  echo "Added JAVA_HOME to $SHELL_CONFIG."
               else
                  echo "JAVA_HOME is already set in $SHELL_CONFIG."
               fi

               # Source the config file
               source "$SHELL_CONFIG"
               echo "Sourced $SHELL_CONFIG to apply changes."
            else
               echo "No matching Java installation found. Please set JAVA_HOME manually."
            fi
            ;;
         Windows)
            JAVA_PATHS=("C:\\Program Files\\Java" "C:\\Program Files (x86)\\Java")
            for path in "${JAVA_PATHS[@]}"; do
               JAVA_HOME_CANDIDATE=$(ls "$path" | grep -E "jdk-$JAVA_VERSION" | head -n 1)
               if [[ -n "$JAVA_HOME_CANDIDATE" ]]; then
                  export JAVA_HOME="$path\\$JAVA_HOME_CANDIDATE"
                  echo "JAVA_HOME set to $JAVA_HOME"
                  echo "To make this change permanent, add the following line to your environment variables:"
                  echo "JAVA_HOME=$JAVA_HOME"
                  break
               fi
            done
            if [[ -z "$JAVA_HOME" ]]; then
               echo "No matching Java installation found in standard paths on Windows."
               echo "Please set JAVA_HOME manually."
            fi
            ;;
      esac
   else
      echo "JAVA_HOME is already set to $JAVA_HOME."
   fi
}

# Install Git
install_git() {
   if command_exists git; then
      echo "Git is already installed."
   else
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
   fi
}

# Install Make
install_make() {
   if command_exists make; then
      echo "Make is already installed."
   else
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
   fi
}

# Install Maven
install_maven() {
   if command_exists mvn; then
      echo "Maven is already installed."
   else
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
   fi
}

# Set up .env file
setup_env_file() {
   if [[ -f ".env" ]]; then
      echo ".env file already exists. Please edit it to fill in your API keys and tokens."
   else
      if [[ -f ".env-example" ]]; then
         echo "Copying .env-example to .env..."
         cp .env-example .env
         echo ".env file created. Please fill in your API keys and tokens."
      else
         echo ".env-example file not found. Creating .env file manually..."
         touch .env-example
         echo "GEMINI_API_KEY=" > .env-example
         echo 'GITHUB_TOKEN=""' >> .env-example
         cp .env-example .env
      fi
      echo ".env file setup complete."
   fi
   echo "Read the .env file section in the README.md for more information on how to fill in the required API keys and Tokens."
}

# Run installation functions
install_python_pip
install_c_cpp_compiler
install_java
setup_java_home
install_git
install_make
install_maven
setup_env_file

echo "Please, check for any errors in the installation process in the log messages above."
echo "All required dependencies should now be installed."
