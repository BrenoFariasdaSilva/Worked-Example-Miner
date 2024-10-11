import atexit # For playing a sound when the program finishes
import csv # For reading csv files
import json # For reading the refactoring file from RefactoringMiner
import matplotlib.pyplot as plt # For plotting the graphs
import numpy as np # For calculating the min, max, avg, and third quartile of each metric
import os # For walking through directories
import pandas as pd # For the csv file operations
import platform # For determining the system's null device to discard output
import select # For waiting for input with a timeout
import sys # For reading the input
import time # For measuring the time
from colorama import Style # For coloring the terminal
from datetime import datetime # For date manipulation
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from sklearn.linear_model import LinearRegression # For the linear regression
from tqdm import tqdm # For progress bar

# Imports from the repositories_picker.py file
from repositories_picker import BackgroundColors # Import the BackgroundColors class
from repositories_picker import RELATIVE_REPOSITORIES_DIRECTORY_PATH, SOUND_FILE_PATH, START_PATH # Importing Constants from the repositories_picker.py file
from repositories_picker import create_directory, output_time, path_contains_whitespaces, play_sound, setup_repository, update_sound_file_path, verbose_output, verify_filepath_exists # Importing Functions from the repositories_picker.py file

# Imports from the code_metrics.py file
from code_metrics import CK_METRICS_FILES, CSV_FILE_EXTENSION, DEFAULT_REPOSITORIES, FULL_CK_METRICS_DIRECTORY_PATH, FULL_REFACTORINGS_DIRECTORY_PATH, FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH, PROCESS_JSON_REPOSITORIES, RELATIVE_REFACTORINGS_DIRECTORY_PATH # Importing Constants from the code_metrics.py file
from code_metrics import get_directories_size_in_gb, setup_process_repository, verify_repositories_execution_constants # Importing Functions from the code_metrics.py file

# Default values that can be changed:
VERBOSE = False # If True, then the program will output the progress of the execution
MINIMUM_CHANGES = 1 # The minimum number of changes a class/method should have to be considered
DESIRED_DECREASE = 0.00 # The desired decrease in the metric
IGNORE_CLASS_NAME_KEYWORDS = ["test"] # The keywords to ignore in the class name
IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS = ["anonymous"] # The keywords to ignore in the variable attribute
METRICS_INDEXES = {"CBO": 0, "DIT": 1, "LCOM": 2, "LOC": 3, "NOC": 4, "RFC": 5, "WMC": 6} # The position of the metrics in the metrics list
NUMBER_OF_METRICS = len(METRICS_INDEXES.keys()) # The number of metrics
DESIRED_REFACTORINGS_ONLY = False # If True, then only the desired refactorings will be stored
DESIRED_REFACTORINGS = ["Extract Method", "Extract Class", "Pull Up Method", "Push Down Method", "Extract Superclass", "Move Method"] # The desired refactorings to search for substantial changes
WRITE_FULL_HISTORY = False # If True, then the metrics evolution will store all of the metrics history and not only the moments the metrics changed between commits

RUN_FUNCTIONS = { # Dictionary with the functions to run and their respective booleans
	"Linear Regression": True, # Run the linear regression graphics
	"Metrics Decrease": True, # Verify the substantial metric decrease
	"Metrics Evolution": True, # Write the metrics evolution to a csv file
	"Metrics Statistics": True, # Generate the metrics track record statistics
	"Metrics Track Record": True, # Write the metrics track record to a txt file
	"Sort by Percentual Variation": True, # Sort the csv file by the percentual variation
}

# Constants:
PROCESS_CLASSES = True # If True, then the classes will be processed, otherwise the methods will be processed

# Extensions:
PNG_FILE_EXTENSION = ".png" # The extension of the PNG files
REFACTORING_MINER_JSON_FILE_EXTENSION = ".json" # The extension of the RefactoringMiner JSON files

# Filenames:
CK_CSV_FILE = CK_METRICS_FILES[0] if PROCESS_CLASSES else CK_METRICS_FILES[1] # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
UNSORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_unsorted_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the top changed methods
SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the sorted top changed methods
SUBSTANTIAL_CHANGES_FILENAME = f"substantial_METRIC_NAME_{CLASSES_OR_METHODS}_changes{CSV_FILE_EXTENSION}" # The relative path to the directory containing the interesting changes

# Relative Paths:
RELATIVE_METRICS_DATA_DIRECTORY_PATH = "/metrics_data" # The relative path to the directory containing the metrics evolution
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution" # The relative path to the directory containing the metrics evolution
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics" # The relative path to the directory containing the metrics statistics
RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH = "/metrics_predictions" # The relative path to the directory containing the metrics prediction
RELATIVE_REFACTORING_MINER_DIRECTORY_PATH = "../RefactoringMiner/RefactoringMiner-2.4.0/bin/RefactoringMiner" # The relative path to the RefactoringMiner directory

# Full Paths (Start Path + Relative Paths):
FULL_METRICS_DATA_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_DATA_DIRECTORY_PATH}" # The full path to the directory containing the metrics evolution
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics evolution
FULL_METRICS_STATISTICS_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}" # The full path to the directory containing the metrics statistics
FULL_METRICS_PREDICTION_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics prediction
OUTPUT_DIRECTORIES = [FULL_METRICS_DATA_DIRECTORY_PATH, FULL_METRICS_EVOLUTION_DIRECTORY_PATH, FULL_METRICS_STATISTICS_DIRECTORY_PATH, FULL_METRICS_PREDICTION_DIRECTORY_PATH] # The output directories list

def input_with_timeout(prompt, timeout=60):
	"""
	Prompts the user for input with a specified timeout on Unix-based systems.
	
	:param prompt: str, the prompt message to display
	:param timeout: int, the timeout in seconds
	:return: str, the user input or None if timeout
	"""
	
	print(prompt, end="", flush=True) # Print the prompt message without a newline character

	ready, _, _ = select.select([sys.stdin], [], [], timeout) # Wait for input with a timeout

	if ready: # If input is ready
		return sys.stdin.readline().strip().lower() # Read and return user input
	else: # If timeout is reached
		return None # Return None if timeout is reached

def update_global_variables_for_processing(process_classes):
	"""
	Updates global variables based on whether to process classes or methods.

	:param process_classes: bool, if True, processes classes; if False, processes methods
	"""

	global PROCESS_CLASSES, CK_CSV_FILE, CLASSES_OR_METHODS, UNSORTED_CHANGED_METHODS_CSV_FILENAME, SORTED_CHANGED_METHODS_CSV_FILENAME, SUBSTANTIAL_CHANGES_FILENAME # Specify the global variables to update
	
	PROCESS_CLASSES = process_classes # Update the PROCESS_CLASSES constant
	CK_CSV_FILE = CK_METRICS_FILES[0] if PROCESS_CLASSES else CK_METRICS_FILES[1] # Update the CK_CSV_FILE constant
	CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # Update the CLASSES_OR_METHODS constant
	UNSORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_unsorted_changes.{CK_CSV_FILE.split('.')[1]}" # Update the UNSORTED_CHANGED_METHODS_CSV_FILENAME constant
	SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_changes.{CK_CSV_FILE.split('.')[1]}" # Update the SORTED_CHANGED_METHODS_CSV_FILENAME constant
	SUBSTANTIAL_CHANGES_FILENAME = f"substantial_METRIC_NAME_{CLASSES_OR_METHODS}_changes{CSV_FILE_EXTENSION}" # Update the SUBSTANTIAL_CHANGES_FILENAME constant

def process_classes_and_methods():
	"""
	Processes data for both classes and methods.
	"""

	# Process classes
	update_global_variables_for_processing(True) # Update the global variables for processing classes
	process_all_repositories() # Process all repositories

	# Process methods
	update_global_variables_for_processing(False) # Update the global variables for processing methods
	process_all_repositories() # Process all repositories

def process_based_on_user_input(user_response):
	"""
	Processes data based on user input.

	:param user_response: str, the user input
	"""

	process_classes = user_response == "true" # If the user input is "true", then process classes, otherwise process methods (False)
	update_global_variables_for_processing(process_classes) # Update the global variables for processing classes or methods
	process_all_repositories() # Process all repositories

def get_directory_path(repository_name):
	"""
	Gets the path to the directory of the CK metrics related to the repository.

	:param repository_name: The name of the repository to be analyzed
	:return: The path to the directory of the CK metrics related to the repository
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the directory path for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	repository_ck_metrics_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}" # Get the directory path for the specified repository name
	return repository_ck_metrics_path # Return the path to the directory of the CK metrics related to the repository

def create_directories(repository_name):
	"""
	Creates all the desired directories.

	:param repository_name: The name of the repository to be analyzed
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Creating the desired directories for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

	# Create the output METRICS_DATA directories if they does not exist
	create_directory(FULL_METRICS_DATA_DIRECTORY_PATH, RELATIVE_METRICS_DATA_DIRECTORY_PATH)
	create_directory(f"{FULL_METRICS_DATA_DIRECTORY_PATH}/{repository_name}", f"{RELATIVE_METRICS_DATA_DIRECTORY_PATH}/{repository_name}")

	# Create the output METRICS_EVOLUTION directories if they does not exist
	create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH)
	create_directory(f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}", f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}") # Create the directory where the csv file will be stored

	# Create the output RELATIVE_METRICS_STATISTICS directories if they does not exist
	create_directory(FULL_METRICS_STATISTICS_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH)
	create_directory(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}", f"{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}")
	
	# Create the output RELATIVE_METRICS_PREDICTION directories if they does not exist
	create_directory(FULL_METRICS_PREDICTION_DIRECTORY_PATH, RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH)
	create_directory(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}", f"{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}")

