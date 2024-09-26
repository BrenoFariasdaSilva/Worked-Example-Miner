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
from repositories_picker import DEFAULT_REPOSITORIES, PROCESS_JSON_REPOSITORIES, RELATIVE_REPOSITORIES_DIRECTORY_PATH, SOUND_FILE_PATH, START_PATH # Importing Constants from the repositories_picker.py file
from repositories_picker import create_directory, output_time, path_contains_whitespaces, play_sound, setup_repository, update_repositories_dictionary, update_sound_file_path, verbose_output, verify_filepath_exists # Importing Functions from the repositories_picker.py file

# Imports from the code_metrics.py file
from code_metrics import CK_METRICS_FILES, CSV_FILE_EXTENSION, FULL_CK_METRICS_DIRECTORY_PATH, FULL_REFACTORINGS_DIRECTORY_PATH, FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH, RELATIVE_REFACTORINGS_DIRECTORY_PATH # Importing Constants from the code_metrics.py file
from code_metrics import get_output_directories_size_in_gb, verify_ck_metrics_directory # Importing Functions from the code_metrics.py file

# Default values that can be changed:
VERBOSE = False # If True, then the program will output the progress of the execution
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 3 # The number of metrics
DESIRED_DECREASE = 0.00 # The desired decrease in the metric
IGNORE_CLASS_NAME_KEYWORDS = ["test"] # The keywords to ignore in the class name
IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS = ["anonymous"] # The keywords to ignore in the variable attribute
SUBSTANTIAL_CHANGE_METRICS = ["CBO"] # The desired metrics to search for substantial changes
METRICS_POSITION = {"CBO": 0, "WMC": 1, "RFC": 2} # The position of the metrics in the metrics list
DESIRED_REFACTORINGS_ONLY = False # If True, then only the desired refactorings will be stored
DESIRED_REFACTORINGS = ["Extract Method", "Extract Class", "Pull Up Method", "Push Down Method", "Extract Superclass", "Move Method"] # The desired refactorings to search for substantial changes
WRITE_FULL_HISTORY = False # If True, then the metrics evolution will store all of the metrics history and not only the moments the metrics changed between commits

RUN_FUNCTIONS = { # Dictionary with the functions to run and their respective booleans
	"generate_metrics_track_record_statistics": True, # Generate the metrics track record statistics
	"linear_regression_graphics": True, # Run the linear regression graphics
	"sort_csv_by_percentual_variation": True, # Sort the csv file by the percentual variation
	"verify_substantial_metric_decrease": True, # Verify the substantial metric decrease
	"write_metrics_evolution_to_csv": True, # Write the metrics evolution to a csv file
	"write_metrics_track_record_to_txt": True, # Write the metrics track record to a txt file
}

# Constants:
PROCESS_CLASSES = True # If True, then the classes will be processed, otherwise the methods will be processed
FIRST_SUBSTANTIAL_CHANGE_VERIFICATION = True # If True, then it is the first run of the program

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

def verify_repositories_execution_constants():
   """
   Verify the constants used in the execution of the repositories.
   It will process the JSON repositories, if the PROCESS_JSON_REPOSITORIES constant is set to True or if the DEFAULT_REPOSITORIES dictionary is empty.
   
   :return: None
   """

   if PROCESS_JSON_REPOSITORIES or not DEFAULT_REPOSITORIES: # Verify if PROCESS_REPOSITORIES_LIST is set to True or if the DEFAULT_REPOSITORIES dictionary is empty
      if not update_repositories_dictionary(): # Update the repositories list
         print(f"{BackgroundColors.RED}The repositories list could not be updated. Please execute the {BackgroundColors.CYAN}repositories_picker.py{BackgroundColors.RED} script or manually fill the {BackgroundColors.CYAN}DEFAULT_REPOSITORIES{BackgroundColors.RED} dictionary.{Style.RESET_ALL}")
         exit() # Exit the program if the repositories list could not be updated

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

def generate_commit_modified_files_dict(repository_name):
	"""
	Generates a dictionary of the modified files path list for each commit.

	:param repository_name: The name of the repository
	:return: A dictionary containing the modified files paths list for each commit
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Generating the commit dictionary for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

	commit_modified_files_dict = {} # A dictionary containing the commit hashes as keys and the modified files path list as values

	for commit in Repository(DEFAULT_REPOSITORIES[repository_name]).traverse_commits(): # Traverse the repository and get the modified files for each commit and store it in the commit_modified_files_dict
		commit_modified_files_dict[commit.hash] = [] # Initialize the commit hash list
		for modified_file in commit.modified_files: # For each modified file in the commit
			commit_modified_files_dict[commit.hash].append(modified_file.new_path) # Append the modified file path to the commit diff d

	return commit_modified_files_dict # Return the commit dictionary containing the modified files paths for each commit

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

def convert_ck_filepath_to_diff_filepath(ck_file_path, repository_file_path):
	"""
	Converts the CK file path to the diff file path.

	:param ck_file_path: The CK file path
	:param repository_file_path: The repository file path
	:return: The diff file path
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Converting the CK file path to the diff file path...{Style.RESET_ALL}")
	
	diff_file_path = ck_file_path.replace("ck_metrics", "diffs") # Replace the ck_metrics with diffs in the file path
	diff_file_path = diff_file_path[:diff_file_path.rfind("/")] # Get the substring path before the last slash (excluding the last slash)
	class_file_path = repository_file_path[repository_file_path.rfind("/") + 1:] # Merge the diff_file_path with the file name
	diff_file_path = f"{diff_file_path}/{class_file_path}.diff" # Merge the diff_file_path with the file name and the .diff extension

	return diff_file_path # Return the diff file path

