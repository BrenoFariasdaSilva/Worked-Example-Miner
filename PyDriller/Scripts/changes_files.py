import os # OS module provides functions for interacting with the operating system
import re # Regular expression operations module
from colorama import Style # Colorama is a Python library for printing colored text and stylizing terminal output.

# Macros:
class backgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red

# List of target file names
TARGET_FILENAMES = ["CHANGES.txt.diff"]

# Repositories List
REPOSITORIES = ["commons-lang", "jabref", "kafka", "zookeeper"]

# @brief: This function searches for files in the given directory
# @param: directory - The directory to search in
# @param: file_counts - A dictionary to store the number of files found
# @param: found_file_paths - A list to store the paths of the found files
# @param: repository_name - The name of the repository
# @return: found_file_paths - A list of the paths of the found files
# @return: file_counts - A dictionary containing the number of files found
def search_files(directory, file_counts, found_file_paths, repository_name):
	for root, _, files in os.walk(directory):
		for file in files:
			file_path = os.path.join(root, file)
			for target_name in TARGET_FILENAMES:
				if file == target_name:
					file_counts[target_name] += 1
					found_file_paths.append(file_path)
	return found_file_paths, file_counts

# @brief: This function writes the found file paths to a text file
# @param: found_file_paths - A list of the paths of the found files
# @param: repository_name - The name of the repository
# @param: current_directory - The current directory
# @return: None
def write_file_paths(found_file_paths, repository_name, current_directory):
	output_file_path = f"{current_directory}/metrics_data/{repository_name}/changes_files_list.txt"
	print(f"{backgroundColors.GREEN}Writing found files to {backgroundColors.CYAN}{output_file_path}{Style.RESET_ALL}")
	with open(output_file_path, "w") as file:
		found_files_count = len(found_file_paths)
		file.write(f"Found files in PyDriller/diffs/{repository_name}: {found_files_count}\n")
		for path in found_file_paths:
			file.write(f"{path}\n")

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
 
		# Initialize counters
		file_counts = {name: 0 for name in TARGET_FILENAMES}
	
		# List to store found file paths
		found_file_paths = []
	
		# Call the function to start the search
		found_file_paths, file_counts = search_files(search_directory, file_counts, found_file_paths, repository_name)

		# Print the counts
		for name, count in file_counts.items():
			print(f"{backgroundColors.GREEN}Number of {backgroundColors.CYAN}{name} {backgroundColors.GREEN}files found in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: {backgroundColors.CYAN}{count}{Style.RESET_ALL}")

		# Sort the file paths based on the numeric value
		found_file_paths.sort(key=lambda path: int(re.search(r'zookeeper/(\d+)-', path).group(1)))

		# Write the file paths to a text file
		write_file_paths(found_file_paths, repository_name, current_directory)
 
# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
	main() # Call the main function