def generate_repository_commits_modified_files_dict(repository_name, commit_hash=None):
	"""
	Generates a dictionary of the modified files path list for each commit, or for a specific commit if a commit hash is given.

	:param repository_name: The name of the repository
	:param commit_hash: The hash of a specific commit (optional). If provided, only that commit's modified files will be listed.
	:return: A dictionary containing the modified files paths list for each commit (or for the specified commit)
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Generating the commit dictionary for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

	commit_modified_files_dict = {} # A dictionary containing commit hashes as keys and the modified files path list as values
	repo_url = DEFAULT_REPOSITORIES[repository_name] # Access the repository URL

	if commit_hash: # Process only the given commit hash if it is provided
		commit = next(Repository(repo_url, single=commit_hash).traverse_commits()) # Get the specific commit
		commit_modified_files_dict[commit.hash] = [path for modified_file in commit.modified_files for path in (modified_file.old_path, modified_file.new_path) if path] # Get the modified files paths for the specific commit
	else: # Process all commits if no specific commit hash is given
		for commit in Repository(repo_url).traverse_commits(): # Traverse through all commits
			commit_modified_files_dict[commit.hash] = [path for modified_file in commit.modified_files for path in (modified_file.old_path, modified_file.new_path) if path] # Get the modified files paths for each commit

	return commit_modified_files_dict # Return the commit dictionary containing the modified files paths

def valid_class_name(class_name):
	"""
	Validates the class name.

	:param class_name: The name of the class
	:return: True if the class name is valid, False otherwise
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Validating the class name...{Style.RESET_ALL}")
	
	return "." in class_name # If the class name contains a dot, then it is valid (it is a package name) and returns True

def get_class_package_name(file_name):
	"""
	Gets the package name of the class.

	:param file_name: The file name where the class is located
	:return: The package name of the class
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the package name of the class...{Style.RESET_ALL}")
	
	start_substring = "/src/" # The start substring
	package_name = file_name[file_name.find(start_substring) + len(start_substring):file_name.rfind(".")] # Get the substring that comes after the: /src/ and before the last dot

	package_name = package_name.replace("/", ".") # Replace the slashes with dots

	return package_name # Return the package name

def get_identifier(row):
	"""
	Gets the identifier of the class or method.

	:param row: The row of the csv file
	:return: The identifier of the class or method
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the identifier and metrics of the class or method...{Style.RESET_ALL}")
	
	if not valid_class_name(row["class"]): # If the class name is not valid (it is not a package name)
		return None # Return None if the class name is not valid

	identifier = f"{row["class"]} {row["type"] if PROCESS_CLASSES else row["method"]}" # The identifier of the class or method

	return identifier # Return the identifier of the class or method

def get_ck_metrics_tuple(row):
	"""
	Gets the metrics of the class or method.

	:param row: The row of the csv file
	:return: The metrics of the class or method as a tuple
	"""
	
	# Use a list comprehension to extract metrics based on the indexes
	metrics = tuple(float(row[metric.lower()]) for metric in METRICS_INDEXES.keys())
	
	return metrics # Return the metrics of the class or method as a tuple

def get_methods_invoked(row):
	"""
	Gets the method invoked of the class or method.

	:param row: The row of the csv file
	:return: The method invoked of the class or method
	"""

	methods_invoked = row["methodInvocations"] if PROCESS_CLASSES else int(row["methodsInvokedQty"]) # Get the methodInvocations (str) or methodsInvokedQty (int) from the row
	
	return methods_invoked # Return the methods_invoked of the class or method

def was_file_modified(ck_metrics, identifier, commit_number, metrics_track_record):
	"""
	Verifies if the file was modified.

	:param ck_metrics: A tuple containing the CK metrics
	param identifier: The identifier (class or method name) to be added or updated
	:param commit_number: The commit number of the current row
	:param metrics_track_record: A dictionary containing the track record of the metrics of each class or method
	:return: True if the file was modified, False otherwise
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the CK Metrics was modified since the last commit...{Style.RESET_ALL}")

	if identifier not in metrics_track_record.keys(): # If the identifier is not a key in the metrics_track_record dictionary
		return True # Return True if the identifier is not in the dictionary
	
	if commit_number not in metrics_track_record[identifier]["commit_hashes"]: # If the commit number is not in the commit hashes list
		return True # Return True if the commit number is not in the commit hashes list
	
	ck_metrics_history = metrics_track_record[identifier]["metrics"] # Get the metrics history of the class or method

	return True if ck_metrics != ck_metrics_history[-1] else False # Return True if the CK Metrics was modified since the last commit, otherwise return False

def update_metrics_track_record(metrics_track_record, identifier, commit_number, ck_metrics, methods_invoked):
	"""
	Updates the metrics track record with new metrics information.

	:param metrics_track_record: A dictionary containing the track record of the metrics of each class or method
	:param identifier: The identifier (class or method name) to be added or updated
	:param commit_number: The commit number of the current row
	:param ck_metrics: A tuple containing the CK metrics
	:param methods_invoked: The method invoked str or methodsInvokedQty int
	:return: None
	"""

	if identifier not in metrics_track_record: # If the identifier is not in the dictionary, add it
		metrics_track_record[identifier] = { # Add the identifier to the metrics_track_record dictionary
			"metrics": [], # The metrics list
			"commit_hashes": [], # The commit hashes list
			"changed": 0, # The number of times the metrics changed
			"code_churns": [], # The code churns values list
			"lines_added": [], # The lines added list
			"lines_deleted": [], # The lines deleted list
			"modified_files_count": [], # The modified files count list
			"methods_invoked": methods_invoked, # The methods_invoked str or methodsInvokedQty int
		}

	metrics_track_record[identifier]["metrics"].append(ck_metrics) # Append the metrics to the metrics list
	metrics_track_record[identifier]["commit_hashes"].append(commit_number) # Append the commit number to the commit hashes list
	metrics_track_record[identifier]["changed"] += 1 # Increment the change count

def get_diff_filepath(ck_file_path, file_in_repository_path):
	"""
	Get the diff file path from the CK file path and the repository file path.

	:param ck_file_path: The CK file path
	:param file_in_repository_path: The path of the file in the repository
	:return: The diff file path
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Converting the CK file path to the diff file path...{Style.RESET_ALL}")

	filename = file_in_repository_path.split("/")[-1]
	diff_dir = ck_file_path.replace("ck_metrics", "diffs") # Get the diff directory
	diff_dir = diff_dir[:diff_dir.rfind("/")] # Remove everything after the last slash (including the slash)
	diff_filepath = f"{diff_dir}/{filename}" # Get the diff filename

	return diff_filepath # Return the diff file path

def convert_ck_classname_to_filename_format(diff_filepath, ck_classname):
	"""
	Convert CK classname format to the filename format used by code churn
	
	:param diff_filepath: The path to the diff file.
	:param ck_classname: The classname from the CK tool
	:return: The converted classname in filename format
	"""
	
	filename = diff_filepath.split("/")[-1] # Get the filename from the diff file path
	filename = filename[:filename.find(".")] # Remove the extension from the filename
	classname = ck_classname[ck_classname.find(filename):] # Get the classname from the CK classname
	return classname.replace("/", ".") # Replace the dots with slashes

def extract_inner_class_name(class_name):
	"""
	Extracts the inner class name from the class name, which starts with a "$".

	:param class_name: The class name which may contain a method name.
	:return: The extracted inner class name if it exists, otherwise None.
	"""

	return class_name.split("$")[1] if "$" in class_name else None # Return inner class name if it exists

def prepare_class_base_name(class_name):
	"""
	Prepare the base class name and extract the last capitalized word.

	:param class_name: The full class name, possibly with inner classes.
	:return: A tuple of the base class name and the last capitalized word.
	"""

	class_base_name = class_name.split("$")[0] # Extract the base class name (without inner class)
	last_capitalized_word = next((class_base_name[i:] for i in range(len(class_base_name) - 1, -1, -1) if class_base_name[i].isupper()), None) # Find the last capitalized word
	return class_base_name, last_capitalized_word # Return the base class name and last capitalized word

def count_lines_within_code_block(line, lines_added, lines_deleted):
	"""
	Count the lines added and deleted based on the diff line content inside a code block.

	:param line: The current line from the diff file.
	:param lines_added: The current count of lines added.
	:param lines_deleted: The current count of lines deleted.
	:return: Updated counts of lines added and deleted.
	"""

	if line.startswith("+") and not line.startswith("+++"): # Count added lines (starting with "+", excluding diff file headers)
		lines_added += 1 # Increment the lines added

	elif line.startswith("-") and not line.startswith("---"): # Count deleted lines (starting with "-", excluding diff file headers)
		lines_deleted += 1 # Increment the lines deleted

	return lines_added, lines_deleted # Return updated counts

def remove_last_capitalized_word(class_base_name):
	"""
	Remove the last capitalized word from the class base name.

	:param class_base_name: The base class name.
	:return: The class base name without the last capitalized word.
	"""

	last_capitalized_word_position = next((i for i in range(len(class_base_name) - 1, -1, -1) if class_base_name[i].isupper()), None) # Find the position of the last capitalized word
	return class_base_name[:last_capitalized_word_position] if last_capitalized_word_position is not None else "" # Return updated base name