def get_identifier_and_metrics(row):
	"""
	Gets the identifier and metrics of the class or method.

	:param row: The row of the csv file
	:return: The identifier, metrics and method_invoked of the class or method
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the identifier and metrics of the class or method...{Style.RESET_ALL}")
	
	class_name = row["class"] # Get the class name from the row
	if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
		if not valid_class_name(class_name): # If the class name is not valid (it is not a package name)
			class_name = get_class_package_name(row["file"]) # Get the package name of the class
		variable_attribute = row["type"] # Get the type of the class
	else: # If the PROCESS_CLASSES constant is set to False
		variable_attribute = row["method"] # Get the method name from the row

	cbo = float(row["cbo"]) # Get the cbo metric from the row as a float
	wmc = float(row["wmc"]) # Get the wmc metric from the row as a float
	rfc = float(row["rfc"]) # Get the rfc metric from the row as a float
	method_invoked = row["methodInvocations"] if PROCESS_CLASSES else int(row["methodsInvokedQty"]) # Get the methodInvocations (str) or methodsInvokedQty (int) from the row

	metrics = (cbo, wmc, rfc) # Create a tuple containing the metrics
	identifier = f"{class_name} {variable_attribute}" # The identifier of the class or method

	return identifier, metrics, method_invoked # Return the identifier, metrics and method_invoked of the class or method

def was_file_modified(commit_modified_files_dict, commit_hash, row):
	"""
	Verifies if the file was modified.

	:param commit_modified_files_dict: A dictionary containing the commit hashes as keys and the modified files paths list as values
	:param commit_hash: The commit hash of the current row
	:param row: The row of the csv file
	:return: True if the file was modified, False otherwise
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the file was modified...{Style.RESET_ALL}")

	modified_files_paths = commit_modified_files_dict[commit_hash] # Get the modified files list for the specified commit hash

	if not modified_files_paths: # If the modified files paths list is empty
		return False # Return False
	
	file_path = row["file"] # Get the file path from the row

	path_index = file_path.find(RELATIVE_REPOSITORIES_DIRECTORY_PATH) # Calculate the file path starting after the specified directory

	if path_index != -1: # If the path index is not -1
		file_path = file_path[path_index + len(RELATIVE_REPOSITORIES_DIRECTORY_PATH) + 1:] # Get the file path starting after the specified directory
	
	repository_name = file_path.split("/")[0] # Get the repository name
	file_path = file_path[len(repository_name) + 1:] # Get the file path starting after the repository name

	for modified_file_path in modified_files_paths: # Iterate through the modified files paths
		if modified_file_path == file_path: # If the modified file path is equal to the file path, then the file was modified
			return True # The file was modified
	return False # The file was not modified

def convert_ck_classname_to_filename_format(ck_classname):
	"""
	Convert CK classname format (e.g., com.houarizegai.calculator.Calculator$Anonymous14)
	to the filename format used by code churn (e.g., com/houarizegai/calculator/Calculator$14).
	
	:param ck_classname: The classname from the CK tool (e.g., com.houarizegai.calculator.Calculator$Anonymous14).
	:return: The converted classname in filename format (e.g., com/houarizegai/calculator/Calculator$14).
	"""
	
	package_path = ck_classname.rsplit(".", 1)[0].replace(".", "/") # Replace dots with slashes except for the class and anonymous part
	
	class_part = ck_classname.rsplit(".", 1)[-1] # Get the class and anonymous part (e.g., Calculator$Anonymous14)
	
	if "Anonymous" in class_part: # If it's an anonymous class (e.g., Calculator$Anonymous14), convert it to Calculator$14
		class_part = class_part.replace("Anonymous", "") # Remove the "Anonymous" part

	filename_format = f"{package_path}/{class_part}.java" # Construct the full path
	
	return filename_format # Return the converted classname in filename format

def extract_method_name(class_name):
	"""
	Extracts the method name from the class name if the class name contains a "$" symbol.

	:param class_name: The class name which may contain a method name.
	:return: The extracted method name, or None if no method name is found.
	"""

	if "$" in class_name: # Verify if class_name contains "$", indicating a method.
		return class_name[class_name.find("$") + 1:class_name.find(".", class_name.find("$"))] # Extract the method name.
	return None # Return None if no method is found.

