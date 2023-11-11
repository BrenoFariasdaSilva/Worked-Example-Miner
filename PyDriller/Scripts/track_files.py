import os # OS module provides functions for interacting with the operating system
import re # Regular expression operations module
from colorama import Style # Colorama is a Python library for printing colored text and stylizing terminal output.

# Macros:
class backgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red
	CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# List of target file names
TARGET_FILENAMES = {"commons-lang": "", "jabref": "", "kafka": "", "zookeeper": "CHANGES.txt.diff"}

# Repositories List
REPOSITORIES = ["commons-lang", "jabref", "kafka", "zookeeper"]

# @brief: This function searches for files in the given directory
# @param: search_directory - The directory to search in
# @param: search_string - The string to search for
# @return: found_file_paths - A list of the paths of the found files
# @return: file_counts - A dictionary containing the number of files found
def search_files(search_directory, search_string):
	file_counts = 0 # Counter for the number of files found
	found_file_paths = [] # List to store the paths of the found files
	# Walk through the directory
	for root, _, files in os.walk(search_directory):
		# Search for the target files
		for file in files:
			file_path = os.path.join(root, file)
			# Verify if the file name matches the target file name
			if search_string in file:
				file_counts += 1 # Increment the counter
				found_file_paths.append(file_path) # Add the file path to the list
					
	return found_file_paths, file_counts # Return the list and the dictionary

# @brief: This function writes the found file paths to a text file
# @param: found_file_paths - A list of the paths of the found files
# @param: repository_name - The name of the repository
# @param: current_directory - The current directory
# @return: None
def write_file_paths(found_file_paths, repository_name, current_directory):
	output_file_path = f"{current_directory}/metrics_data/{repository_name}/track_files_list.txt"
	print(f"{backgroundColors.GREEN}Writing found files to {backgroundColors.CYAN}{output_file_path}{Style.RESET_ALL}")

	# If the found file paths list is empty, return
	if not found_file_paths:
		print(f"{backgroundColors.RED}No files found in {backgroundColors.CYAN}{repository_name}{Style.RESET_ALL}")
		return # Exit the function

	# Write the found file paths to a text file
	with open(output_file_path, "w") as file:
		found_files_count = len(found_file_paths)
		file.write(f"Found files in PyDriller/diffs/{repository_name}: {found_files_count}\n")

		# For each file path in the list
		for path in found_file_paths:
			file.write(f"{path}\n") # Write the file path to the text file

# @brief: This is the main function
# @param: None
# @return: None
def main():
   # Directory to start the search from (current directory)
	current_directory = os.getcwd()

	# Search directories
	for repository_name in REPOSITORIES:
		print(f"{backgroundColors.GREEN}Searching for {backgroundColors.CYAN}changes files{backgroundColors.GREEN} in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}...{Style.RESET_ALL}")

		# Set the search directory
		search_directory = os.path.join(current_directory, "diffs", repository_name)

		# Verify if the search directory exists
		if not os.path.isdir(search_directory):
			print(f"{backgroundColors.RED}Directory {backgroundColors.CYAN}PyDriller/diffs/{repository_name}{backgroundColors.RED} does not exist{Style.RESET_ALL}")
			continue

		# Verify if the target file name is empty
		if not TARGET_FILENAMES[repository_name]:
			print(f"{backgroundColors.RED}Target file name for {backgroundColors.CYAN}{repository_name}{backgroundColors.RED} is empty{Style.RESET_ALL}")
			continue

		# Call the function to start the search
		found_file_paths, file_counts = search_files(search_directory, TARGET_FILENAMES[repository_name])

		print(f"{backgroundColors.GREEN}Number of {backgroundColors.CYAN}{TARGET_FILENAMES[repository_name]} {backgroundColors.GREEN}files found in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: {backgroundColors.CYAN}{file_counts}{Style.RESET_ALL}")

		# Sort the file paths based on the numeric value
		found_file_paths.sort(key=lambda path: int(re.search(rf"{repository_name}/(\d+)-", path).group(1)))

		# Write the file paths to a text file
		write_file_paths(found_file_paths, repository_name, current_directory)
 
# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
	main() # Call the main function