def find_diff_file_path(diff_file_path, class_base_name, max_levels=2):
	"""
	Traverse up to max_levels to find the diff file path.

	:param diff_file_path: The original diff file path.
	:param class_base_name: The base class name to search for the diff file.
	:param max_levels: Maximum number of directory levels to go up while searching.
	:return: The correct diff file path if found, otherwise None.
	"""

	current_class_path = f"{class_base_name}.java.diff" # Start with the full class name for the diff file
	levels_up = 0 # Counter to track levels we have gone up

	while levels_up < max_levels: # While we have not reached the maximum levels up
		candidate_diff_file_path = os.path.join(os.path.dirname(diff_file_path), current_class_path) # Get candidate diff file path
		if os.path.exists(candidate_diff_file_path): # If the file exists, return the path
			return candidate_diff_file_path # Return the candidate diff file path

		class_base_name = remove_last_capitalized_word(class_base_name) # Update class base name
		current_class_path = f"{class_base_name}.java.diff" # Update current class path for the next level up
		levels_up += 1 # Increment the levels up counter

	return None # Return None if the diff file is not found within the max levels

def process_diff_lines(java_file, last_capitalized_word, inner_class_name, lines_added, lines_deleted):
	"""
	Iterate over the lines in the diff file and count lines added or deleted.

	:param java_file: The opened diff file.
	:param last_capitalized_word: The last capitalized word of the class.
	:param inner_class_name: The inner class name (if any).
	:param lines_added: Current count of lines added.
	:param lines_deleted: Current count of lines deleted.
	:return: A tuple of the updated lines added and deleted.
	"""

	in_class_block = False # Track if we are inside the last capitalized word class block
	open_braces_count = 0 # Track braces to determine the start and end of a class

	for line in java_file: # Iterate through the lines of the Java file
		if last_capitalized_word and f"class {last_capitalized_word}" in line and "{" in line: # If the class is found
			in_class_block = True # Enter the class block
			open_braces_count = 1 # Start counting braces

		elif in_class_block: # If inside the class block
			open_braces_count += line.count("{") # Increment for opening braces
			open_braces_count -= line.count("}") # Decrement for closing braces

			if open_braces_count == 0: # If braces balance out, exit the class block
				in_class_block = False # Exit the class block

		if inner_class_name and not in_class_block: # If an inner class is specified, skip lines outside the class block
			continue # Skip the line if an inner class is specified and we are not in the class block

		lines_added, lines_deleted = count_lines_within_code_block(line, lines_added, lines_deleted) # Count the lines added and deleted

	return lines_added, lines_deleted # Return the updated lines added and deleted

def process_diff_file(diff_file_path, last_capitalized_word, inner_class_name, lines_added, lines_deleted):
	"""
	Process the diff file and count lines added and deleted.

	:param diff_file_path: The path to the diff file.
	:param last_capitalized_word: The last capitalized word of the class.
	:param inner_class_name: The inner class name (if any).
	:param lines_added: Current count of lines added.
	:param lines_deleted: Current count of lines deleted.
	:return: A tuple of the updated lines added and deleted.
	"""

	try: # Try to open the diff file
		with open(diff_file_path, "r") as java_file: # Open the diff file
			return process_diff_lines(java_file, last_capitalized_word, inner_class_name, lines_added, lines_deleted) # Process the lines in the diff file

	except FileNotFoundError: # Catch the FileNotFoundError exception
		raise FileNotFoundError(f"{BackgroundColors.RED}Error: Diff file {BackgroundColors.GREEN}{diff_file_path}{BackgroundColors.RED} not found{Style.RESET_ALL}") # Raise an error if the file is not found

	except Exception as e: # Catch any other exceptions
		raise Exception(f"{BackgroundColors.RED}Error: An error occurred while reading the diff file {BackgroundColors.GREEN}{diff_file_path}{BackgroundColors.RED}: {e}{Style.RESET_ALL}") # Raise an error if an exception occurs

def get_code_churn_attributes(diff_file_path, class_name):
	"""
	Get the code churn attributes (lines added and deleted) from the diff file path, handling inner classes if necessary.

	:param diff_file_path: The diff file path.
	:param class_name: The class name, possibly with an inner class.
	:return: A tuple containing lines added and lines deleted.
	"""

	lines_added, lines_deleted = 0, 0 # Initialize the lines added and deleted
	inner_class_name = extract_inner_class_name(class_name) # Extract the inner class name if it exists
	class_base_name, last_capitalized_word = prepare_class_base_name(class_name) # Get base class name and last capitalized word
	diff_file_path = find_diff_file_path(diff_file_path, class_base_name) # Find the diff file path for the class

	if diff_file_path is None: # If no diff file is found, return 0 for added and deleted lines
		return lines_added, lines_deleted # Return 0 for added and deleted lines

	return process_diff_file(diff_file_path, last_capitalized_word, inner_class_name, lines_added, lines_deleted) # Process the diff file

def get_code_churn(lines_added, lines_deleted):
	"""
	Get the code churn value given the churn attributes.

	:param lines_added: The number of lines added.
	:param lines_deleted: The number of lines deleted.
	:return: The code churn value (lines added + lines deleted).
	"""

	code_churn_value = lines_added + lines_deleted # Calculate the code churn value.
	return code_churn_value # Return the code churn value.

def update_code_churn_and_file_info(metrics_track_record, identifier, lines_added, lines_deleted, code_churn_value, commit_modified_files_dict, commit_hash):
	"""
	Updates the code churn and file modification information in the metrics track record.

	:param metrics_track_record: A dictionary containing the track record of the metrics of each class or method
	:param identifier: The identifier (class or method name) to be updated
	:param lines_added: The number of lines added
	:param lines_deleted: The number of lines deleted
	:param code_churn_value: The code churn value
	:param commit_modified_files_dict: A dictionary with commit hashes as keys and modified files as values
	:param commit_hash: The current commit hash being processed
	:return: None
	"""

	metrics_track_record[identifier]["code_churns"].append(code_churn_value) # Append the code churn value to the code churns list
	metrics_track_record[identifier]["lines_added"].append(lines_added) # Append the lines added to the lines added list
	metrics_track_record[identifier]["lines_deleted"].append(lines_deleted) # Append the lines deleted to the lines deleted list

	modified_files_count = len(commit_modified_files_dict[commit_hash]) # Get the number of modified files for the current commit hash
	metrics_track_record[identifier]["modified_files_count"].append(modified_files_count) # Append the modified files count to the modified files count list

def process_csv_file(file_path, commit_modified_files_dict, metrics_track_record):
	"""
	Processes a csv file containing the metrics of a class or method.

	:param file_path: The path to the csv file
	:param commit_modified_files_dict: A dictionary containing the commit hashes as keys and the modified files list as values
	:param metrics_track_record: A dictionary containing the track record of the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the csv file containing the metrics of a class or method...{Style.RESET_ALL}")

	with open(file_path, "r") as csvfile: # Open the csv file
		reader = csv.DictReader(csvfile) # Read the csv file
		for row in reader: # For each row in the csv file
			identifier = get_identifier(row) # Get the identifier of the class or method
			ck_metrics = get_ck_metrics_tuple(row) # Get the metrics of the class or method
			methods_invoked = get_methods_invoked(row) # Get the method invoked of the class or method
			
			commit_number = file_path[file_path.rfind("/", 0, file_path.rfind("/")) + 1:file_path.rfind("/")] # Get the commit number from the file path
			commit_hash = commit_number.split("-")[1] # Get the commit hash from the commit number

			if was_file_modified(ck_metrics, identifier, commit_number, metrics_track_record) and commit_modified_files_dict[commit_hash]: # If the file was modified, then update the metrics track record
				update_metrics_track_record(metrics_track_record, identifier, commit_number, ck_metrics, methods_invoked) # Update the metrics track record
				diff_filepath = get_diff_filepath(file_path, row["file"]) # Get the diff file path
				class_name = convert_ck_classname_to_filename_format(diff_filepath, row["class"]) # Convert the CK class name to the filename format
				lines_added, lines_deleted = get_code_churn_attributes(diff_filepath, class_name) # Get the code churn attributes
				update_code_churn_and_file_info(metrics_track_record, identifier, lines_added, lines_deleted, get_code_churn(lines_added, lines_deleted), commit_modified_files_dict, commit_hash) # Update the code churn and file info

def traverse_directory(repository_name, repository_ck_metrics_path):
	"""
	Traverses a directory and processes all the csv files.

	:param repository_name: The name of the repository
	:param repository_ck_metrics_path: The path to the directory
	:return: A dictionary containing the metrics of each class and method combination
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Traversing the directory and processing all the csv files for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	metrics_track_record = {} # Dictionary containing the track record of the metrics of each method nor class. The key is the identifier and the value is a dictionary containing the metrics, commit hashes and the number of times the metrics changed.
	file_count = 0 # Initialize the file count

	commit_modified_files_dict = generate_repository_commits_modified_files_dict(repository_name) # Generate the commit modified files dictionary, having the commit hashes as keys and the modified files list as values
	total_files = sum(file == CK_CSV_FILE for _, _, files in os.walk(repository_ck_metrics_path) for file in files) # Get the total number of files in the directory

	# Iterate through each directory inside the repository_directory and call the process_csv_file function to get the methods metrics of each file
	with tqdm(total=total_files, unit=f" {BackgroundColors.GREEN}Processing all of the {BackgroundColors.CYAN}{repository_ck_metrics_path.split('/')[-1]} CSV Files{Style.RESET_ALL}") as progress_bar:
		for root, subdirs, files in os.walk(repository_ck_metrics_path): # Walk through the directory
			subdirs.sort(key=lambda x: int(x.split("-")[0])) # Sort the subdirectories in ascending order by the substring that comes before the "-"
			for dir in subdirs: # For each subdirectory
				for file in os.listdir(os.path.join(root, dir)): # For each file in the subdirectory
					if file == CK_CSV_FILE: # If the file is the desired csv file
						process_csv_file(os.path.join(root, os.path.join(dir, file)), commit_modified_files_dict, metrics_track_record) # Process the csv file
						file_count += 1 # Increment the file count
						progress_bar.update(1) # Update the progress bar

	return metrics_track_record # Return the method metrics, which is a dictionary containing the metrics of each method