def get_code_churn_attributes(diff_file_path, class_name):
	"""
	Get the code churn attributes (lines added and deleted) from the diff file path.

	:param diff_file_path: The diff file path.
	:param class_name: The class name.
	:return: A tuple containing lines added and lines deleted.
	"""

	lines_added = 0 # Initialize the lines added
	lines_deleted = 0 # Initialize the lines deleted
	method_name = extract_method_name(class_name) # Extract the method name from the class name

	# Variables to track whether we're inside the relevant method block (if applicable)
	in_method_block = False # Track if we are inside the method block
	open_braces_count = 0 # Track braces to determine the start and end of a method

	try: # Try to read the diff file
		with open(diff_file_path, "r") as diff_file: # Open the diff file for reading.
			for line in diff_file: # Loop through each line in the diff file.
				if method_name: # If a method name is specified, search for the method block.
					if (f" {method_name}(" in line or line.strip().endswith(f"{method_name}(")) and "{" in line: # Detect if the method signature is found in the diff (Java method pattern).
						in_method_block = True # Enter the method block.
						open_braces_count = 1 # Start counting braces.

					elif in_method_block: # If we are inside the method block.
						open_braces_count += line.count("{") # Increment for opening braces.
						open_braces_count -= line.count("}") # Decrement for closing braces.

						if open_braces_count == 0: # If braces balance out, exit the method block.
							in_method_block = False

				if method_name and not in_method_block: # Only count changes inside the method block if method_name is specified
					continue # Skip lines outside the method

				if line.startswith("+") and not line.startswith("+++"): # Count added lines (starting with "+", excluding diff file headers).
					lines_added += 1 # Increment the lines added.

				elif line.startswith("-") and not line.startswith("---"): # Count deleted lines (starting with "-", excluding diff file headers).
					lines_deleted += 1 # Increment the lines deleted.

		return lines_added, lines_deleted # Return the tuple containing lines added and lines deleted.

	except FileNotFoundError: # Catch the FileNotFoundError exception.
		raise FileNotFoundError(f"{BackgroundColors.RED}Error: Diff file {BackgroundColors.GREEN}{diff_file_path}{BackgroundColors.RED} not found{Style.RESET_ALL}") # Raise an error if the file is not found.

	except Exception as e: # Catch any other exceptions.
		raise Exception(f"{BackgroundColors.RED}Error: An error occurred while reading the diff file {BackgroundColors.GREEN}{diff_file_path}{BackgroundColors.RED}: {e}{Style.RESET_ALL}") # Raise an error if an exception occurs.

def get_code_churn(churn_attributes):
	"""
	Get the code churn value given the churn attributes.

	:param churn_attributes: A tuple containing lines added and lines deleted.
	:return: The code churn value (lines added - lines deleted).
	"""

	lines_added, lines_deleted = churn_attributes # Unpack the tuple into lines added and deleted.
	code_churn_value = lines_added - lines_deleted # Calculate the code churn value.
	return code_churn_value # Return the code churn value.

def process_csv_file(commit_modified_files_dict, file_path, metrics_track_record):
	"""
	Processes a csv file containing the metrics of a method or class.

	:param commit_modified_files_dict: A dictionary containing the commit hashes as keys and the modified files list as values
	:param file_path: The path to the csv file
	:param metrics_track_record: A dictionary containing the track record of the metrics of each method or class
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the csv file containing the metrics of a method or class...{Style.RESET_ALL}")

	with open(file_path, "r") as csvfile: # Open the csv file
		reader = csv.DictReader(csvfile) # Read the csv file
		for row in reader: # Iterate through each row, that is, for each method in the csv file
			identifier, ck_metrics, method_invoked = get_identifier_and_metrics(row) # Get the identifier, metrics and method_invoked of the class or method
			if identifier not in metrics_track_record.keys(): # If the identifier is not in the dictionary, then add it
				metrics_track_record[identifier] = { # Add the identifier to the metrics_track_record dictionary
					"metrics": [], # The metrics list (CBO, WMC, RFC)
					"commit_hashes": [], # The commit hashes list
					"changed": 0, # The number of times the metrics changed
					"code_churns": [], # The code churns values list
					"lines_added": [], # The lines added list
					"lines_deleted": [], # The lines deleted list
					"modified_files_count": [], # The modified files count list
					"method_invoked": method_invoked, # The method_invoked str or methodsInvokedQty int
				}

			metrics_changes = metrics_track_record[identifier]["metrics"] # Get the metrics_changes list for the method
			commit_hashes = metrics_track_record[identifier]["commit_hashes"] # Get the commit hashes list for the method
			commit_number = file_path[file_path.rfind("/", 0, file_path.rfind("/")) + 1:file_path.rfind("/")] # Get the commit number of the current row (i-commit_hash)
			commit_hash = commit_number.split("-")[1] # Get the commit hash of the current row

			# Verify if the file in the current row of the file path was actually modified
			if (commit_number not in commit_hashes or (ck_metrics not in metrics_changes)) and (was_file_modified(commit_modified_files_dict, commit_hash, row)):
				metrics_changes.append(ck_metrics) # Append the metrics to the list
				metrics_track_record[identifier]["changed"] += 1 # Increment the number of changes
				commit_hashes.append(commit_number) # Append the commit hash to the list

				diff_file_path = convert_ck_filepath_to_diff_filepath(file_path, row["file"]) # Convert the CK file path to the diff file path
				class_name = convert_ck_classname_to_filename_format(row["class"]) # Convert the CK class name to the filename format

				churn_attributes = get_code_churn_attributes(diff_file_path, class_name) # Get the code churn attributes
				lines_added, lines_deleted = churn_attributes # Unpack the churn attributes

				code_churn_value = get_code_churn(churn_attributes) # Calculate the code churn value

				metrics_track_record[identifier]["code_churns"].append(code_churn_value) # Append the code churn value to the list
				metrics_track_record[identifier]["lines_added"].append(lines_added) # Append the lines added to the list
				metrics_track_record[identifier]["lines_deleted"].append(lines_deleted) # Append the lines deleted to the list

				modified_files_count = len(commit_modified_files_dict[commit_hash]) # Get the modified files count for the current commit
				metrics_track_record[identifier]["modified_files_count"].append(modified_files_count) # Append the modified files count to the list

				metrics_track_record[identifier]["metrics"] = metrics_changes # Update the metrics_track_record dictionary

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
	progress_bar = None # Initialize the progress bar

	commit_modified_files_dict = generate_commit_modified_files_dict(repository_name) # Generate the commit modified files dictionary, having the commit hashes as keys and the modified files list as values

	# Iterate through each directory inside the repository_directory and call the process_csv_file function to get the methods metrics of each file
	with tqdm(total=len(os.listdir(repository_ck_metrics_path)), unit=f" {BackgroundColors.CYAN}{repository_ck_metrics_path.split('/')[-1]} files{Style.RESET_ALL}") as progress_bar:
		for root, subdirs, files in os.walk(repository_ck_metrics_path): # Walk through the directory
			subdirs.sort(key=lambda x: int(x.split("-")[0])) # Sort the subdirectories in ascending order by the substring that comes before the "-"
			for dir in subdirs: # For each subdirectory in the directories
				for file in os.listdir(os.path.join(root, dir)): # For each file in the subdirectory
					if file == CK_CSV_FILE: # If the file is the desired csv file
						relative_file_path = os.path.join(dir, file) # Get the relative path to the csv file
						file_path = os.path.join(root, relative_file_path) # Get the path to the csv file
						process_csv_file(commit_modified_files_dict, file_path, metrics_track_record) # Process the csv file
						file_count += 1 # Increment the file count

						if progress_bar is None: # If the progress bar is not initialized
							progress_bar = tqdm(total=file_count) # Initialize the progress bar
						else:
							progress_bar.update(1) # Update the progress bar

	if progress_bar is not None: # If the progress bar is not None, then close it
		progress_bar.close() # Close the progress bar

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

def write_metrics_track_record_to_txt(repository_name, metrics_track_record):
	"""
	Writes the metrics_track_record to a txt file.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the metrics track record for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to a txt file...{Style.RESET_ALL}")

	with open(f"{FULL_METRICS_DATA_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}_track_record.txt", "w") as file: # Open the txt file and write the metrics_track_record to it
		for key, value in metrics_track_record.items(): # For each key, value in the metrics_track_record dictionary
			file.write(f"{key}: \n") # Write the key
			file.write(f"\tMetrics: {value['metrics']}\n") # Write the metrics
			file.write(f"\tCommit Hashes: {value['commit_hashes']}\n") # Write the commit hashes
			file.write(f"\tChanged: {value['changed']}\n") # Write the changed value
			file.write(f"\tCode Churns: {value['code_churns']}\n") # Write the code churns value
			file.write(f"\tLines Added: {value['lines_added']}\n") # Write the lines added
			file.write(f"\tLines Deleted: {value['lines_deleted']}\n") # Write the lines deleted
			file.write(f"\tModified Files Count: {value['modified_files_count']}\n") # Write the modified files count
			file.write(f"\t{'Method Invocations' if PROCESS_CLASSES else 'Methods Invoked Qty'}: {value['method_invoked']}\n") # Write the 'Method Invocations' if PROCESS_CLASS, else 'Methods Invoked Qty' value
			file.write(f"\n") # Write a new line

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

