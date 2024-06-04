import atexit # For playing a sound when the program finishes
import google.generativeai as genai # Import the Google AI Python SDK
import os # For running a command in the terminal
import pandas as pd # For handling CSV files
import platform # For getting the operating system name
import sys # For exiting the program
from colorama import Style # For coloring the terminal
from dotenv import load_dotenv # For loading .env files

# Macros:
class BackgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red  
	BOLD = "\033[1m" # Bold
	UNDERLINE = "\033[4m" # Underline
	CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Sound Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The commands to play a sound for each operating system
SOUND_FILE = "../.assets/Sounds/NotificationSound.wav" # The path to the sound file

# .Env Constants:
ENV_PATH = "../.env" # The path to the .env file
ENV_VARIABLE = "GEMINI_API_KEY" # The environment variable to load

# File Path Constants:
JSON_INPUT_FILE = "../PyDriller/metrics_statistics/zookeeper/substantial_CBO_classes_changes.csv" # The path to the input JSON file
OUTPUT_FILE = "./output.txt" # The path to the output file

# Header Constants:
DESIRED_HEADER = ["Class", "Method Invocations"] # The desired header of the CSV file

def play_sound():
	"""
	Plays a sound when the program finishes.
	:return: None
	"""
	if os.path.exists(SOUND_FILE):
		if platform.system() in SOUND_COMMANDS: # If the platform.system() is in the SOUND_COMMANDS dictionary
			os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
		else: # If the platform.system() is not in the SOUND_COMMANDS dictionary
			print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
	else: # If the sound file does not exist
		print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

def verify_env_file(env_path=ENV_PATH, key=ENV_VARIABLE):
	"""
	Verify if the .env file exists and if the desired key is present.
	:param env_path: Path to the .env file.
	:param key: The key to get in the .env file.
	:return: The value of the key if it exists.
	"""

	# Verify if the .env file exists
	if not os.path.exists(env_path):
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}.env file{BackgroundColors.RED} not found at {BackgroundColors.CYAN}{env_path}{Style.RESET_ALL}")
		sys.exit(1) # Exit the program

	load_dotenv(env_path) # Load the .env file
	api_key = os.getenv(key) # Get the value of the key

	# Verify if the key exists
	if not api_key:
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{key}{BackgroundColors.RED} key was not found in the .env file located at {BackgroundColors.CYAN}{env_path}{Style.RESET_ALL}")
		sys.exit(1) # Exit the program

	return api_key # Return the value of the key

def main():
	"""
	Main function.
	:return: None
	"""

	print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Google Gemini API Integration{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the Welcome message


	print(f"{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
	"""
	This is the standard boilerplate that calls the main() function.
	:return: None
	"""

	main() # Call the main function