def sort_commit_hashes_by_commit_number(metrics_track_record):
	"""
	Sorts the commit_hashes list for each entry in the metrics_track_record dictionary
	by the commit number (numeric value before the hyphen).

	:param metrics_track_record: A dictionary where each key maps to another dictionary that contains a list under the key "commit_hashes".
	:return: The sorted metrics_track_record
	"""

	for key in metrics_track_record: # For each key in the metrics_track_record dictionary
		metrics_track_record[key]["commit_hashes"].sort(key=lambda x: int(x.split("-")[0])) # Sort the commit hashes list for each class or method according to the commit number

	return metrics_track_record # Return the sorted metrics_track_record

def generate_progress_bar_description():
	"""
	Generates the description for the progress bar.

	:return: A string containing the description for the progress bar
	"""

	processes = [key.title() for key, value in sorted(RUN_FUNCTIONS.items()) if value and key != "Sort by Percentual Variation"] # Get the processes that are set to True
	metrics_description = ", ".join(processes) # Join the processes with a comma
	progress_description = f"{BackgroundColors.GREEN}Generating {BackgroundColors.CYAN}{metrics_description}{BackgroundColors.GREEN}...{Style.RESET_ALL}" if processes else f"{BackgroundColors.GREEN}Processing Metrics..{Style.RESET_ALL}" # Generate the description for the progress bar

	return progress_description # Return the description for the progress bar

def get_clean_id(id):
	"""
	Receives an id and verifies if it contains slashes, if so, it returns the id without the slashes.

	:param id: ID of the class or method to be analyzed
	:return: ID of the class or method to be analyzed without the slashes
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the clean id for {BackgroundColors.CYAN}{id}{BackgroundColors.GREEN}...{Style.RESET_ALL}")
	
	if "/" in id: # If the id contains slashes, remove them
		return str(id.split("/")[0:-1])[2:-2] # Return the id without the slashes
	else: # If the id does not contain slashes, simply return the id
		return id # Return the id

def write_metrics_track_record_to_txt(filename, repository_name, identifier, record):
	"""
	Writes the metrics_track_record to a txt file.

	:param repository_name: The name of the repository
	:param identifier: The identifier of the class or method
	:param record: A dictionary containing the metrics of the identifier
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the metrics track record for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to a txt file...{Style.RESET_ALL}")

	with open(filename, "a") as file: # Open the txt file and write the metrics_track_record to it
		file.write(f"{identifier}: \n") # Write the key
		file.write(f"\tMetrics: {record['metrics']}\n") # Write the metrics
		file.write(f"\tCommit Hashes: {record['commit_hashes']}\n") # Write the commit hashes
		file.write(f"\tChanged: {record['changed']}\n") # Write the changed value
		file.write(f"\tCode Churns: {record['code_churns']}\n") # Write the code churns value
		file.write(f"\tLines Added: {record['lines_added']}\n") # Write the lines added
		file.write(f"\tLines Deleted: {record['lines_deleted']}\n") # Write the lines deleted
		file.write(f"\tModified Files Count: {record['modified_files_count']}\n") # Write the modified files count
		file.write(f"\t{'Method Invocations' if PROCESS_CLASSES else 'Methods Invoked Qty'}: {record['methods_invoked']}\n") # Write the 'Method Invocations' if PROCESS_CLASS, else 'Methods Invoked Qty' value
		file.write(f"\n") # Write a new line