def verify_refactoring_file(refactoring_file_path):
	"""
	Validates if the refactoring file was created successfully.

	:param refactoring_file_path: The path to the refactoring file
	:return: A tuple (bool, str) where the bool indicates if the file is valid, and the str provides a message.
	"""

	if not os.path.isfile(refactoring_file_path): # Verify if the file exists
		return False, "File does not exist." # Return False if the file does not exist

	if os.path.getsize(refactoring_file_path) == 0: # Verify if the file is not empty
		return False, "File is empty." # Return False if the file is empty

	try: # Try to load the JSON content of the file
		with open(refactoring_file_path, "r") as file: # Open the refactoring file
			data = json.load(file) # Load the JSON data
			if not data: # Verify if the data is empty
				return True, "File is valid." # Return True if the file is valid
	except json.JSONDecodeError: # Catch the JSONDecodeError exception
		return False, "File contains invalid JSON." # Return False if the file contains invalid JSON

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

	return refactorings_by_filepath # Return the dictionary containing the file paths and their corresponding refactoring types and occurrences

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

def add_csv_header(csv_filename, metric_name):
	""""
	Adds the header to the csv file, if it does not exist.

	:param csv_filename: The name of the csv file
	:param metric_name: The name of the metric
	:return: None
	"""

	expected_header = [] # The expected header list
	if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
		expected_header = ["Class", "Type", f"From {metric_name}", f"To {metric_name}", "Percentual Variation", "Commit Number", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files", "Method Invocations", "Refactoring Patterns"]
	else: # If the PROCESS_CLASSES constant is set to False
		expected_header = ["Class", "Method", f"From {metric_name}", f"To {metric_name}", "Percentual Variation", "Commit Number", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files", "Methods Invoked Qty", "Refactoring Patterns"]
	
	if verify_filepath_exists(csv_filename): # If the file exists
		with open(csv_filename, "r") as file: # Open the file
			first_line = file.readline().strip() # Read the first line
			if first_line != ",".join(expected_header): # If the first line is not equal to the expected header
				existing_lines = file.readlines() # Read the existing lines
				with open(csv_filename, "w") as csvfile: # Open the file in write mode
					writer = csv.writer(csvfile) # Create the csv writer
					writer.writerow(expected_header) # Write the expected header
					csvfile.writelines(existing_lines) # Write the existing lines
	else: # If the file does not exist
		with open(csv_filename, "w") as csvfile: # Open the file in write mode
			writer = csv.writer(csvfile) # Create the csv writer
			writer.writerow(expected_header) # Write the expected header

def verify_substantial_metric_decrease(metrics_values, class_name, raw_variable_attribute, commit_hashes, code_churns, lines_added, lines_deleted, modified_files, occurrences, metric_name, repository_name):
	"""
	Verifies if the class or method has had a substantial decrease in the current metric, and writes the relevant data, including code churn, lines added, and lines deleted, to the CSV file.

	:param metrics_values: A list containing the metrics values for the specified class_name and metric_name
	:param class_name: The class name of the current linear regression
	:param raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
	:param commit_hashes: The commit hashes list for the specified class_name
	:param code_churns: The list of code churn values for each commit
	:param lines_added: The list of lines added for each commit
	:param lines_deleted: The list of lines deleted for each commit
	:param modified_files: The list of modified files for each commit
	:param occurrences: The occurrences counter of the class_name
	:param metric_name: The name of the metric
	:param repository_name: The name of the repository
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the class or method has had a substantial decrease in the {BackgroundColors.CYAN}{metric_name}{BackgroundColors.GREEN} metric...{Style.RESET_ALL}")

	if any(keyword.lower() in class_name.lower() for keyword in IGNORE_CLASS_NAME_KEYWORDS): # If any of the class name ignore keywords is found in the class name, return
		return # If any of the class name ignore keywords is found in the class name, return

	if any(keyword.lower() in raw_variable_attribute.lower() for keyword in IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS): # If any of the variable/attribute ignore keywords is found in the variable attribute,
		return # If any of the variable/attribute ignore keywords is found in the variable attribute, return
	
	folder_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/" # The folder path
	csv_filename = f"{folder_path}{SUBSTANTIAL_CHANGES_FILENAME.replace("METRIC_NAME", metric_name)}" # The csv file name

	global FIRST_SUBSTANTIAL_CHANGE_VERIFICATION # Declare that we're using the global variable
	
	if FIRST_SUBSTANTIAL_CHANGE_VERIFICATION and verify_filepath_exists(csv_filename): # Verify if it's the first run and if the CSV file already exists
		FIRST_SUBSTANTIAL_CHANGE_VERIFICATION = False # Update the flag after handling the first run
		os.remove(csv_filename) # Remove the CSV file if it exists

	if not verify_filepath_exists(csv_filename): # Add the header if the file is newly created
		add_csv_header(csv_filename, metric_name) # Add the header to the csv file

	biggest_change = [0, 0, 0.00] # The biggest change values in the metric [from, to, percentual_variation]
	commit_data = ["", "", "", ""] # The commit data [from_commit_number, from_commit_hash, to_commit_number, to_commit_hash]

	for i in range(1, len(metrics_values)): # Loop through the metrics values
		if metrics_values[i] >= metrics_values[i - 1] or metrics_values[i - 1] == 0: # Verify if the current metric is bigger than the previous metric or the previous metric is zero
			continue # If the current metric is bigger than the previous metric or the previous metric is zero, then continue

		current_percentual_variation = round((metrics_values[i - 1] - metrics_values[i]) / metrics_values[i - 1], 3) # Calculate the current percentual variation

		if current_percentual_variation > DESIRED_DECREASE and current_percentual_variation > biggest_change[2]: # If the current percentual variation is bigger than the desired decrease, then update the biggest_change list
			temp_commit_data = [commit_hashes[i - 1], commit_hashes[i]] # The commit data [from_commit_hash, to_commit_hash]
			refactorings_info = get_refactoring_info(repository_name, temp_commit_data[1].split("-")[0], temp_commit_data[1].split("-")[1], class_name) # Get the refactoring information

			if not DESIRED_REFACTORINGS_ONLY or any(refactoring in DESIRED_REFACTORINGS for refactoring_list in refactorings_info.values() for refactoring in refactoring_list): # Verify if we're not filtering by desired refactorings or if the current refactoring type is a desired refactoring.
				refactorings_summary = convert_refactorings_dictionary_to_string(refactorings_info) # Convert the refactorings dictionary into a string

				biggest_change = [metrics_values[i - 1], metrics_values[i], current_percentual_variation, refactorings_summary.replace("'", "")] # Update the biggest_change list and commit data only if the conditions above are met.
				commit_data = [temp_commit_data[0].split("-")[0], temp_commit_data[0].split("-")[1], temp_commit_data[1].split("-")[0], temp_commit_data[1].split("-")[1]] # Splitting commit hash to get commit number and hash

	if biggest_change[2] > DESIRED_DECREASE and biggest_change[3]: # If the biggest change percentual variation is bigger than the desired decrease and the refactorings summary is not empty
		with open(f"{csv_filename}", "a") as csvfile: # Open the csv file
			writer = csv.writer(csvfile) # Create the csv writer
			writer.writerow([class_name, raw_variable_attribute, biggest_change[0], biggest_change[1], round(biggest_change[2] * 100, 2), f"{commit_data[0]} -> {commit_data[2]}", f"{commit_data[1]} -> {commit_data[3]}", occurrences, code_churns[i], lines_added[i], lines_deleted[i], modified_files[i], biggest_change[3]]) # Write the class name, the variable attribute, the biggest change values, the commit data and the refactorings information to the csv file

def linear_regression_graphics(metrics, class_name, variable_attribute, commit_hashes, code_churns, lines_added, lines_deleted, modified_files, occurrences, raw_variable_attribute, repository_name):
	"""
	Perform linear regression on the given metrics and save the plot to a PNG file.

	:param metrics: A list containing the metrics values for linear regression
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param commit_hashes: A list of the commit_hashes for the specified class_name/identifier.
	:param code_churns: A list of the code churn values for each commit
	:param lines_added: A list of the lines added for each commit
	:param lines_deleted: A list of the lines deleted for each commit
	:param modified_files: A list of the modified files count for each commit
	:param occurrences: The number of occurrences of the class or method
	:param raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
	:param repository_name: The name of the repository
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Performing linear regression on the given metrics and saving the plot to a PNG file for {BackgroundColors.CYAN}{class_name}{BackgroundColors.GREEN} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	if not metrics and VERBOSE: # Verify for empty metrics list
		print(f"{BackgroundColors.RED}Metrics list for {class_name} {variable_attribute} is empty!{Style.RESET_ALL}")
		return # Return if the metrics list is empty
	
	try: # Try to convert the metrics list to a NumPy array
		metrics_array = np.array(metrics, dtype=float) # Safely convert to NumPy array for flexibility in handling
	except: # Catch any exceptions
		verbose_output(true_string=f"{BackgroundColors.RED}Error converting the {BackgroundColors.CYAN}metrics{BackgroundColors.GREEN} to {BackgroundColors.CYAN}NumPy array{BackgroundColors.GREEN} for {class_name} {variable_attribute}.{Style.RESET_ALL}")
		return

	if metrics_array.ndim != 2 or metrics_array.shape[1] < len(METRICS_POSITION): # Verify for invalid values in the metrics
		verbose_output(true_string=f"{BackgroundColors.RED}Metrics structure for {class_name} {variable_attribute} is not as expected!{Style.RESET_ALL}")
		return # Return if the metrics structure is not as expected
	
	for metric_name, metric_position in METRICS_POSITION.items(): # Loop through the metrics_position dictionary
		commit_number = np.arange(metrics_array.shape[0]) # Create the commit number array
		if not commit_number.any(): # If the commit number is empty
			continue # Ignore the current iteration, since there are no commit numbers, thus no linear regression can be performed
		metric_values = metrics_array[:, metric_position] # Extract the metrics values from the metrics array in the specified position (column)
		if metric_name in SUBSTANTIAL_CHANGE_METRICS: # For the CBO metric, verify if there occurred any substantial decrease in the metric
			verify_substantial_metric_decrease(metric_values, class_name, raw_variable_attribute, commit_hashes, code_churns, lines_added, lines_deleted, modified_files, occurrences, metric_name, repository_name) if RUN_FUNCTIONS["verify_substantial_metric_decrease"] else None # Verify if there occurred any substantial decrease in the metric

		if len(commit_number) < 2 or len(metric_values) < 2: # Verify for sufficient data points for regression
			return # Return if there are not enough data points for regression
		
		# Perform linear regression using Scikit-Learn
		model = LinearRegression() # Create the linear regression model
		model.fit(commit_number.reshape(-1, 1), metric_values) # Fit the model to the data
		linear_fit = model.predict(commit_number.reshape(-1, 1)) # Perform the linear fit

		# Create the plot
		plt.figure(figsize=(10, 6)) # Set the figure size
		plt.plot(commit_number, metric_values, "o", label=f"{metric_name}") # Plot the metrics values
		plt.plot(commit_number, linear_fit, "-", label="Linear Regression Fit") # Plot the linear fit
		plt.xlabel("Commit Number") # Set the x-axis label
		plt.ylabel(f"{metric_name} Value") # Set the y-axis label
		plt.title(f"Linear Regression for {metric_name} metric of {class_name} {variable_attribute}") # Set the title
		plt.legend() # Show the legend

		relative_metrics_prediction_directory_path = f"{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}" # The relative path to the directory where the plot will be stored
		full_metrics_prediction_directory_path = f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}" # The full path to the directory where the plot will be stored
		create_directory(full_metrics_prediction_directory_path, relative_metrics_prediction_directory_path) # Create the directory where the plot will be stored

		plt.savefig(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}/{metric_name}{PNG_FILE_EXTENSION}") # Save the plot to a PNG file
		plt.close() # Close the plot

def write_metrics_evolution_to_csv(repository_name, metrics_track_record):
	"""
	Writes the metrics evolution to a csv file.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the metrics evolution for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to a csv file...{Style.RESET_ALL}")
	
	with tqdm(total=len(metrics_track_record), unit=f" {BackgroundColors.CYAN}Creating Linear Regression and Metrics Evolution{Style.RESET_ALL}") as progress_bar: # For every identifier in the metrics_track_record, store each metrics values tuple in a row of the csv file
		for identifier, record in metrics_track_record.items(): # For each identifier and record in the metrics_track_record dictionary
			metrics = record["metrics"] # Get the metrics list
			class_name = identifier.split(" ")[0] # Get the identifier which is currently the class name
			variable_attribute = get_clean_id(identifier.split(" ")[1]) # Get the variable attribute which could be the type of the class or the method name
			full_metrics_evolution_directory_path = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/" # The path to the directory where the csv file will be stored
			create_directory(full_metrics_evolution_directory_path, f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}") # Create the directory where the csv file will be stored
			metrics_filename = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}"

			with open(metrics_filename, "w") as csvfile: # Open the csv file and write the metrics to it
				writer = csv.writer(csvfile) # Create the csv writer
				if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
					unique_identifier = class_name # The unique identifier is the class name
					writer.writerow(["Class", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files", "CBO", "WMC", "RFC", "Method Invocations"]) # Write the header to the csv file
				else: # If the PROCESS_CLASSES constant is set to False
					unique_identifier = variable_attribute # The unique identifier is the method name
					writer.writerow(["Method", "Commit Hash", "Code Churn", "Lines Added", "Lines Deleted", "Modified Files", "CBO", "WMC", "RFC", "Methods Invoked Qty"]) # Write the header to the csv file
				
				previous_metrics = None # Initialize to None for the first iteration
				metrics_len = len(metrics) # Get the len of the metrics list

				for i in range(metrics_len): # For each metric in the metrics list
					current_metrics = (metrics[i][0], metrics[i][1], metrics[i][2]) # Tuple of current metrics (CBO, WMC, RFC)

					if WRITE_FULL_HISTORY or (previous_metrics is None or current_metrics != previous_metrics): # Verify if the metrics tuple is different from the previous metrics tuple
						writer.writerow([unique_identifier, record["commit_hashes"][i], record["code_churns"][i], record["lines_added"][i], record["lines_deleted"][i], record["modified_files_count"][i], metrics[i][0], metrics[i][1], metrics[i][2], record["method_invoked"]]) # Write the unique identifier, the commit hash, code churn, lines added, lines deleted, and the metrics to the csv file
					
					previous_metrics = current_metrics # Update previous metrics

			linear_regression_graphics(metrics, class_name, variable_attribute, record["commit_hashes"], record["code_churns"][i], record["lines_added"][i], record["lines_deleted"][i], record["modified_files_count"][i], record["method_invoked"], identifier.split(" ")[1], repository_name) if RUN_FUNCTIONS["linear_regression_graphics"] else None # Perform linear regression and generate graphics for the metrics
			progress_bar.update(1) # Update the progress bar

def merge_code_churn_fields(code_churn_metrics):
	"""
	Merges the code churn fields into a single string separated by spaces.

	:param code_churn_metrics: A dictionary containing the code churn metrics
	:return: A string containing the merged code churn fields
	"""

	churn_info = [] # Initialize the churn information list

	for i in range(len(code_churn_metrics["code_churns"])): # For each code churn in the code churns list
		churn_entry = f"{code_churn_metrics['code_churns'][i]} ({code_churn_metrics['lines_added'][i]} - {code_churn_metrics['lines_deleted'][i]})"
		churn_info.append(churn_entry) # Append the code churn entry to the churn information list
	
	churn_merged = ", ".join(churn_info) # Join the churn information list with a comma and a space

	return churn_merged # Return the merged code churn fields

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

def write_method_metrics_statistics(csv_writer, id, key, metrics, metrics_values, first_commit_hash, last_commit_hash):
	"""
	Calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file.

	:param csv_writer: The csv writer object
	:param id: The id of the method
	:param key: The key of the method
	:param metrics: The list of metrics
	:param metrics_values: The list of metrics values
	:param first_commit_hash: The first commit hash of the method
	:param last_commit_hash: The last commit hash of the method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating statistics for method {BackgroundColors.CYAN}{id}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

	cbo_stats = calculate_metric_statistics(metrics_values[0]) # Calculate statistics for CBO
	wmc_stats = calculate_metric_statistics(metrics_values[1]) # Calculate statistics for WMC
	rfc_stats = calculate_metric_statistics(metrics_values[2]) # Calculate statistics for RFC

	churn_stats = calculate_metric_statistics(metrics["code_churns"]) # Calculate statistics for code churn
	modified_files_stats = calculate_metric_statistics(metrics["modified_files_count"]) # Calculate statistics for modified files

	csv_writer.writerow([id, key, metrics["changed"], *churn_stats, *modified_files_stats, *cbo_stats, *wmc_stats, *rfc_stats, first_commit_hash, last_commit_hash, metrics["method_invoked"]]) # Write the metrics statistics to the CSV file

def generate_metrics_track_record_statistics(repository_name, metrics_track_record):
	"""
	Processes the metrics in metrics_track_record to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the metrics in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to calculate the minimum, maximum, average, and third quartile of each metric and writing it to a csv file...{Style.RESET_ALL}")

	unsorted_metrics_filename = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}" # The unsorted metrics filename
	with open(unsorted_metrics_filename, "w") as csvfile: # Open the csv file in write mode
		writer = csv.writer(csvfile) # Create the csv writer
		if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
			writer.writerow(["Class", "Type", "Changed", "Churn Min", "Churn Max", "Churn Avg", "Churn Q3", "Modified Files Min", "Modified Files Max", "Modified Files Avg", "Modified Files Q3", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash", "Method Invocations"]) # Write the header to the csv file but using the "Type" in the second column
		else: # If the PROCESS_CLASSES constant is set to False
			writer.writerow(["Class", "Method", "Changed", "Churn Min", "Churn Max", "Churn Avg", "Churn Q3", "Modified Files Min", "Modified Files Max", "Modified Files Avg", "Modified Files Q3", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash", "Methods Invoked Qty"]) # Write the header to the csv file but using the "Method" in the second column

		with tqdm(total=len(metrics_track_record), unit=f" {BackgroundColors.CYAN}Creating Metrics Statistics{Style.RESET_ALL}") as progress_bar: # For every identifier in the metrics_track_record, store each metrics values tuple in a row of the csv file
			for identifier, metrics in metrics_track_record.items(): # For each identifier and metrics in the metrics_track_record dictionary
				if metrics["changed"] < MINIMUM_CHANGES: # Verify if the metrics changes is greater than the minimum changes
					continue # If the metrics changes is less than the minimum changes, then jump to the next iteration

				metrics_values = [] # This stores the metrics values in a list of lists of each metric
				for i in range(0, NUMBER_OF_METRICS): # For each metric in the metrics list
					metrics_values.append([sublist[i] for sublist in metrics["metrics"]]) # This get the metrics values of each metric occurrence in the method to get the min, max, avg, and third quartile of each metric

				id = identifier.split(" ")[0] # Get the id of the method
				key = identifier.split(" ")[1] # Get the key of the method

				write_method_metrics_statistics(writer, id, key, metrics, metrics_values, metrics_track_record[identifier]["commit_hashes"][0], metrics_track_record[identifier]["commit_hashes"][-1]) # Write the metrics statistics to the csv file
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
	
	data = data.sort_values(by=["Changed"], ascending=False) # Sort the csv file by the number of changes
	
	sorted_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SORTED_CHANGED_METHODS_CSV_FILENAME}" # The sorted csv file path
	
	data.to_csv(sorted_csv_file_path, index=False) # Write the sorted csv file to a new csv file

def sort_csv_by_percentual_variation(repository_name):
	"""
	Sorts the csv files according to the percentual variation of the metric.

	:param repository_name: The name of the repository
	:return: None
	"""
	
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}interesting changes files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}percentual variation of the metric{BackgroundColors.GREEN}.{Style.RESET_ALL}")

	for metric_name in SUBSTANTIAL_CHANGE_METRICS:
		data = pd.read_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME.replace("METRIC_NAME", metric_name)}") # Read the csv file
		data = data.sort_values(by=["Percentual Variation"], ascending=False) # Sort the csv file by the percentual variation of the metric
		data.to_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME.replace("METRIC_NAME", metric_name)}", index=False) # Write the sorted csv file to a new csv file

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
		repositories_attributes[repository_name]["size_in_gb"] += get_output_directories_size_in_gb(repository_name, OUTPUT_DIRECTORIES) # Update the size in GB
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

	number_of_commits = len(list(Repository(repository_url).traverse_commits())) # Get the number of commits for the specified repository
	if not verify_ck_metrics_directory(repository_name, repository_url, number_of_commits): # Verify if the ck metrics were already calculated, which are the source of the data processed by traverse_directory(repository_ck_metrics).
		print(f"{BackgroundColors.RED}The metrics for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} were not calculated. Please run the {BackgroundColors.CYAN}code_metrics.py{BackgroundColors.RED} file first{Style.RESET_ALL}")
		return # Return if the ck metrics were not calculated

	repository_ck_metrics_path = get_directory_path(repository_name) # Get the directory path for the specified repository name
	
	create_directories(repository_name) # Create the desired directory if it does not exist

	metrics_track_record = traverse_directory(repository_name, repository_ck_metrics_path) # Traverse the directory and get the method metrics

	sorted_metrics_track_record = sort_commit_hashes_by_commit_number(metrics_track_record) # Sort the commit_hashes list for each entry in the metrics_track_record dictionary by the commit number

	write_metrics_track_record_to_txt(repository_name, sorted_metrics_track_record) if RUN_FUNCTIONS["write_metrics_track_record_to_txt"] else None # Write the metrics_track_record to a txt file
	write_metrics_evolution_to_csv(repository_name, sorted_metrics_track_record) if RUN_FUNCTIONS["write_metrics_evolution_to_csv"] else None # Write, for each identifier, the metrics evolution values to a csv file
	generate_metrics_track_record_statistics(repository_name, sorted_metrics_track_record) if RUN_FUNCTIONS["generate_metrics_track_record_statistics"] else None # Generate the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file

	sort_csv_by_changes(repository_name) # Sort the csv file by the number of changes

	old_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}" # The old csv file path
	os.remove(old_csv_file_path) # Remove the old csv file

	sort_csv_by_percentual_variation(repository_name) if RUN_FUNCTIONS["sort_csv_by_percentual_variation"] else None# Sort the interesting changes csv file by the percentual variation of the metric

	repositories_attributes = update_repository_attributes(repository_name, elapsed_time) # Update the attributes of the repositories file with the elapsed time and output data size in GB
	write_dict_to_csv(FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH, repositories_attributes) # Write the updated data back to the CSV file

	elapsed_time = time.time() - start_time # Calculate the elapsed time
	elapsed_time_string = f"Time taken to generate the {BackgroundColors.CYAN}metrics evolution records, metrics statistics and linear regression{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS}{BackgroundColors.GREEN} in {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
	output_time(elapsed_time_string, round(elapsed_time, 2)) # Output the elapsed time

def process_all_repositories():
	"""
	Processes all the repositories in the DEFAULT_REPOSITORIES dictionary.

	:return: None
	"""

	for repository_name, repository_url in DEFAULT_REPOSITORIES.items(): # Loop through the DEFAULT_REPOSITORIES dictionary
		print(f"") # Print an empty line
		print(f"{BackgroundColors.GREEN}Processing the {BackgroundColors.CYAN}metrics evolution history, metrics statistics, linear regression, substantial changes and refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS}{BackgroundColors.GREEN} from the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
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
	print(f"{BackgroundColors.GREEN}This script generates the {BackgroundColors.CYAN}classes or methods metrics evolution history, metrics statistics, linear regression, substantial changes and refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{', '.join(repo.capitalize() for repo in DEFAULT_REPOSITORIES.keys())}{BackgroundColors.GREEN} repositories based on the {BackgroundColors.CYAN}ck metrics files, the commit hashes list file and the diffs of each commit{BackgroundColors.GREEN} generated by the {BackgroundColors.CYAN}./code_metrics.py{BackgroundColors.GREEN} code.{Style.RESET_ALL}")
	print(f"{BackgroundColors.RED}This Python code avoids using threads due to its high memory usage. It stores metric values, generates regression graphs, and detects substantial changes, which demands a lot of RAM.{Style.RESET_ALL}\n")

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
