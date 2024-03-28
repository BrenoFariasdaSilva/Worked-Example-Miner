import os # OS module provides functions for interacting with the operating system
import re # Regular expression operations module
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
REPOSITORIES = ["zookeeper"] # The list of repositories
TARGET_FILENAMES = {"zookeeper": "CHANGES.txt.diff"} # The target file names
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function.

def search_files(search_directory, search_string):
	"""
	Search for files in the given directory.

	:param search_directory: The directory to search in
	:param search_string: The string to search for
	:return: found_file_paths: A list of the paths of the found files
	:return: found_files_count: A dictionary containing the number of files found
	"""

	if VERBOSE: # If the VERBOSE constant is set to True
		print(f"{BackgroundColors.GREEN}Searching for {BackgroundColors.CYAN}{search_string} {BackgroundColors.GREEN}files in {BackgroundColors.CYAN}{search_directory}{Style.RESET_ALL}")

	found_files_count = 0 # Counter for the number of files found
	found_file_paths = [] # List to store the paths of the found files

	# Walk through the directory
	for root, _, files in os.walk(search_directory):
		for file in files: # Loop through the files
			file_path = os.path.join(root, file)

			# Verify if the file name matches the target file name
			if search_string in file:
				found_files_count += 1 # Increment the counter
				found_file_paths.append(file_path) # Add the file path to the list
					
	return found_file_paths, found_files_count # Return the list and the dictionary

def write_file_paths(found_file_paths, found_files_count, repository_name, current_directory):
	"""
	Write the found file paths to a text file.

	:param found_file_paths: A list of the paths of the found files
	:param found_files_count: A dictionary containing the number of files found
	:param repository_name: The name of the repository
	:param current_directory: The current directory
	:return: None
	"""
	
	output_file_path = f"{current_directory}/metrics_data/{repository_name}/track_files_list.txt"
	print(f"{BackgroundColors.GREEN}Writing found files to {BackgroundColors.CYAN}{output_file_path}{Style.RESET_ALL}")

	# If the found file paths list is empty, return
	if not found_file_paths:
		print(f"{BackgroundColors.RED}No files found in {BackgroundColors.CYAN}{repository_name}{Style.RESET_ALL}")
		return # Exit the function

	# Open the text file
	with open(output_file_path, "w") as file:
		# Write the found file paths to a text file
		file.write(f"Found files in PyDriller/diffs/{repository_name}: {found_files_count}\n")

		# For each file path in the list
		for path in found_file_paths:
			file.write(f"{path}\n") # Write the file path to the text file

def main():
	"""
   Main function.

   :return: None
   """

	# Print the welcome message
	print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Track Files{BackgroundColors.GREEN} script! This script is part of the {BackgroundColors.CYAN}Worked Example Miner (WEM){BackgroundColors.GREEN} project.{Style.RESET_ALL}", end="\n\n")
	
   # Directory to start the search from (current directory)
	current_directory = os.getcwd()

	# Search directories
	for repository_name in REPOSITORIES:
		print(f"{BackgroundColors.GREEN}Searching for {BackgroundColors.CYAN}changes files{BackgroundColors.GREEN} in {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

		# Set the search directory
		search_directory = os.path.join(current_directory, "diffs", repository_name)

		# Verify if the search directory exists
		if not os.path.isdir(search_directory):
			print(f"{BackgroundColors.RED}Directory {BackgroundColors.CYAN}PyDriller/diffs/{repository_name}{BackgroundColors.RED} does not exist{Style.RESET_ALL}")
			continue

		# Verify if the target file name is empty
		if not TARGET_FILENAMES[repository_name]:
			print(f"{BackgroundColors.RED}Target file name for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} is empty{Style.RESET_ALL}")
			continue

		# Call the function to start the search
		found_file_paths, found_files_count = search_files(search_directory, TARGET_FILENAMES[repository_name])

		print(f"{BackgroundColors.GREEN}Number of {BackgroundColors.CYAN}{TARGET_FILENAMES[repository_name]} {BackgroundColors.GREEN}files found in {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: {BackgroundColors.CYAN}{found_files_count}{Style.RESET_ALL}")

		# Sort the file paths based on the numeric value
		found_file_paths.sort(key=lambda path: int(re.search(rf"{repository_name}/(\d+)-", path).group(1)))

		# Write the file paths to a text file
		write_file_paths(found_file_paths, found_files_count, repository_name, current_directory)

	# Print the completion message
	print(f"\n{BackgroundColors.GREEN}The {BackgroundColors.CYAN}Track Files{BackgroundColors.GREEN} script has completed!{Style.RESET_ALL}")
 
if __name__ == '__main__':
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
