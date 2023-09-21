import os # This module provides a portable way of using operating system dependent functionality.
from colorama import Style # Colorama is a Python library for printing colored text and stylizing terminal output.

# Macros:
class backgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red

# @brief: This function counts the empty folders in a directory
# @param: directory - The directory to count the empty folders
# @return: empty_folders - The list of empty folders
def count_empty_folders(directory):
	empty_folders = [] # The list of empty folders

	# Loop through the directory
	for root, dirs, files in os.walk(directory):
		for dir in dirs: # Loop through the directories
			folder_path = os.path.join(root, dir) # Get the path of the directory
			if not os.listdir(folder_path): # If the directory is empty
				empty_folders.append(folder_path) # Add the directory to the list of empty folders

	# Return the list of empty folders
	return empty_folders

# @brief: The main function
# @param: None
# @return: None
def main():
	print(f"{backgroundColors.GREEN}Current working directory: {backgroundColors.CYAN}{os.getcwd()}{Style.RESET_ALL}")
	initial_directory = input(f"{backgroundColors.GREEN}Enter the initial directory {backgroundColors.CYAN}(Relative/Absolute Paths): {Style.RESET_ALL}")
	
	if not os.path.isdir(initial_directory):
		print(f"{backgroundColors.RED}Invalid directory path.{Style.RESET_ALL}")
	else:
		empty_folders = count_empty_folders(initial_directory)
		if empty_folders:
			print(f"{backgroundColors.GREEN}Empty folders found:{Style.RESET_ALL}")
			for folder in empty_folders:
				print(f"{backgroundColors.CYAN}{folder}{Style.RESET_ALL}")
			print(f"{backgroundColors.GREEN}Total empty folders found: {backgroundColors.CYAN}{len(empty_folders)}{Style.RESET_ALL}")
		else:
			print(f"{backgroundColors.CYAN}No empty folders found.{Style.RESET_ALL}")

if __name__ == "__main__":
	main()