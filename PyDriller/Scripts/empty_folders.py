import os # This module provides a portable way of using operating system dependent functionality.
from colorama import Style # Colorama is a Python library for printing colored text and stylizing terminal output.

# Macros:
class BackgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red
	BOLD = "\033[1m" # Bold
	UNDERLINE = "\033[4m" # Underline
	CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Default values that can be changed:
DATA_FOLDERS = ["ck_metrics", "diffs", "metrics_evolution", "metrics_predictions", "metrics_statistics"] # The Data Folders
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function.

def search_empty_folders(directory):
	"""
	Search for empty folders in the given directory.

	:param directory: The directory to search in
	:return: empty_folders: The list of empty folders
	
	"""

	if VERBOSE: # If the VERBOSE constant is set to True
		print(f"{BackgroundColors.GREEN}Searching for empty folders in {BackgroundColors.CYAN}{directory}{Style.RESET_ALL}")

	empty_folders = [] # The list of empty folders

	# Loop through the directory
	for root, dirs, files in os.walk(directory):
		for dir in dirs: # Loop through the directories
			folder_path = os.path.join(root, dir) # Get the path of the directory
			if ".git" in folder_path: # If the substring ".git" is in the path, skip it
				continue
			if not os.listdir(folder_path): # If the directory is empty
				empty_folders.append(folder_path) # Add the directory to the list of empty folders

	# Return the list of empty folders
	return empty_folders

def main():
	"""
   Main function.

   :return: None
   """

	# Print the welcome message
	print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Empty Folders Finder{BackgroundColors.GREEN}! This script is part of the {BackgroundColors.CYAN}Worked Example Miner (WEM){BackgroundColors.GREEN} project.{Style.RESET_ALL}", end="\n\n")
	
	print(f"{BackgroundColors.GREEN}Current working directory: {BackgroundColors.CYAN}{os.getcwd()}{Style.RESET_ALL}")
	initial_directory = input(f"{BackgroundColors.GREEN}Enter the initial directory {BackgroundColors.CYAN}(default, relative/absolute paths): {Style.RESET_ALL}")
	print(f"")

	# If the initial directory is "default", set it to the data folders
	if initial_directory.lower() == "default":
		initial_directory = DATA_FOLDERS # Set the initial directory to the data folders

	# Loop through the directories in the initial directory	
	for directory in initial_directory:
		if not os.path.isdir(directory): # If the directory does not exist
			print(f"{BackgroundColors.RED}Invalid directory path: {BackgroundColors.CYAN}{directory}{Style.RESET_ALL}")
			continue # Skip the directory

		empty_folders = search_empty_folders(directory) # Search for empty folders in the directory

		if empty_folders: # If empty folders are found
			print(f"{BackgroundColors.GREEN}Empty folders found in {BackgroundColors.CYAN}{directory}{BackgroundColors.GREEN}:{Style.RESET_ALL}")
			for folder in empty_folders: # Loop through the empty folders and print them
				print(f"{BackgroundColors.CYAN}{folder}{Style.RESET_ALL}")
			print(f"{BackgroundColors.GREEN}Total empty folders found in {BackgroundColors.CYAN}{directory}{BackgroundColors.GREEN}: {BackgroundColors.CYAN}{len(empty_folders)}{Style.RESET_ALL}")
			print(f"")
		else: # If no empty folders are found
			print(f"{BackgroundColors.GREEN}No empty folders found in {BackgroundColors.CYAN}{directory}{BackgroundColors.GREEN}.{Style.RESET_ALL}")

	# Print the end message
	print(f"\n\n{BackgroundColors.GREEN}The {BackgroundColors.CYAN}Empty Folders Finder{BackgroundColors.GREEN} has finished running. Thank you for using it!{Style.RESET_ALL}")

if __name__ == '__main__':
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
