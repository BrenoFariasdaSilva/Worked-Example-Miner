import os # OS module provides functions for interacting with the operating system
import re # Regular expression operations module

# List of target file names
TARGET_FILENAMES = ["CHANGES.txt.diff"]

# @brief: This function searches for files in the given directory
# @param: directory - The directory to search in
# @param: file_counts - A dictionary to store the number of files found
# @param: found_file_paths - A list to store the paths of the found files
# @return: found_file_paths - A list of the paths of the found files
# @return: file_counts - A dictionary containing the number of files found
def search_files(directory, file_counts, found_file_paths):
	for root, _, files in os.walk(directory):
		for file in files:
			file_path = os.path.join(root, file)
			for target_name in TARGET_FILENAMES:
				if file == target_name:
					file_counts[target_name] += 1
					found_file_paths.append(file_path)
					print(f"Found {target_name} file: {file_path}")
	return found_file_paths, file_counts

# @brief: This function writes the found file paths to a text file
# @param: found_file_paths - A list of the paths of the found files
# @return: None
def write_file_paths(found_file_paths):
	output_file_path = "found_files.txt"
	with open(output_file_path, "w") as file:
		found_files_count = len(found_file_paths)
		file.write(f"Found {found_files_count} files\n")
		for path in found_file_paths:
			file.write(path + "\n")

# @brief: This is the main function
# @param: None
# @return: None
def main():
   # Directory to start the search from (current directory)
	current_directory = os.getcwd()
 
	# Initialize counters
	file_counts = {name: 0 for name in TARGET_FILENAMES}
 
	# List to store found file paths
	found_file_paths = []
 
	# Call the function to start the search
	found_file_paths, file_counts = search_files(current_directory, file_counts, found_file_paths)

	# Print the counts
	for name, count in file_counts.items():
		print(f"Number of {name} files found: {count}")

	# Sort the file paths based on the numeric value
	found_file_paths.sort(key=lambda path: int(re.search(r'zookeeper/(\d+)-', path).group(1)))

	# Write the file paths to a text file
	write_file_paths(found_file_paths)
 
# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
	main() # Call the main function