def setup_write_metrics_track_record_to_txt(repository_name, identifier, record, iteration):
	"""
	Sets up the writing of the metrics track record to a txt file.

	:param repository_name: The name of the repository.
	:param identifier: The identifier of the class or method.
	:param record: A dictionary containing the metrics of the identifier.
	:param iteration: The current iteration of the analysis.
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Setting up the writing of the metrics track record to a txt file for {identifier.split(' ')[0]} {identifier.split(' ')[1]} in the {repository_name} repository...{Style.RESET_ALL}")

	initial_file_path = f"{CLASSES_OR_METHODS}_metrics_track_record.txt" # The initial file path
	filename = f"{FULL_METRICS_DATA_DIRECTORY_PATH}/{repository_name}/{initial_file_path}" # The filename of the metrics track record
	os.remove(filename) if (verify_filepath_exists(filename) and iteration == 1) else None # Remove the file if it exists

	write_metrics_track_record_to_txt(filename, repository_name, identifier, record) # Write the metrics track record to a txt file

def write_metrics_evolution_to_csv(repository_name, filename, class_name, variable_attribute, record):
	"""
	Writes the metrics for a specific class or method to a CSV file.

	:param repository_name: The name of the repository
	:param filename: The path of the CSV file to write to
	:param class_name: The name of the class
	:param variable_attribute: The variable attribute (class or method name)
	:param record: The record containing additional information for writing
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the metrics evolution for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to a csv file...{Style.RESET_ALL}")

	with open(filename, "w") as csvfile: # Open the csv file and write the metrics to it
		writer = csv.writer(csvfile) # Create the csv writer
		if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
			writer.writerow(["Class", "Type", "Commit Number", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files", *[metric for metric in METRICS_INDEXES.keys()], "Methods Invoked Qty"]) # Write the header to the csv file
		else: # If the PROCESS_CLASSES constant is set to False
			writer.writerow(["Class", "Method", "Commit Number", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files", *[metric for metric in METRICS_INDEXES.keys()], "Methods Invoked Qty"]) # Write the header to the csv file

		previous_metrics = None # Initialize to None for the first iteration
		metrics = record["metrics"] # Get the metrics from the record

		for i in range(len(metrics)): # For each metric in the metrics list
			current_metrics = list(metrics[i]) # Tuple of current metrics based on METRICS_INDEXES
			if WRITE_FULL_HISTORY or (previous_metrics is None or current_metrics != previous_metrics): # Verify if the metrics tuple is different from the previous metrics tuple
				commit_number, commit_hash = record["commit_hashes"][i].split("-") # Split the commit hash to get the commit number and commit hash
				writer.writerow([class_name, variable_attribute, commit_number, commit_hash, record["code_churns"][i], record["lines_added"][i], record["lines_deleted"][i], record["modified_files_count"][i], *current_metrics, record["methods_invoked"]]) # Write the unique identifier and metrics to the csv file
			previous_metrics = current_metrics # Update previous metrics

def setup_write_metrics_evolution_to_csv(repository_name, class_name, variable_attribute, record):
	"""
	Sets up the writing of the metrics evolution to a CSV file.

	:param repository_name: The name of the repository
	:param class_name: The name of the class
	:param variable_attribute: The variable attribute (class or method name)
	:param record: The record containing additional information for writing
	:return: None
	"""

	full_metrics_evolution_directory_path = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/" # The path to the directory where the csv file will be stored
	create_directory(full_metrics_evolution_directory_path, f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}") # Create the directory where the csv file will be stored
	metrics_filename = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}" # The path to the csv file

	write_metrics_evolution_to_csv(repository_name, metrics_filename, class_name, variable_attribute, record) # Call the new auxiliary function

def found_ignore_keywords(source, keywords, entity_type):
	"""
	Verifies if the source of the specified entity type contains any of the ignore keywords.

	:param source: The source of the entity
	:param keywords: The ignore keywords
	:param entity_type: The type of the entity
	:return: True if the source contains any of the ignore keywords, False otherwise
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the class name or variable attribute contains any of the ignore keywords...{Style.RESET_ALL}")

	if any(keyword.lower() in source.lower() for keyword in keywords): # If any of the ignore keywords is in the source
		verbose_output(true_string=f"{BackgroundColors.YELLOW}Ignoring {entity_type} {source} as the name contains one of the ignore keywords: {keywords}{Style.RESET_ALL}")
		return True # Return True if the source contains any of the ignore keywords
	return False # Return False if the source does not contain any of the ignore keywords

def add_substantial_decrease_csv_header(csv_filename, metric_name):
	""""
	Adds the header to the csv file, if it does not exist.

	:param csv_filename: The name of the csv file
	:param metric_name: The name of the metric
	:return: None
	"""

	expected_header = [] # The expected header list
	if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
		expected_header = ["Class", "Type", f"Percentual Variation {metric_name}" + "Commit Number", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files"] + list(METRICS_INDEXES.keys()) + ["Method Invocations", "Refactoring Patterns"]
	else: # If the PROCESS_CLASSES constant is set to False
		expected_header = ["Class", "Method", f"Percentual Variation {metric_name}" + "Commit Number", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files"] + list(METRICS_INDEXES.keys()) + ["Methods Invoked Qty", "Refactoring Patterns"]
	
	with open(csv_filename, "w") as csvfile: # Open the csv file in write mode
		writer = csv.writer(csvfile) # Create the csv writer
		writer.writerow(expected_header) # Write the expected header

def setup_substantial_decrease_file(repository_name, metric_name, iteration):
	"""
	Sets up the substantial decrease file for the specified repository and metric name.

	:param repository_name: The name of the repository
	:param metric_name: The name of the metric
	:param iteration: The current iteration
	:return: The path to the substantial decrease file
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Setting up the substantial decrease file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

	csv_filename = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME.replace('METRIC_NAME', metric_name)}" # The csv file name

	if verify_filepath_exists(csv_filename) and iteration == 1: # Verify if the CSV file exists and if it's the first iteration
		add_substantial_decrease_csv_header(csv_filename, metric_name) # Add the header to the CSV file

	return csv_filename # Return the path to the substantial decrease file

def extract_commit_data(commit_hashes, index):
	"""
	Extracts commit data from commit hashes.

	:param commit_hashes: The list of commit hashes
	:param index: The current index in the commit hashes list
	:return: The extracted commit data (index, previous commit number, previous commit hash, current commit number, current commit hash)
	"""

	return [index, commit_hashes[index - 1].split("-")[0], commit_hashes[index - 1].split("-")[1], commit_hashes[index].split("-")[0], commit_hashes[index].split("-")[1]]

def verify_refactoring_file(refactoring_file_path):
	"""
	Validates if the refactoring file was created successfully.

	:param refactoring_file_path: The path to the refactoring file
	:return: A tuple (bool, str) where the bool indicates if the file is valid, and the str provides a message.
	"""

	if not os.path.isfile(refactoring_file_path): # Verify if the file exists
		return False, "File does not exist." # Return False if the file does not exist
	
	try: # Try to load the JSON content of the file
		with open(refactoring_file_path, "r") as file: # Open the refactoring file
			data = json.load(file) # Load the JSON data
			if not data: # Verify if the data is empty
				return False, "File is empty." # Return False if the file is empty
	except json.JSONDecodeError: # Catch the JSONDecodeError exception
		return False, "File contains invalid JSON." # Return False if the file contains invalid JSON
	except Exception as e: # Catch any other exceptions
		return False, f"An unexpected error occurred: {str(e)}" # Handle any other unexpected errors
	
	return True, "File is valid." # Return True if the file is valid

def generate_refactoring_file(repository_name, commit_hash, refactoring_file_path):
	"""
	Generates the refactoring file for a specific commit hash in a specific repository.

	:param repository_name: The name of the repository
	:param commit_hash: The commit hash of the current linear regression
	:param refactoring_file_path: The path to the refactoring file
	:return: The refactoring file path
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Generating the refactoring file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	relatively_refactorings_directory_path = f"{RELATIVE_REFACTORINGS_DIRECTORY_PATH}/{repository_name}" # Get the relatively refactorings directory path
	full_refactorings_directory_path = f"{START_PATH}/{relatively_refactorings_directory_path}" # Get the full refactorings directory path
	create_directory(full_refactorings_directory_path, relatively_refactorings_directory_path) # Create the refactorings directory

	if not verify_filepath_exists(refactoring_file_path) or os.path.getsize(refactoring_file_path) == 0: # If the refactoring file does not exist or is empty
		null_device = "NUL" if platform.system() == "Windows" else "/dev/null" # Determine the system's null device to discard output

		setup_repository(repository_name, DEFAULT_REPOSITORIES[repository_name]) # Setup the repository
		
		command = f"{RELATIVE_REFACTORING_MINER_DIRECTORY_PATH} -c .{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/{repository_name} {commit_hash} -json {refactoring_file_path} >{null_device} 2>&1" # Run RefactoringMiner to get the refactoring data, hiding its output
		os.system(command) # Run the command to get the RefactoringMiner data

	is_valid, message = verify_refactoring_file(refactoring_file_path) # Verify if the refactoring file was properly generated

	if is_valid: # If the refactoring file was properly generated
		return refactoring_file_path # Return the refactoring file path
	else: # If the refactoring file was not properly generated
		print(f"{BackgroundColors.RED}The refactoring file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository was not generated: {BackgroundColors.YELLOW}{message}{Style.RESET_ALL}")
		return None # Return None

def process_refactorings(commit, class_name, refactorings_by_filepath):
	"""
	Process the refactorings from a commit and update the refactoring types by file path.

	:param commit: The commit data containing refactorings.
	:param class_name: The class name to search for in file paths.
	:param refactorings_by_filepath: The dictionary holding file paths and their corresponding refactoring types.
	:return: Updated refactorings_by_filepath dictionary.
	"""

	for refactoring in commit["refactorings"]: # Loop through the refactorings in the commit
		for location in refactoring["leftSideLocations"] + refactoring["rightSideLocations"]: # Combine and loop through both left and right side locations
			simplified_class_name = class_name.split("$")[0].replace(".", "/") # Simplify the class name and adapt it to the path format
			if simplified_class_name in location["filePath"]: # If the class name is in the file path
				if location["filePath"] not in refactorings_by_filepath: # If the file path is already in the dictionary, append the refactoring type to its list
					refactorings_by_filepath[location["filePath"]] = {} # Initialize the dictionary for the file path
				refactoring_type = refactoring["type"] # Get the refactoring type
				if refactoring_type not in refactorings_by_filepath[location["filePath"]]: # If the refactoring type is not in the dictionary, add it
					refactorings_by_filepath[location["filePath"]][refactoring_type] = 0 # Initialize the refactoring type counter
				refactorings_by_filepath[location["filePath"]][refactoring_type] += 1 # Increment the refactoring type counter
				verbose_output(true_string=f"Refactoring: {json.dumps(refactoring, indent=4)}") # Print the refactoring data

	return refactorings_by_filepath # Return the updated dictionary

def get_refactoring_info(repository_name, commit_number, commit_hash, class_name):
	"""
	Gets specific information about the refactorings of the commit hash and class name from RefactoringMiner.

	:param repository_name: The name of the repository
	:param commit_number: The commit number of the current linear regression
	:param commit_hash: The commit hash of the current linear regression
	:param class_name: The class name of the current linear regression
	:return: A dictionary containing the file paths and their corresponding refactoring types and occurrences
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the specific information about the refactorings for {BackgroundColors.CYAN}{class_name}{BackgroundColors.GREEN} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	refactoring_file_path = f"{FULL_REFACTORINGS_DIRECTORY_PATH}/{repository_name}/{commit_number}-{commit_hash}{REFACTORING_MINER_JSON_FILE_EXTENSION}" # Define the refactoring file path

	if not verify_filepath_exists(refactoring_file_path) or os.path.getsize(refactoring_file_path) == 0: # Generate the refactoring file if it does not exist or is empty
		generate_refactoring_file(repository_name, commit_hash, refactoring_file_path) # Generate the refactoring file

	refactorings_by_filepath = {} # Initialize the dictionary to hold file paths and their corresponding refactoring types

	with open(refactoring_file_path, "r") as file: # Open and read the refactoring file
		data = json.load(file) # Load the JSON data
		for commit in data["commits"]: # Loop through the refactorings in the data
			if commit["sha1"] == commit_hash: # Verify if the commit hash matches the specified one
				process_refactorings(commit, class_name, refactorings_by_filepath) # Process the refactorings for the commit

	return refactorings_by_filepath # Return the dictionary containing the file paths and their corresponding refactoring types and occurrences

def is_desired_refactoring(refactorings_info):
	"""
	Verifies if the refactoring is a desired refactoring.

	:param refactorings_info: A dictionary containing the file paths and their corresponding refactoring types and occurrences
	:return: True if the refactoring is a desired refactoring, False otherwise
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the refactoring is a desired refactoring...{Style.RESET_ALL}")

	for types in refactorings_info.values(): # For each refactoring type in the refactorings info
		if any(refactoring_type in types for refactoring_type in DESIRED_REFACTORINGS): # If any of the desired refactoring types are in the refactoring types
			return True # Return True if the refactoring is a desired refactoring

	return False # Return False if the refactoring is not a desired refactoring

def convert_refactorings_dictionary_to_string(refactorings_info):
	"""
	Converts the refactorings dictionary into a string.

	:param refactorings_info: A dictionary containing the file paths and their corresponding refactoring types and occurrences
	:return: A formatted string containing the refactorings information
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Formatting the refactorings summary...{Style.RESET_ALL}")

	# Converts the nested dictionary into a formatted string with the file paths and their corresponding refactoring types and occurrences
	refactorings_summary = " ".join(
		f"{filepath}: [{', '.join(f'{refactoring_type}({occurrences})' for refactoring_type, occurrences in sorted(types.items(), key=lambda item: item[1], reverse=True))}]"
		for filepath, types in refactorings_info.items()
    )

	return refactorings_summary # Return the formatted string containing the refactorings information

def find_biggest_decrease(metric_values, commit_hashes, repository_name, class_name):
	"""
	Finds the biggest change in metrics values and corresponding commit data.

	:param metric_values: A list of metrics values for the specified metric name
	:param commit_hashes: The list of commit hashes
	:param repository_name: The name of the repository
	:param class_name: The class name
	:return: The biggest change and the corresponding commit data
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Finding the biggest decrease in metrics values for the {BackgroundColors.CYAN}{class_name}{BackgroundColors.GREEN} class...{Style.RESET_ALL}")

	biggest_change_data = [0, 0, 0.00, ""] # [From, To, Percentual Variation, Refactorings Detected]
	commit_data = ["", "", "", "", ""] # [Biggest Change Position (i), From Commit Number, From Commit Hash, To Commit Number, To Commit Hash]

	for i in range(1, len(metric_values)): # For each metric value in the metric values list
		if metric_values[i] >= metric_values[i - 1] or metric_values[i - 1] == 0: # If the current metric value is greater than or equal to the previous metric value or the previous metric value is 0
			continue # Skip the current iteration

		current_percentual_variation = round((metric_values[i - 1] - metric_values[i]) / metric_values[i - 1], 3) # Calculate the current percentual variation

		if current_percentual_variation > DESIRED_DECREASE and current_percentual_variation > biggest_change_data[2]: # If the current percentual variation is greater than the desired decrease and the biggest change
			commit_data = extract_commit_data(commit_hashes, i) # Extract the commit data
			refactorings_info = get_refactoring_info(repository_name, commit_data[1], commit_data[2], class_name) # Get the refactoring info

			if not refactorings_info: # If the refactorings info is empty
				continue # Skip the current iteration

			if (DESIRED_REFACTORINGS_ONLY and is_desired_refactoring(refactorings_info)) or not DESIRED_REFACTORINGS_ONLY: # If the refactoring is a desired refactoring
				refactorings_summary = convert_refactorings_dictionary_to_string(refactorings_info) # Convert the refactorings dictionary to a string
				biggest_change_data = [metric_values[i - 1], metric_values[i], current_percentual_variation, refactorings_summary.replace("'", "")] # Update the biggest change

	return biggest_change_data, commit_data # Return the biggest change and the corresponding commit data

def add_substantial_decrease_to_csv(csv_filename, class_name, raw_variable_attribute, biggest_change_data, commit_data, record):
	"""
	Writes the substantial decrease to the CSV file.

	:param csv_filename: The name of the csv file
	:param class_name: The class name
	:param raw_variable_attribute: The raw variable attribute (class type or method name)
	:param biggest_change_data: The information of the biggest change in the metrics 
	:param commit_data: The commit data
	:param record: The record containing additional information for writing
	:return: None
	"""

	with open(f"{csv_filename}", "a") as csvfile: # Open the csv file
		writer = csv.writer(csvfile) # Create the csv writer
		index = commit_data[0] # Get the metric position
		writer.writerow([class_name, raw_variable_attribute] + [biggest_change_data[2]] + [round(biggest_change_data[2] * 100, 2)] + [f"{commit_data[1]} -> {commit_data[3]}", f"{commit_data[2]} -> {commit_data[4]}", record["code_churns"][index], record["lines_added"][index], record["lines_deleted"][index], record["modified_files_count"][index]] + list(record["metrics"][index]) + [record["methods_invoked"], biggest_change_data[3]]) # Write the row to the csv file

def verify_substantial_metric_decrease(repository_name, class_name, raw_variable_attribute, record, metric_name, metric_position, iteration):
	"""
	Verifies if the class or method has had a substantial decrease in the current metric, and writes the relevant data, including code churn, lines added, and lines deleted, to the CSV file.

	:param repository_name: The name of the repository
	:param class_name: The class name of the current linear regression
	:param raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
	:param record: A dictionary containing commit information and metric history
	:param metric_name: The name of the metric
	:param metric_position: The position of the metric in the metrics list
	:param iteration: A integer representing the current iteration number. If its the first iteration, it will be 1, otherwise it will be greater.
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the class or method has had a substantial decrease in the {BackgroundColors.CYAN}{metric_name}{BackgroundColors.GREEN} metric...{Style.RESET_ALL}")

	if not len(record["metrics"]): # If the metrics values list is empty
		return # If the metrics values list is empty, return

	if found_ignore_keywords(class_name, IGNORE_CLASS_NAME_KEYWORDS, "class") or found_ignore_keywords(raw_variable_attribute, IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS, "variable attribute"): # If the class name or variable attribute contains ignore keywords,
		return # If the class name or variable attribute contains ignore keywords, return
	
	csv_filename = setup_substantial_decrease_file(repository_name, metric_name, iteration) # Setup the substantial decrease file for the specified repository and metric name

	biggest_change_data, commit_data = find_biggest_decrease([metric[metric_position] for metric in record["metrics"]], record["commit_hashes"], repository_name, class_name) # Find the biggest decrease in metrics values and corresponding commit data

	if biggest_change_data[2] > DESIRED_DECREASE and biggest_change_data[3]: # If the biggest change percentual variation is bigger than the desired decrease and the refactorings summary is not empty
		add_substantial_decrease_to_csv(csv_filename, class_name, raw_variable_attribute, biggest_change_data, commit_data, record) # Write the substantial decrease to the CSV file

def setup_substantial_metric_decrease_for_each_metric(repository_name, class_name, variable_attribute, record, iteration):
	"""
	Verifies if there has been a substantial decrease in the metrics for each metric.

	:param repository_name: The name of the repository being analyzed
	:param class_name: The name of the class being analyzed
	:param variable_attribute: The method or attribute of the class being analyzed
	:param record: A dictionary containing commit information and metric history
	:param iteration: The current iteration of the analysis
	:return: None
	"""

	if len(record["metrics"]): # If the metrics list is not empty
		for metric_name, metric_position in METRICS_INDEXES.items(): # If the metric name is not in the keys of the METRICS_INDEXES dictionary
			verify_substantial_metric_decrease(repository_name, class_name, variable_attribute, record, metric_name, metric_position, iteration) # Verify if there has been a substantial decrease in the metrics

def convert_metrics_to_array(class_name, variable_attribute, metrics):
	"""
	Convert the metrics list to a NumPy array.

	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param metrics: A list containing the metrics values for linear regression
	:return: A NumPy array containing the metrics values
	"""

	try: # Try to convert the metrics list to a NumPy array
		return np.array(metrics, dtype=float) # Convert the metrics list to a NumPy array
	except Exception: # Catch any exceptions
		verbose_output(true_string=f"{BackgroundColors.RED}Error converting the {BackgroundColors.CYAN}metrics{BackgroundColors.GREEN} to {BackgroundColors.CYAN}NumPy array{BackgroundColors.GREEN} for {class_name} {variable_attribute}.{Style.RESET_ALL}")
		return None # Return None if an exception occurs

def validate_metrics_structure(class_name, variable_attribute, metrics_array):
	"""
	Validate if the metrics array has the correct structure.
	
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param metrics_array: A NumPy array containing the metrics values
	:return: True if the metrics structure is as expected, False otherwise
	"""

	if metrics_array.ndim != 2 or metrics_array.shape[1] < len(METRICS_INDEXES): # If the metrics array dimensions are not 2 (commit metrics and metrics) or the number of columns is less than the number of metrics
		verbose_output(true_string=f"{BackgroundColors.RED}Metrics structure for {class_name} {variable_attribute} is not as expected!{Style.RESET_ALL}")
		return False # Return False if the metrics structure is not as expected
	return True # Return True if the metrics structure is as expected

def extract_column_values_from_array(array, column_position):
	"""
	Extract the 

	:param array: A NumPy array containing the metrics values
	:param column_position: The position of the column to extract the metric values
	:return: A list containing the values of the specified column
	"""

	return array[:, column_position] # Return the values of the specified column

def has_sufficient_data(commit_number, metric_values):
	"""
	Verify if there are enough data points for linear regression.

	:param commit_number: A NumPy array containing the commit numbers
	:param metric_values: A NumPy array containing the metric values
	:return: True if there are enough data points for linear regression, False otherwise
	"""

	if len(commit_number) < 2 or len(metric_values) < 2: # If there are less than 2 data points for linear regression
		return False # Return False if there are less than 2 data points for linear regression
	return True # Return True if there are enough data points for linear regression

def perform_linear_regression(commit_number, metric_values):
	"""
	Perform linear regression and return the predicted linear fit.

	:param commit_number: A NumPy array containing the commit numbers
	:param metric_values: A NumPy array containing the metric values
	:return: A NumPy array containing the predicted linear fit
	"""

	model = LinearRegression() # Create a Linear Regression model
	model.fit(commit_number.reshape(-1, 1), metric_values) # Fit the model to the data
	return model.predict(commit_number.reshape(-1, 1)) # Return the predicted linear fit

def plot_and_save_graph(repository_name, class_name, variable_attribute, commit_number, metric_values, metric_name, linear_fit):
	"""
	Create the linear regression plot and save it as a PNG file.

	:param repository_name: The name of the repository
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param commit_number: A NumPy array containing the commit numbers
	:param metric_values: A NumPy array containing the metric values
	:param metric_name: The name of the metric
	:param linear_fit: A NumPy array containing the predicted linear fit
	:return: None
	"""

	plt.figure(figsize=(10, 6)) # Set the figure size
	plt.plot(commit_number, metric_values, "o", label=f"{metric_name}") # Plot the metric values
	plt.plot(commit_number, linear_fit, "-", label="Linear Regression Fit") # Plot the linear regression fit
	plt.xlabel("Commit Number") # Set the x-axis label
	plt.ylabel(f"{metric_name} Value") # Set the y-axis label
	plt.title(f"Linear Regression for {metric_name} metric of {class_name} {variable_attribute}") # Set the title
	plt.legend() # Add the legend

	relative_metrics_prediction_directory_path = f"{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}"
	full_metrics_prediction_directory_path = f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}"

	create_directory(full_metrics_prediction_directory_path, relative_metrics_prediction_directory_path) # Create the directory where the plot will be stored

	plt.savefig(f"{full_metrics_prediction_directory_path}/{metric_name}{PNG_FILE_EXTENSION}")
	plt.close() # Close the plot

def setup_linear_regression_plots(repository_name, class_name, variable_attribute, record):
	"""
	Setup and, if with valid metrics, perform linear regression on the given metrics and save the plot to a PNG file.
	
	:param repository_name: The name of the repository
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param record: A dictionary containing commit information and metric history
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Performing linear regression on the given metrics and saving the plot to a PNG file for {BackgroundColors.CYAN}{class_name}{BackgroundColors.GREEN} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	metrics_array = convert_metrics_to_array(class_name, variable_attribute, record["metrics"]) # Convert the metrics list to a NumPy array

	if metrics_array is None or not validate_metrics_structure(class_name, variable_attribute, metrics_array): # If the metrics array is None or the metrics structure is not valid,
		return # Return if the metrics array is None or the metrics structure is not valid

	for metric_name, metric_position in METRICS_INDEXES.items(): # For each metric name and position in the METRICS_INDEXES dictionary
		commit_numbers = np.arange(1, len(record["commit_hashes"]) + 1) # Generate an array of commit numbers
		metric_values = extract_column_values_from_array(metrics_array, metric_position) # Extract the metric values from the array for the given metric position

		if not commit_numbers.any() or not has_sufficient_data(commit_numbers, metric_values): # If the commit number array is empty or there are not enough data points for linear regression
			continue # Jump to the next iteration of the loop

		linear_fit = perform_linear_regression(commit_numbers, metric_values) # Perform linear regression and get the predicted linear fit
		plot_and_save_graph(repository_name, class_name, variable_attribute, commit_numbers, metric_values, metric_name, linear_fit) # Create the linear regression plot and save it as a PNG file

def add_metrics_statistics_csv_header(csv_filename):
	"""
	Adds the header to the metrics statistics CSV file.

	:param csv_filename: The name of the csv file
	:return: None
	"""

	expected_header = [] # The expected header list
	if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
		expected_header = ["Class", "Type", "Changed", "Churn Min", "Churn Max", "Churn Avg", "Churn Q3", "Modified Files Min", "Modified Files Max", "Modified Files Avg", "Modified Files Q3"] + generate_metric_headers() + ["First Commit Hash", "Last Commit Hash", "Method Invocations"] # The expected header list
	else: # If the PROCESS_CLASSES constant is set to False
		expected_header = ["Class", "Method", "Changed", "Churn Min", "Churn Max", "Churn Avg", "Churn Q3", "Modified Files Min", "Modified Files Max", "Modified Files Avg", "Modified Files Q3"] + generate_metric_headers() + ["First Commit Hash", "Last Commit Hash", "Methods Invoked Qty"] # The expected header list

	with open(csv_filename, "w") as csvfile: # Open the csv file in write mode
		writer = csv.writer(csvfile) # Create the csv writer
		writer.writerow(expected_header) # Write the expected header to the csv file

def generate_metric_headers():
	"""
	Generates the headers for the metrics statistics.

	:return: A list containing the headers for the metrics statistics
	"""

	return [f"{metric} {stat}" for metric in METRICS_INDEXES for stat in ["Min", "Max", "Avg", "Q3"]]

def calculate_metric_statistics(metric_values):
	"""
	Calculates the min, max, avg, and Q3 for a given list of metric values.

	:param metric_values: List of metric values
	:return: A tuple containing (min, max, avg, Q3) rounded to 3 decimal places
	"""

	if not metric_values: # If the list is empty
		return (0, 0, 0, 0) # Return zeros if the list is empty

	metric_min = round(float(min(metric_values)), 3) # The minimum metric value rounded to 3 decimal places
	metric_max = round(float(max(metric_values)), 3) # The maximum metric value rounded to 3 decimal places
	metric_avg = round(float(sum(metric_values)) / len(metric_values), 3) # The average metric value rounded to 3 decimal places
	metric_q3 = round(float(np.percentile(metric_values, 75)), 3) # The third quartile metric value rounded to 3 decimal places

	return metric_min, metric_max, metric_avg, metric_q3 # Return the metric statistics

def write_method_metrics_statistics(csv_writer, id, key, record, first_commit_hash, last_commit_hash):
	"""
	Calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file.

	:param csv_writer: The csv writer object
	:param id: The id of the class/method
	:param key: The key of the class/method
	:param record: A dictionary containing commit information and metric history
	:param first_commit_hash: The first commit hash of the class/method
	:param last_commit_hash: The last commit hash of the class/method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating statistics for class/method {BackgroundColors.CYAN}{id}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

	ck_metrics_stats_tuples = [calculate_metric_statistics([record["metrics"][i][metric_position] for i in range(len(record["metrics"]))]) for metric_position in METRICS_INDEXES.values()] # Calculate statistics for all defined metrics
	flat_ck_metrics_stats = [stat for ck_metrics_stat in ck_metrics_stats_tuples for stat in ck_metrics_stat] # Flatten the list of tuples

	churn_stats = calculate_metric_statistics(record["code_churns"]) # Calculate statistics for code churn
	modified_files_stats = calculate_metric_statistics(record["modified_files_count"]) # Calculate statistics for modified files

	csv_writer.writerow([id, key, record["changed"], *churn_stats, *modified_files_stats, *flat_ck_metrics_stats, first_commit_hash, last_commit_hash, record["methods_invoked"]]) # Write the metrics statistics to the csv file

def add_metrics_track_record_statistics(repository_name, class_name, variable_attribute, record, filename):
	"""
	Processes the metrics in metrics_track_record to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file.

	:param repository_name: The name of the repository
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param record: A dictionary containing commit information and metric history
	:param filename: The name of the csv file
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the metrics in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to calculate the minimum, maximum, average, and third quartile of each metric and writing it to a csv file...{Style.RESET_ALL}")
	
	with open(filename, "a") as csvfile: # Open the csv file in write mode
		writer = csv.writer(csvfile) # Create the csv writer
		write_method_metrics_statistics(writer, class_name, variable_attribute, record, record["commit_hashes"][0], record["commit_hashes"][-1]) # Write the metrics statistics to the csv file

def setup_write_metrics_statistics_to_csv(repository_name, class_name, variable_attribute, record, iteration):
	"""
	Setup the writing of the metrics statistics to a CSV file.

	:param repository_name: The name of the repository
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param record: A dictionary containing commit information and metric history
	:param iteration: The current iteration of the analysis
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Setting up the writing of the metrics statistics to a CSV file for {BackgroundColors.CYAN}{class_name}{BackgroundColors.GREEN} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

	unsorted_metrics_filename = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}" # The unsorted metrics filename

	if verify_filepath_exists(unsorted_metrics_filename) and iteration == 1: # If the unsorted metrics filename exists and it is the first iteration
		add_metrics_statistics_csv_header(unsorted_metrics_filename) # Add the metrics statistics csv header

	if record["changed"] >= MINIMUM_CHANGES: # If the number of changes is greater than or equal to the minimum changes
		add_metrics_track_record_statistics(repository_name, class_name, variable_attribute, record, unsorted_metrics_filename) # Generate the metrics track record statistics

