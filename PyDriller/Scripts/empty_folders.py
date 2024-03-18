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

DATA_FOLDERS = ["ck_metrics", "diffs", "metrics_evolution", "metrics_predictions", "metrics_statistics"] # The Data Folders

def search_empty_folders(directory):
	"""
	Search for empty folders in the given directory.

	:param directory: The directory to search in
	:return: empty_folders: The list of empty folders
	
	"""

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
	print(f"{BackgroundColors.GREEN}Current working directory: {BackgroundColors.CYAN}{os.getcwd()}{Style.RESET_ALL}")
	initial_directory = input(f"{BackgroundColors.GREEN}Enter the initial directory {BackgroundColors.CYAN}(default, relative/absolute paths): {Style.RESET_ALL}")
	print(f"")

	if initial_directory.lower() == "default":
		initial_directory = DATA_FOLDERS
	
	for directory in initial_directory:
		if not os.path.isdir(directory):
			print(f"{BackgroundColors.RED}Invalid directory path: {BackgroundColors.CYAN}{directory}{Style.RESET_ALL}")
			continue

		empty_folders = search_empty_folders(directory)
		if empty_folders:
			print(f"{BackgroundColors.GREEN}Empty folders found in {BackgroundColors.CYAN}{directory}{BackgroundColors.GREEN}:{Style.RESET_ALL}")
			for folder in empty_folders:
				print(f"{BackgroundColors.CYAN}{folder}{Style.RESET_ALL}")
			print(f"{BackgroundColors.GREEN}Total empty folders found in {BackgroundColors.CYAN}{directory}{BackgroundColors.GREEN}: {BackgroundColors.CYAN}{len(empty_folders)}{Style.RESET_ALL}")
			print(f"")
		else:
			print(f"{BackgroundColors.GREEN}No empty folders found in {BackgroundColors.CYAN}{directory}{BackgroundColors.GREEN}.{Style.RESET_ALL}")

if __name__ == '__main__':
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