def process_metrics_track_record(repository_name, metrics_track_record):
	"""
	Processes the metrics track record to generate outputs such as linear regression graphics, metrics evolution data, and verification of substantial metric decreases.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the Metrics Track Record Dictionary for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

	progress_description = generate_progress_bar_description() # Generate the description for the progress bar
	with tqdm(total=len(metrics_track_record), unit=f" {progress_description}") as progress_bar: # For every identifier in the metrics_track_record, process the metrics
		for iteration, (identifier, record) in enumerate(metrics_track_record.items(), start=1): # For each identifier and record in the metrics_track_record dictionary
			metrics = record["metrics"] # Get the metrics list
			class_name = identifier.split(" ")[0] # Get the identifier which is currently the class name
			variable_attribute = get_clean_id(identifier.split(" ")[1]) # Get the variable attribute which could be the type of the class or the method name

			if metrics: # If the metrics list is not empty
				setup_write_metrics_track_record_to_txt(repository_name, identifier, record, iteration) if RUN_FUNCTIONS["Metrics Track Record"] else None # Setup the writing of the metrics track record to a txt file
				setup_write_metrics_evolution_to_csv(repository_name, class_name, variable_attribute, record) if RUN_FUNCTIONS["Metrics Evolution"] else None # Setup the writing of the metrics evolution to a CSV file
				setup_substantial_metric_decrease_for_each_metric(repository_name, class_name, variable_attribute, record, iteration) if RUN_FUNCTIONS["Metrics Decrease"] else None # Verify if substantial decrease
				setup_linear_regression_plots(repository_name, class_name, variable_attribute, record) if RUN_FUNCTIONS["Linear Regression"] else None # Generate linear regression graphics
				setup_write_metrics_statistics_to_csv(repository_name, class_name, variable_attribute, record, iteration) if RUN_FUNCTIONS["Metrics Statistics"] else None # Setup the writing of the metrics statistics to a CSV file
			
			progress_bar.update(1) # Update the progress bar

def sort_csv_by_changes(repository_name):
	"""
	Sorts the csv file according to the number of changes.

	:param repository_name: The name of the repository
	:return: None
	"""
	
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}metrics statistics files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}number of changes{BackgroundColors.GREEN}.{Style.RESET_ALL}")

	unsorted_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}" # The unsorted csv file path

	if not verify_filepath_exists(unsorted_csv_file_path): # Verify if the unsorted csv file exists
		verbose_output(true_string=f"{BackgroundColors.RED}The unsorted csv file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository does not exist.{Style.RESET_ALL}")
		return # Return if the unsorted csv file does not exist

	data = pd.read_csv(unsorted_csv_file_path) # Read the csv file
	
	if data.empty: # Verify if the DataFrame is empty after the header
		verbose_output(true_string=f"{BackgroundColors.RED}The unsorted csv file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository is empty after the header.{Style.RESET_ALL}")
		return # Return if the file is empty after the header
	
	data = data.sort_values(by=["changed"], ascending=False) # Sort the csv file by the number of changes
	
	sorted_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SORTED_CHANGED_METHODS_CSV_FILENAME}" # The sorted csv file path
	
	data.to_csv(sorted_csv_file_path, index=False) # Write the sorted csv file to a new csv file

def sort_csv_by_percentual_variation(repository_name):
	"""
	Sorts the csv files according to the percentual variation of the metric.

	:param repository_name: The name of the repository
	:return: None
	"""
	
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}interesting changes files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}percentual variation of the metric{BackgroundColors.GREEN}.{Style.RESET_ALL}")

	for metric_name in METRICS_INDEXES.keys(): # For each metric name in the METRICS_INDEXES dictionary
		data = pd.read_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME.replace('METRIC_NAME', metric_name)}") # Read the csv file
		data = data.sort_values(by=[f"Percentual Variation {metric_name}"], ascending=False) # Sort the csv file by the percentual variation of the metric
		data.to_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME.replace('METRIC_NAME', metric_name)}", index=False) # Write the sorted csv file to a new csv file

def read_csv_as_dict(file_path):
	"""
	Reads the CSV file into a dictionary format where the key is the repository name.
	
	:param file_path: Path to the CSV file
	:return: Dictionary containing repository data
	"""

	repository_data = {} # Initialize the dictionary to hold the repository data
	if verify_filepath_exists(file_path): # If the file path exists
		with open(file_path, "r", newline="") as csv_file: # Open the CSV file
			reader = csv.DictReader(csv_file) # Create the CSV reader
			for row in reader: # For each row in the CSV file
				repository_name = row["Repository Name"] # Get the repository name
				repository_data[repository_name] = { # Add the repository data to the dictionary
					"classes": int(row["Number of Classes"]), # Convert the number of classes to an integer
					"lines_of_code": int(row["Lines of Code (LOC)"]), # Convert the lines of code to an integer
					"commits": int(row["Number of Commits"]), # Convert the number of commits to an integer
					"execution_time_in_minutes": float(row["Execution Time (Minutes)"]), # Convert the execution time to a float
					"size_in_gb": float(row["Size (GB)"]) # Convert the size to a float
				}
	else: # If the file path does not exist
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{file_path}{BackgroundColors.RED} file does not exist.{Style.RESET_ALL}")
		repository_data = {} # Reset the repository data if the file does not exist

	return repository_data # Return the dictionary containing the repository data

def write_dict_to_csv(file_path, repositories_attributes):
	"""
	Writes the dictionary data back into the CSV file.
	
	:param file_path: Path to the CSV file
	:param repositories_attributes: Dictionary containing repositories attributes
	"""

	with open(file_path, "w", newline="") as csv_file: # Open the CSV file
		writer = csv.writer(csv_file) # Create the CSV writer
		writer.writerow(["Repository Name", "Number of Classes", "Lines of Code (LOC)", "Number of Commits", "Execution Time (Minutes)", "Size (GB)"]) # Write the header to the CSV file
		for repository_name, attributes in repositories_attributes.items(): # For each repository name and attributes in the data dictionary
			writer.writerow([ # Write the repository name and attributes to the CSV file
				repository_name, # Repository name
				attributes["classes"], # Number of classes
				attributes["lines_of_code"], # Lines of code (LOC)
				attributes["commits"], # Number of commits
				attributes["execution_time_in_minutes"], # Execution time in minutes
				round(attributes["size_in_gb"], 2) # Size in GB
			])

def update_repository_attributes(repository_name, elapsed_time):
	"""
	Updates the attributes for a specific repository.
	
	:param repository_name: Name of the repository to update
	:param elapsed_time: Additional elapsed time in seconds

	:return: Updated repository attributes
	"""

	repositories_attributes = read_csv_as_dict(FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH) # Read the existing CSV data

	if repository_name in repositories_attributes: # Update the attributes for the specified repository
		repositories_attributes[repository_name]["execution_time_in_minutes"] = round(repositories_attributes[repository_name]["execution_time_in_minutes"] + elapsed_time / 60, 2) # Update the execution time in minutes
		repositories_attributes[repository_name]["size_in_gb"] += get_directories_size_in_gb(repository_name, OUTPUT_DIRECTORIES) # Update the size in GB
	else: # If the repository was not found in the repositories attributes file
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository was not found in the {BackgroundColors.CYAN}repositories attributes{BackgroundColors.RED} file.{Style.RESET_ALL}")
		return # Return if the repository was not found in the repositories attributes file

	return repositories_attributes # Return the updated repositories attributes

def process_repository(repository_name, repository_url):
	"""
	Processes the specified repository.

	:param repository_name: The name of the repository to be analyzed
	:param repository_url: The URL of the repository to be analyzed
	:return: None
	"""

	start_time = time.time() # Start the timer

	number_of_commits = sum(1 for _ in Repository(repository_url).traverse_commits()) # Get the number of commits for the specified repository
	setup_process_repository(repository_name, repository_url, number_of_commits) # Setup to process the repository to caculate missing data (CK Metris)
	
	repository_ck_metrics_path = get_directory_path(repository_name) # Get the directory path for the specified repository name
	
	create_directories(repository_name) # Create the desired directory if it does not exist

	metrics_track_record = traverse_directory(repository_name, repository_ck_metrics_path) # Traverse the directory and get the classes/methods metrics

	sorted_metrics_track_record = sort_commit_hashes_by_commit_number(metrics_track_record) # Sort the commit_hashes list for each entry in the metrics_track_record dictionary by the commit number

	process_metrics_track_record(repository_name, sorted_metrics_track_record) # Process the metrics track record to generate outputs such as linear regression graphics, metrics evolution data, and verification of substantial metric decreases

	sort_csv_by_changes(repository_name) # Sort the csv file by the number of changes

	old_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}" # The old csv file path
	os.remove(old_csv_file_path) # Remove the old csv file

	sort_csv_by_percentual_variation(repository_name) if RUN_FUNCTIONS["Sort by Percentual Variation"] else None # Sort the interesting changes csv file by the percentual variation of the metric

	repositories_attributes = update_repository_attributes(repository_name, time.time() - start_time) # Update the attributes of the repositories file with the elapsed time and output data size in GB
	write_dict_to_csv(FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH, repositories_attributes) # Write the updated data back to the CSV file

	elapsed_time = time.time() - start_time # Calculate the elapsed time
	elapsed_time_string = f"Time taken to generate the {BackgroundColors.CYAN}metrics evolution records, metrics statistics and linear regression{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS.capitalize()}{BackgroundColors.GREEN} in {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
	output_time(elapsed_time_string, round(elapsed_time, 2)) # Output the elapsed time

def process_all_repositories():
	"""
	Processes all the repositories in the DEFAULT_REPOSITORIES dictionary.

	:return: None
	"""

	for repository_name, repository_url in DEFAULT_REPOSITORIES.items(): # Loop through the DEFAULT_REPOSITORIES dictionary
		print(f"") # Print an empty line
		print(f"{BackgroundColors.GREEN}Processing the {BackgroundColors.CYAN}{', '.join([key.title() for key in sorted(RUN_FUNCTIONS.keys())])}{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS.capitalize()}{BackgroundColors.GREEN} from the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
		process_repository(repository_name, repository_url) # Process the current repository
		print(f"\n------------------------------------------------------------") # Print a separator

atexit.register(play_sound) # Register the function to play a sound when the program finishes

def main():
	"""
   Main function.

   :return: None
   """

	start_time = datetime.now() # Get the start time
   
	if path_contains_whitespaces(): # Verify if the path constants contains whitespaces
		print(f"{BackgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
		return # Exit the program
	
	global SOUND_FILE_PATH # Declare the SOUND_FILE_PATH as a global variable
	SOUND_FILE_PATH = update_sound_file_path() # Update the sound file path

	if not verify_filepath_exists(RELATIVE_REFACTORING_MINER_DIRECTORY_PATH): # Verify if the refactoring miner tool exists in the specified path
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}RefactoringMiner{BackgroundColors.RED} tool was not found in the specified path: {BackgroundColors.GREEN}{RELATIVE_REFACTORING_MINER_DIRECTORY_PATH}{Style.RESET_ALL}")
		return # Exit the program
        
	verify_repositories_execution_constants() # Verify the repositories execution constants

	# Print the Welcome Messages
	print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Metrics Changes Generator{BackgroundColors.GREEN}! This script is part of the {BackgroundColors.CYAN}Worked Example Miner (WEM){BackgroundColors.GREEN} project.{Style.RESET_ALL}")
	print(f"{BackgroundColors.GREEN}This script generates the {BackgroundColors.CYAN}Classes and/or Methods {', '.join([key.title() for key in sorted(RUN_FUNCTIONS.keys())])}{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{', '.join(repo.title() for repo in DEFAULT_REPOSITORIES.keys())}{BackgroundColors.GREEN} repositories based on the {BackgroundColors.CYAN}ck metrics files, the commit hashes list file and the diffs of each commit{BackgroundColors.GREEN} generated by the {BackgroundColors.CYAN}./code_metrics.py{BackgroundColors.GREEN} code.{Style.RESET_ALL}")
	print(f"{BackgroundColors.RED}This Python code avoids using threads due to its high memory usage. It stores Metrics Values, Generates Linear Regression Graphs, and Detects Metrics Decreases B, which demands a lot of RAM.{Style.RESET_ALL}\n")

	user_response = input_with_timeout(f"{BackgroundColors.GREEN}Do you want to process the {BackgroundColors.CYAN}class.csv{BackgroundColors.GREEN} file {BackgroundColors.RED}(True/False){BackgroundColors.GREEN}? {Style.RESET_ALL}", 60) # Prompt the user with a timeout
	
	if user_response is None: # No input received within timeout
		print(f"{BackgroundColors.RED}No input received within the timeout. Processing both classes and methods.{Style.RESET_ALL}")
		process_classes_and_methods() # Process both classes and methods
	else: # Input received within timeout
		process_based_on_user_input(user_response) # Process based on user input

	end_time = datetime.now() # Get the end time
	output_time(f"\n{BackgroundColors.GREEN}Total execution time: ", (end_time - start_time).total_seconds()) # Output the total execution time

	print(f"\n{BackgroundColors.GREEN}The {BackgroundColors.CYAN}Metrics Changes Generator{BackgroundColors.GREEN} has finished processing the {BackgroundColors.CYAN}classes or methods metrics evolution history, metrics statistics and linear regression, substantial changes and refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{', '.join(repo.capitalize() for repo in DEFAULT_REPOSITORIES.keys())}{BackgroundColors.GREEN} repositories.{Style.RESET_ALL}") # Output the message that the Metrics Changes Generator has finished
		
if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
