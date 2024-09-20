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
from pydriller.metrics.process.code_churn import CodeChurn # For calculating the Code Churn (Delta of Added and Deleted Lines) metric
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from sklearn.linear_model import LinearRegression # For the linear regression
from tqdm import tqdm # For progress bar

# Imports from the repositories_picker.py file
from repositories_picker import BackgroundColors # Import the BackgroundColors class
from repositories_picker import DEFAULT_REPOSITORIES, PROCESS_JSON_REPOSITORIES, RELATIVE_REPOSITORIES_DIRECTORY_PATH, SOUND_FILE_PATH, START_PATH # Importing Constants from the repositories_picker.py file
from repositories_picker import create_directory, output_time, path_contains_whitespaces, play_sound, setup_repository, update_repositories_dictionary, update_sound_file_path, verbose_output # Importing Functions from the repositories_picker.py file

# Imports from the code_metrics.py file
from code_metrics import CK_METRICS_FILES, CSV_FILE_EXTENSION, FULL_CK_METRICS_DIRECTORY_PATH, FULL_REFACTORINGS_DIRECTORY_PATH, FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH, RELATIVE_REFACTORINGS_DIRECTORY_PATH # Importing Constants from the code_metrics.py file
from code_metrics import get_output_directories_size_in_gb, verify_ck_metrics_folder # Importing Functions from the code_metrics.py file

# Default values that can be changed:
VERBOSE = False # If True, then the program will output the progress of the execution
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 3 # The number of metrics
DESIRED_DECREASE = 0.00 # The desired decrease in the metric
IGNORE_CLASS_NAME_KEYWORDS = ["test"] # The keywords to ignore in the class name
IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS = ["anonymous"] # The keywords to ignore in the variable attribute
SUBSTANTIAL_CHANGE_METRIC = "CBO" # The desired metric to search for substantial changes
METRICS_POSITION = {"CBO": 0, "WMC": 1, "RFC": 2} # The position of the metrics in the metrics list
DESIRED_REFACTORINGS_ONLY = False # If True, then only the desired refactorings will be stored
DESIRED_REFACTORINGS = ["Extract Method", "Extract Class", "Pull Up Method", "Push Down Method", "Extract Superclass", "Move Method"] # The desired refactorings to search for substantial changesWRITE_FULL_HISTORY = False # If True, then the metrics evolution will store all of the metrics history and not only the moments the metrics changed between commits

# Constants:
PROCESS_CLASSES = True # If True, then the classes will be processed, otherwise the methods will be processed
DEFAULT_REPOSITORIES_NAMES = json.dumps(list(DEFAULT_REPOSITORIES.keys())) # The default repository names
FIRST_SUBSTANTIAL_CHANGE_VERIFICATION = True # If True, then it is the first run of the program

# Extensions:
PNG_FILE_EXTENSION = ".png" # The extension of the PNG files
REFACTORING_MINER_JSON_FILE_EXTENSION = ".json" # The extension of the RefactoringMiner JSON files

# Filenames:
CK_CSV_FILE = CK_METRICS_FILES[0] if PROCESS_CLASSES else CK_METRICS_FILES[1] # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
UNSORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_unsorted_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the top changed methods
SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the sorted top changed methods
SUBSTANTIAL_CHANGES_FILENAME = f"substantial_{SUBSTANTIAL_CHANGE_METRIC}_{CLASSES_OR_METHODS}_changes{CSV_FILE_EXTENSION}" # The relative path to the directory containing the interesting changes

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

def verify_file(file_path):
	"""
	Verifies if a specified file exists.

	:param file_path: The path to the file
	:return: True if the file already exists, False otherwise
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the file {BackgroundColors.CYAN}{file_path}{BackgroundColors.GREEN} exists...{Style.RESET_ALL}")
	
	return os.path.exists(file_path) # Return True if the file already exists, False otherwise

def verify_repositories_execution_constants():
   """
   Verify the constants used in the execution of the repositories.
   It will process the JSON repositories, if the PROCESS_JSON_REPOSITORIES constant is set to True or if the DEFAULT_REPOSITORIES dictionary is empty.
   
   :return: None
   """

   # Verify if PROCESS_REPOSITORIES_LIST is set to True or if the DEFAULT_REPOSITORIES dictionary is empty
   if PROCESS_JSON_REPOSITORIES or not DEFAULT_REPOSITORIES:
      if not update_repositories_dictionary(): # Update the repositories list
         print(f"{BackgroundColors.RED}The repositories list could not be updated. Please execute the {BackgroundColors.CYAN}repositories_picker.py{BackgroundColors.RED} script or manually fill the {BackgroundColors.CYAN}DEFAULT_REPOSITORIES{BackgroundColors.RED} dictionary.{Style.RESET_ALL}")
         exit() # Exit the program if the repositories list could not be updated

def verify_and_update_repositories():
	"""
	Verifies the DEFAULT_REPOSITORIES and PROCESS_JSON_REPOSITORIES constants,
	updates the repositories list file with the DEFAULT_REPOSITORIES dictionary,
	and updates the DEFAULT_REPOSITORIES_NAMES list with the keys of the DEFAULT_REPOSITORIES dictionary.

	:return: None
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying and updating the repositories...{Style.RESET_ALL}")

	# Verify DEFAULT_REPOSITORIES and PROCESS_JSON_REPOSITORIES constants
	verify_repositories_execution_constants()

	# Update DEFAULT_REPOSITORIES_NAMES with the keys of the DEFAULT_REPOSITORIES dictionary
	global DEFAULT_REPOSITORIES_NAMES
	DEFAULT_REPOSITORIES_NAMES = list(DEFAULT_REPOSITORIES.keys())

	verbose_output(true_string=f"{BackgroundColors.GREEN}The {BackgroundColors.CYAN}DEFAULT_REPOSITORIES_NAMES{BackgroundColors.GREEN} list was successfully updated with the keys of the {BackgroundColors.CYAN}DEFAULT_REPOSITORIES{BackgroundColors.GREEN} dictionary.{Style.RESET_ALL}")

def input_with_timeout(prompt, timeout=60):
	"""
	Prompts the user for input with a specified timeout on Unix-based systems.
	
	:param prompt: str, the prompt message to display
	:param timeout: int, the timeout in seconds
	:return: str, the user input or None if timeout
	"""
	
	print(prompt, end="", flush=True) # Print the prompt message without a newline character

	# Wait for input with a timeout
	ready, _, _ = select.select([sys.stdin], [], [], timeout)

	if ready:
		return sys.stdin.readline().strip().lower() # Read and return user input
	else:
		return None # Return None if timeout is reached

def update_global_variables_for_processing(process_classes):
	"""
	Updates global variables based on whether to process classes or methods.

	:param process_classes: bool, if True, processes classes; if False, processes methods
	"""

	global PROCESS_CLASSES, CK_CSV_FILE, CLASSES_OR_METHODS, UNSORTED_CHANGED_METHODS_CSV_FILENAME, SORTED_CHANGED_METHODS_CSV_FILENAME, SUBSTANTIAL_CHANGES_FILENAME
	
	PROCESS_CLASSES = process_classes # Update the PROCESS_CLASSES constant
	CK_CSV_FILE = CK_METRICS_FILES[0] if PROCESS_CLASSES else CK_METRICS_FILES[1] # Update the CK_CSV_FILE constant
	CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # Update the CLASSES_OR_METHODS constant
	UNSORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_unsorted_changes.{CK_CSV_FILE.split('.')[1]}" # Update the UNSORTED_CHANGED_METHODS_CSV_FILENAME constant
	SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_changes.{CK_CSV_FILE.split('.')[1]}" # Update the SORTED_CHANGED_METHODS_CSV_FILENAME constant
	SUBSTANTIAL_CHANGES_FILENAME = f"substantial_{SUBSTANTIAL_CHANGE_METRIC}_{CLASSES_OR_METHODS}_changes{CSV_FILE_EXTENSION}" # Update the SUBSTANTIAL_CHANGES_FILENAME constant

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
	
	# Get the directory path for the specified repository name
	repository_ck_metrics_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}"

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

	# Traverse the repository and get the modified files for each commit and store it in the commit_modified_files_dict
	for commit in Repository(DEFAULT_REPOSITORIES[repository_name]).traverse_commits():
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

	# Replace the slashes with dots
	package_name = package_name.replace("/", ".")

	return package_name # Return the package name

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

	# Create a tuple containing the metrics
	metrics = (cbo, wmc, rfc) # The metrics tuple
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

	# Calculate the file path starting after the specified directory
	path_index = file_path.find(RELATIVE_REPOSITORIES_DIRECTORY_PATH)

	if path_index != -1:
		file_path = file_path[path_index + len(RELATIVE_REPOSITORIES_DIRECTORY_PATH) + 1:]
	
	repository_name = file_path.split("/")[0] # Get the repository name
	file_path = file_path[len(repository_name) + 1:] # Get the file path starting after the repository name

	for modified_file_path in modified_files_paths: # Iterate through the modified files paths
		# If the modified file path is equal to the file path, then the file was modified
		if modified_file_path == file_path:
			return True # The file was modified
	return False # The file was not modified

def convert_ck_classname_to_filename_format(ck_classname):
	"""
	Convert CK classname format (e.g., com.houarizegai.calculator.Calculator$Anonymous14)
	to the filename format used by code churn (e.g., com/houarizegai/calculator/Calculator$14).
	
	:param ck_classname: The classname from the CK tool (e.g., com.houarizegai.calculator.Calculator$Anonymous14).
	:return: The converted classname in filename format (e.g., com/houarizegai/calculator/Calculator$14).
	"""
	
	# Replace dots with slashes except for the class and anonymous part
	package_path = ck_classname.rsplit(".", 1)[0].replace(".", "/")
	
	# Get the class and anonymous part (e.g., Calculator$Anonymous14)
	class_part = ck_classname.rsplit(".", 1)[-1]
	
	# If it's an anonymous class (e.g., Calculator$Anonymous14), convert it to Calculator$14
	if "Anonymous" in class_part:
		class_part = class_part.replace("Anonymous", "")

	# Construct the full path
	filename_format = f"{package_path}/{class_part}"
	
	return filename_format # Return the converted classname in filename format

def calculate_code_churn(repo_path, class_name, commit_hash):
	"""
	Calculate the code churn metric for a specific class between two commits.
	
	:param repo_path: Path to the repository.
	:param class_name: Name of the class to search for.
	:param commit_hash: Commit hash.
	:return: The churn value of the matched file or 0 if not found.
	"""
	
	# Initialize the code churn metric for the specified repository and commit range
	code_churn_metric = CodeChurn(path_to_repo=repo_path, from_commit=commit_hash, to_commit=commit_hash)
	
	# Get the code churn for all files in the repository
	files_churn = code_churn_metric.count()

	if not files_churn or not class_name: # If files_churn is empty or class_name is None,
		return 0

	matched_churn_value = 0 # Initialize variable to store the churn value

	# Verify if the class_name is a key or a substring in the keys of the files churn
	for churn_file in files_churn.keys():
		if churn_file is None or class_name is None: # If the churn_file or class_name is None, skip to the next iteration
			continue

		if class_name in churn_file: # If the class_name is a substring in the churn_file
			matched_churn_value = files_churn[churn_file] # Get the churn value of the matched file
			return matched_churn_value # Return the churn value of the matched file

	return matched_churn_value # If no match, return 0

def process_csv_file(commit_modified_files_dict, repo_path, file_path, metrics_track_record):
	"""
	Processes a csv file containing the metrics of a method nor class.

	:param commit_modified_files_dict: A dictionary containing the commit hashes as keys and the modified files list as values
	:param repo_path: The path to the repository
	:param file_path: The path to the csv file
	:param metrics_track_record: A dictionary containing the track record of the metrics of each method nor class
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the csv file containing the metrics of a method nor class...{Style.RESET_ALL}")

	# Open the csv file
	with open(file_path, "r") as csvfile:
		# Read the csv file
		reader = csv.DictReader(csvfile)
		# Iterate through each row, that is, for each method in the csv file
		for row in reader:
			# Get the identifier, metrics and method_invoked of the class or method
			identifier, ck_metrics, method_invoked = get_identifier_and_metrics(row)

			# If the identifier is not in the dictionary, then add it
			if identifier not in metrics_track_record.keys():
				metrics_track_record[identifier] = {"metrics": [], "commit_hashes": [], "changed": 0, "code_churns": [], "method_invoked": method_invoked}

			# Get the metrics_changes list for the method
			metrics_changes = metrics_track_record[identifier]["metrics"]
			# Get the commit hashes list for the method
			commit_hashes = metrics_track_record[identifier]["commit_hashes"]
			# Get the commit number of the current row (i-commit_hash)
			commit_number = file_path[file_path.rfind("/", 0, file_path.rfind("/")) + 1:file_path.rfind("/")]
			# Get the commit hash of the current row
			commit_hash = commit_number.split("-")[1]

			# Verify if the file in the current row of the file path was actually modified
			if (commit_number not in commit_hashes or (ck_metrics not in metrics_changes)) and (was_file_modified(commit_modified_files_dict, commit_hash, row)):
				# Append the metrics to the list
				metrics_changes.append(ck_metrics)
				# Increment the number of changes
				metrics_track_record[identifier]["changed"] += 1
				# Append the commit hash to the list
				commit_hashes.append(commit_number)
				# Calculate code churn for the specific file and commit
				metrics_track_record[identifier]["code_churns"] = calculate_code_churn(repo_path, convert_ck_classname_to_filename_format(row["class"]), commit_hash)
				# Update the metrics_track_record dictionary
				metrics_track_record[identifier]["metrics"] = metrics_changes

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

	# Generate the commit modified files dictionary, having the commit hashes as keys and the modified files list as values
	commit_modified_files_dict = generate_commit_modified_files_dict(repository_name)

	repo_path = f"{START_PATH}/{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository

	# Iterate through each directory inside the repository_directory and call the process_csv_file function to get the methods metrics of each file
	with tqdm(total=len(os.listdir(repository_ck_metrics_path)), unit=f" {BackgroundColors.CYAN}{repository_ck_metrics_path.split('/')[-1]} files{Style.RESET_ALL}") as progress_bar:
		for root, subdirs, files in os.walk(repository_ck_metrics_path):
			# Sort the subdirectories in ascending order by the substring that comes before the "-"
			subdirs.sort(key=lambda x: int(x.split("-")[0]))
			for dir in subdirs: # For each subdirectory in the directories
				for file in os.listdir(os.path.join(root, dir)): # For each file in the subdirectory
					if file == CK_CSV_FILE: # If the file is the desired csv file
						relative_file_path = os.path.join(dir, file) # Get the relative path to the csv file
						file_path = os.path.join(root, relative_file_path) # Get the path to the csv file
						process_csv_file(commit_modified_files_dict, repo_path, file_path, metrics_track_record) # Process the csv file
						file_count += 1 # Increment the file count

						if progress_bar is None: # If the progress bar is not initialized
							progress_bar = tqdm(total=file_count) # Initialize the progress bar
						else:
							progress_bar.update(1) # Update the progress bar

	# If the progress bar is not None, then close it
	if progress_bar is not None:
		progress_bar.close() # Close the progress bar

	# Return the method metrics, which is a dictionary containing the metrics of each method  
	return metrics_track_record

def sort_commit_hashes_by_commit_number(metrics_track_record):
	"""
	Sorts the commit_hashes list for each entry in the metrics_track_record dictionary
	by the commit number (numeric value before the hyphen).

	:param metrics_track_record: A dictionary where each key maps to another dictionary that contains a list under the key "commit_hashes".
	:return: The sorted metrics_track_record
	"""

	for key in metrics_track_record:
		# Sort the commit hashes list for each class or method according to the commit number
		metrics_track_record[key]["commit_hashes"].sort(key=lambda x: int(x.split("-")[0]))

	return metrics_track_record # Return the sorted metrics_track_record

def write_metrics_track_record_to_txt(repository_name, metrics_track_record):
	"""
	Writes the metrics_track_record to a txt file.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the metrics track record for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to a txt file...{Style.RESET_ALL}")

	# Open the txt file and write the metrics_track_record to it
	with open(f"{FULL_METRICS_DATA_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}_track_record.txt", "w") as file:
		for key, value in metrics_track_record.items(): # For each key, value in the metrics_track_record dictionary
			file.write(f"{key}: \n") # Write the key
			file.write(f"\tMetrics: {value['metrics']}\n") # Write the metrics
			file.write(f"\tCommit Hashes: {value['commit_hashes']}\n") # Write the commit hashes
			file.write(f"\tChanged: {value['changed']}\n") # Write the changed value
			file.write(f"\t{'Method Invocations' if PROCESS_CLASSES else 'Methods Invoked Qty'}: {value['method_invoked']}\n") # Write the 'Method Invocations' if PROCESS_CLASS, else 'Methods Invoked Qty' value
			file.write(f"\n") # Write a new line

def get_clean_id(id):
	"""
	Receives an id and verifies if it contains slashes, if so, it returns the id without the slashes.

	:param id: ID of the class or method to be analyzed
	:return: ID of the class or method to be analyzed without the slashes
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Getting the clean id for {BackgroundColors.CYAN}{id}{BackgroundColors.GREEN}...{Style.RESET_ALL}")
	
	# If the id contains slashes, remove them
	if "/" in id:
		return str(id.split("/")[0:-1])[2:-2] # Return the id without the slashes
	else: # If the id does not contain slashes, simply return the id
		return id # Return the id

def verify_refactoring_file(refactoring_file_path):
	"""
	Validates if the refactoring file was created successfully.

	:param refactoring_file_path: The path to the refactoring file
	:return: A tuple (bool, str) where the bool indicates if the file is valid, and the str provides a message.
	"""

	# Verify if the file exists
	if not os.path.isfile(refactoring_file_path):
		return False, "File does not exist."

	# Verify if the file is not empty
	if os.path.getsize(refactoring_file_path) == 0:
		return False, "File is empty."

	# Try to load the JSON content of the file
	try:
		with open(refactoring_file_path, "r") as file:
			data = json.load(file)
	except json.JSONDecodeError:
		return False, "File contains invalid JSON."

	# If all checks pass, the file is considered valid
	return True, "File is valid."

def generate_refactoring_file(repository_name, commit_hash, refactoring_file_path):
	"""
	Generates the refactoring file for a specific commit hash in a specific repository.

	:param repository_name: The name of the repository
	:param commit_hash: The commit hash of the current linear regression
	:param refactoring_file_path: The path to the refactoring file
	:return: The refactoring file path
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Generating the refactoring file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	# Create the "refactorings" directory if it does not exist
	relatively_refactorings_directory_path = f"{RELATIVE_REFACTORINGS_DIRECTORY_PATH}/{repository_name}"
	full_refactorings_directory_path = f"{START_PATH}/{relatively_refactorings_directory_path}"
	create_directory(full_refactorings_directory_path, relatively_refactorings_directory_path)

	# Verify if the refactoring file exists
	if not verify_file(refactoring_file_path) or os.path.getsize(refactoring_file_path) == 0: # If the refactoring file does not exist
		# Determine the system's null device to discard output
		null_device = "NUL" if platform.system() == "Windows" else "/dev/null"

		setup_repository(repository_name, DEFAULT_REPOSITORIES[repository_name])
		
		# Run RefactoringMiner to get the refactoring data, hiding its output
		command = f"{RELATIVE_REFACTORING_MINER_DIRECTORY_PATH} -c .{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/{repository_name} {commit_hash} -json {refactoring_file_path} >{null_device} 2>&1"
		os.system(command) # Run the command to get the RefactoringMiner data

	# Verify if the refactoring file was properly generated
	is_valid, message = verify_refactoring_file(refactoring_file_path)

	if is_valid: # If the refactoring file was properly generated
		return refactoring_file_path # Return the refactoring file path
	else:
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
	
	# Define the refactoring file path
	refactoring_file_path = f"{FULL_REFACTORINGS_DIRECTORY_PATH}/{repository_name}/{commit_number}-{commit_hash}{REFACTORING_MINER_JSON_FILE_EXTENSION}"

	# Generate the refactoring file if it does not exist or is empty
	if not verify_file(refactoring_file_path) or os.path.getsize(refactoring_file_path) == 0:
		generate_refactoring_file(repository_name, commit_hash, refactoring_file_path)

	# Initialize the dictionary to hold file paths and their corresponding refactoring types
	refactorings_by_filepath = {}

	# Open and read the refactoring file
	with open(refactoring_file_path, "r") as file:
		data = json.load(file) # Load the JSON data
		# Loop through the refactorings in the data
		for commit in data["commits"]:
			if commit["sha1"] == commit_hash: # Verify if the commit hash matches the specified one
				for refactoring in commit["refactorings"]: # Loop through the refactorings in the commit
					for location in refactoring["leftSideLocations"] + refactoring["rightSideLocations"]: # Combine and loop through both left and right side locations
						# Verify if the class name is in the file path
						simplified_class_name = class_name.split("$")[0].replace(".", "/") # Simplify the class name and adapt it to the path format
						if simplified_class_name in location["filePath"]:
							# If the file path is already in the dictionary, append the refactoring type to its list
							if location["filePath"] not in refactorings_by_filepath:
								refactorings_by_filepath[location["filePath"]] = {} # Initialize the dictionary for the file path
							refactoring_type = refactoring["type"] # Get the refactoring type
							if refactoring_type not in refactorings_by_filepath[location["filePath"]]: # If the refactoring type is not in the dictionary, add it
								refactorings_by_filepath[location["filePath"]][refactoring_type] = 0 # Initialize the refactoring type counter
							refactorings_by_filepath[location["filePath"]][refactoring_type] += 1 # Increment the refactoring type counter
							verbose_output(true_string=f"Refactoring: {json.dumps(refactoring, indent=4)}")

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
	if PROCESS_CLASSES:
		expected_header = ["Class", "Type", f"From {metric_name}", f"To {metric_name}", "Percentual Variation", "Commit Number", "Commit Hash", "Method Invocations", "Refactoring Patterns"]
	else:
		expected_header = ["Class", "Method", f"From {metric_name}", f"To {metric_name}", "Percentual Variation", "Commit Number", "Commit Hash", "Methods Invoked Qty", "Refactoring Patterns"]
	
	if verify_file(csv_filename): # If the file exists
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

def verify_substantial_metric_decrease(metrics_values, class_name, raw_variable_attribute, commit_hashes, occurrences, metric_name, repository_name):
	"""
	Verifies if the class or method has had a substantial decrease in the current metric.

	:param metrics_values: A list containing the metrics values for linear regression
	:param class_name: The class name of the current linear regression
	:param raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
	:param commit_hashes: The commit hashes list for the specified class_name
	:param occurrences: The occurrences counter of the class_name
	:param metric_name: The name of the metric
	:param repository_name: The name of the repository
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the class or method has had a substantial decrease in the {BackgroundColors.CYAN}{metric_name}{BackgroundColors.GREEN} metric...{Style.RESET_ALL}")

	if any(keyword.lower() in class_name.lower() for keyword in IGNORE_CLASS_NAME_KEYWORDS):
		return # If any of the class name ignore keywords is found in the class name, return

	if any(keyword.lower() in raw_variable_attribute.lower() for keyword in IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS):
		return # If any of the variable/attribute ignore keywords is found in the variable attribute, return
	
	folder_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/" # The folder path
	csv_filename = f"{folder_path}{SUBSTANTIAL_CHANGES_FILENAME}" # The csv file name

	global FIRST_SUBSTANTIAL_CHANGE_VERIFICATION # Declare that we're using the global variable
	
	# Verify if it's the first run and if the CSV file already exists
	if FIRST_SUBSTANTIAL_CHANGE_VERIFICATION and verify_file(csv_filename):
		FIRST_SUBSTANTIAL_CHANGE_VERIFICATION = False # Update the flag after handling the first run
		os.remove(csv_filename) # Remove the CSV file if it exists

	# Add the header if the file is newly created
	if not verify_file(csv_filename):
		add_csv_header(csv_filename, metric_name)

	biggest_change = [0, 0, 0.00] # The biggest change values in the metric [from, to, percentual_variation]
	commit_data = ["", "", "", ""] # The commit data [from_commit_number, from_commit_hash, to_commit_number, to_commit_hash]

	# Loop through the metrics values
	for i in range(1, len(metrics_values)):
		# Verify if the current metric is bigger than the previous metric or the previous metric is zero
		if metrics_values[i] >= metrics_values[i - 1] or metrics_values[i - 1] == 0:
			continue # If the current metric is bigger than the previous metric or the previous metric is zero, then continue

		# Calculate the current percentual variation
		current_percentual_variation = round((metrics_values[i - 1] - metrics_values[i]) / metrics_values[i - 1], 3)

		# If the current percentual variation is bigger than the desired decrease, then update the biggest_change list
		if current_percentual_variation > DESIRED_DECREASE and current_percentual_variation > biggest_change[2]:
			# Fetch commit data to retrieve refactoring information
			temp_commit_data = [commit_hashes[i - 1], commit_hashes[i]] # The commit data [from_commit_hash, to_commit_hash]
			refactorings_info = get_refactoring_info(repository_name, temp_commit_data[1].split("-")[0], temp_commit_data[1].split("-")[1], class_name)

			# Verify if we're not filtering by desired refactorings or if the current refactoring type is a desired refactoring.
			if not DESIRED_REFACTORINGS_ONLY or any(refactoring in DESIRED_REFACTORINGS for refactoring_list in refactorings_info.values() for refactoring in refactoring_list):
				refactorings_summary = convert_refactorings_dictionary_to_string(refactorings_info) # Convert the refactorings dictionary into a string

				# Update the biggest_change list and commit data only if the conditions above are met.
				biggest_change = [metrics_values[i - 1], metrics_values[i], current_percentual_variation, refactorings_summary.replace("'", "")]
				commit_data = [temp_commit_data[0].split("-")[0], temp_commit_data[0].split("-")[1], temp_commit_data[1].split("-")[0], temp_commit_data[1].split("-")[1]] # Splitting commit hash to get commit number and hash

	# Write the biggest change to the csv file if the percentual variation is bigger than the desired decrease and refactorings were found
	if biggest_change[2] > DESIRED_DECREASE and biggest_change[3]:
		with open(f"{csv_filename}", "a") as csvfile: # Open the csv file
			writer = csv.writer(csvfile) # Create the csv writer
			# Write the class name, the variable attribute, the biggest change values, the commit data and the refactorings information to the csv file
			writer.writerow([class_name, raw_variable_attribute, biggest_change[0], biggest_change[1], round(biggest_change[2] * 100, 2), f"{commit_data[0]} -> {commit_data[2]}", f"{commit_data[1]} -> {commit_data[3]}", occurrences, biggest_change[3]])
	 
def linear_regression_graphics(metrics, class_name, variable_attribute, commit_hashes, occurrences, raw_variable_attribute, repository_name):
	"""
	Perform linear regression on the given metrics and save the plot to a PNG file.

	:param metrics: A list containing the metrics values for linear regression
	:param class_name: The class name of the current linear regression
	:param variable_attribute: The variable attribute (class type or method name) of the current linear regression
	:param commit_hashes: A list of the commit_hashes for the specified class_name/identifier.
	:param occurrences: The number of occurrences of the class or method
	:param raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
	:param repository_name: The name of the repository
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Performing linear regression on the given metrics and saving the plot to a PNG file for {BackgroundColors.CYAN}{class_name}{BackgroundColors.GREEN} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
	
	# Verify for empty metrics list
	if not metrics and VERBOSE:
		print(f"{BackgroundColors.RED}Metrics list for {class_name} {variable_attribute} is empty!{Style.RESET_ALL}")
		return
	
	try:
		metrics_array = np.array(metrics, dtype=float) # Safely convert to NumPy array for flexibility in handling
	except:
		verbose_output(true_string=f"{BackgroundColors.RED}Error converting the {BackgroundColors.CYAN}metrics{BackgroundColors.GREEN} to {BackgroundColors.CYAN}NumPy array{BackgroundColors.GREEN} for {class_name} {variable_attribute}.{Style.RESET_ALL}")
		return

	# Verify for invalid values in the metrics
	if metrics_array.ndim != 2 or metrics_array.shape[1] < len(METRICS_POSITION):
		verbose_output(true_string=f"{BackgroundColors.RED}Metrics structure for {class_name} {variable_attribute} is not as expected!{Style.RESET_ALL}")
		return # Return if the metrics structure is not as expected
	
	# Loop through the metrics_position dictionary
	for metric_name, metric_position in METRICS_POSITION.items():
		# Extract the metrics values
		commit_number = np.arange(metrics_array.shape[0]) # Create the commit number array
		if not commit_number.any(): # If the commit number is empty
			continue # Ignore the current iteration, since there are no commit numbers, thus no linear regression can be performed
		metric_values = metrics_array[:, metric_position] # Extract the metrics values from the metrics array in the specified position (column)

		# For the CBO metric, verify if there occurred any substantial decrease in the metric
		if metric_name == SUBSTANTIAL_CHANGE_METRIC:
			verify_substantial_metric_decrease(metric_values, class_name, raw_variable_attribute, commit_hashes, occurrences, metric_name, repository_name)
			
		# Verify for sufficient data points for regression
		if len(commit_number) < 2 or len(metric_values) < 2:
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

		# Create the Class/Method linear prediction directory if it does not exist
		relative_metrics_prediction_directory_path = f"{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}"
		full_metrics_prediction_directory_path = f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}"
		create_directory(full_metrics_prediction_directory_path, relative_metrics_prediction_directory_path)

		# Save the plot to a PNG file
		plt.savefig(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}/{metric_name}{PNG_FILE_EXTENSION}")
		
		# Close the plot
		plt.close()

def write_metrics_evolution_to_csv(repository_name, metrics_track_record):
	"""
	Writes the metrics evolution to a csv file.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the metrics evolution for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to a csv file...{Style.RESET_ALL}")
	
	# For every identifier in the metrics_track_record, store each metrics values tuple in a row of the csv file
	with tqdm(total=len(metrics_track_record), unit=f" {BackgroundColors.CYAN}Creating Linear Regression and Metrics Evolution{Style.RESET_ALL}") as progress_bar:
		for identifier, record in metrics_track_record.items(): # For each identifier and record in the metrics_track_record dictionary
			metrics = record["metrics"] # Get the metrics list
			class_name = identifier.split(" ")[0] # Get the identifier which is currently the class name
			variable_attribute = get_clean_id(identifier.split(" ")[1]) # Get the variable attribute which could be the type of the class or the method name
			full_metrics_evolution_directory_path = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/" # The path to the directory where the csv file will be stored
			create_directory(full_metrics_evolution_directory_path, f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}") # Create the directory where the csv file will be stored
			metrics_filename = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}"

			# Open the csv file and write the metrics to it
			with open(metrics_filename, "w") as csvfile: 
				writer = csv.writer(csvfile) # Create the csv writer
				if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
					unique_identifier = class_name # The unique identifier is the class name
					writer.writerow(["Class", "Commit Hash", "CBO", "WMC", "RFC", "Method Invocations"]) # Write the header to the csv file
				else: # If the PROCESS_CLASSES constant is set to False
					unique_identifier = variable_attribute # The unique identifier is the method name
					writer.writerow(["Method", "Commit Hash", "CBO", "WMC", "RFC", "Methods Invoked Qty"]) # Write the header to the csv file
				
				# Get the len of the metrics list
				metrics_len = len(metrics)
				for i in range(metrics_len): # For each metric in the metrics list
					# Write the unique identifier, the commit hash, and the metrics to the csv file
					writer.writerow([unique_identifier, record["commit_hashes"][i], metrics[i][0], metrics[i][1], metrics[i][2], record["method_invoked"]])

			# Perform linear regression and generate graphics for the metrics
			linear_regression_graphics(metrics, class_name, variable_attribute, record["commit_hashes"], record["method_invoked"], identifier.split(" ")[1], repository_name)
			progress_bar.update(1) # Update the progress bar

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

	verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating the minimum, maximum, average, and third quartile of each metric and writing it to a csv file for {BackgroundColors.CYAN}{id}{BackgroundColors.GREEN}...{Style.RESET_ALL}")
	
	cboMin = round(float(min(metrics_values[0])), 3) # The minimum cbo value rounded to 3 decimal places
	cboMax = round(float(max(metrics_values[0])), 3) # The maximum cbo value rounded to 3 decimal places
	cboAvg = round(float(sum(metrics_values[0])) / len(metrics_values[0]), 3) # The average cbo value rounded to 3 decimal places
	cboQ3 = round(float(np.percentile(metrics_values[0], 75)), 3) # The third quartile cbo value rounded to 3 decimal places

	wmcMin = round(float(min(metrics_values[1])), 3) # The minimum wmc value rounded to 3 decimal places
	wmcMax = round(float(max(metrics_values[1])), 3) # The maximum wmc value rounded to 3 decimal places
	wmcAvg = round(float(sum(metrics_values[1])) / len(metrics_values[1]), 3) # The average wmc value rounded to 3 decimal places
	wmcQ3 = round(float(np.percentile(metrics_values[1], 75)), 3) # The third quartile wmc value rounded to 3 decimal places
	
	rfcMin = round(float(min(metrics_values[2])), 3) # The minimum rfc value rounded to 3 decimal places
	rfcMax = round(float(max(metrics_values[2])), 3) # The maximum rfc value rounded to 3 decimal places
	rfcAvg = round(float(sum(metrics_values[2])) / len(metrics_values[2]), 3) # The average rfc value rounded to 3 decimal places
	rfcQ3 = round(float(np.percentile(metrics_values[2], 75)), 3) # The third quartile rfc value rounded to 3 decimal places

	# Write the metrics statistics to the csv file
	csv_writer.writerow([id, key, metrics["changed"], cboMin, cboMax, cboAvg, cboQ3, wmcMin, wmcMax, wmcAvg, wmcQ3, rfcMin, rfcMax, rfcAvg, rfcQ3, first_commit_hash, last_commit_hash, metrics["method_invoked"]])

def generate_metrics_track_record_statistics(repository_name, metrics_track_record):
	"""
	Processes the metrics in metrics_track_record to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file.

	:param repository_name: The name of the repository
	:param metrics_track_record: A dictionary containing the metrics of each class or method
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the metrics in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository to calculate the minimum, maximum, average, and third quartile of each metric and writing it to a csv file...{Style.RESET_ALL}")
	
	# Open the csv file and process the metrics of each method
	unsorted_metrics_filename = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}"
	with open(unsorted_metrics_filename, "w") as csvfile:
		writer = csv.writer(csvfile)	
		if PROCESS_CLASSES: # If the PROCESS_CLASSES constant is set to True
			# Write the header to the csv file but using the "Type" in the second column
			writer.writerow(["Class", "Type", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash", "Method Invocations"])
		else:
			# Write the header to the csv file but using the "Method" in the second column
			writer.writerow(["Class", "Method", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash", "Methods Invoked Qty"])

		# Loop inside the *metrics["metrics"] in order to get the min, max, avg, and third quartile of each metric (cbo, wmc, rfc)
		with tqdm(total=len(metrics_track_record), unit=f" {BackgroundColors.CYAN}Creating Metrics Statistics{Style.RESET_ALL}") as progress_bar:
			for identifier, metrics in metrics_track_record.items():
				# Verify if the metrics changes is greater than the minimum changes
				if metrics["changed"] < MINIMUM_CHANGES:
					continue # If the metrics changes is less than the minimum changes, then jump to the next iteration

				metrics_values = [] # This stores the metrics values in a list of lists of each metric
				for i in range(0, NUMBER_OF_METRICS): # For each metric in the metrics list
					# This get the metrics values of each metric occurence in the method in order to, later on, be able to get the min, max, avg, and third quartile of each metric
					metrics_values.append([sublist[i] for sublist in metrics["metrics"]])

				# Split the identifier to get the id and key which is separated by a space
				id = identifier.split(" ")[0] # Get the id of the method
				key = identifier.split(" ")[1] # Get the key of the method

				# Create a function to get the min, max, avg, and third quartile of each metric, the first commit hash and the last commit hash, and then write it to the csv file
				write_method_metrics_statistics(writer, id, key, metrics, metrics_values, metrics_track_record[identifier]["commit_hashes"][0], metrics_track_record[identifier]["commit_hashes"][-1])
				progress_bar.update(1) # Update the progress bar

def sort_csv_by_changes(repository_name):
	"""
	Sorts the csv file according to the number of changes.

	:param repository_name: The name of the repository
	:return: None
	"""
	
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}metrics statistics files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}number of changes{BackgroundColors.GREEN}.{Style.RESET_ALL}")

	# Define the unsorted csv file path
	unsorted_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}" # The unsorted csv file path

	# Verify if the unsorted csv file exists
	if not verify_file(unsorted_csv_file_path):
		verbose_output(true_string=f"{BackgroundColors.RED}The unsorted csv file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository does not exist.{Style.RESET_ALL}")
		return # Return if the unsorted csv file does not exist

	# Read the csv file
	data = pd.read_csv(unsorted_csv_file_path)
	
	# Verify if the DataFrame is empty after the header
	if data.empty:
		verbose_output(true_string=f"{BackgroundColors.RED}The unsorted csv file for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository is empty after the header.{Style.RESET_ALL}")
		return # Return if the file is empty after the header
	
	# Sort the csv file by the number of changes
	data = data.sort_values(by=["Changed"], ascending=False)
	
	# Define the sorted csv file path
	sorted_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SORTED_CHANGED_METHODS_CSV_FILENAME}" # The sorted csv file path
	
	# Write the sorted csv file to a new csv file
	data.to_csv(sorted_csv_file_path, index=False)

def sort_csv_by_percentual_variation(repository_name):
	"""
	Sorts the csv file according to the percentual variation of the metric.

	:param repository_name: The name of the repository
	:return: None
	"""
	
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}interesting changes files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}percentual variation of the metric{BackgroundColors.GREEN}.{Style.RESET_ALL}")

	# Read the csv file
	data = pd.read_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}")
	# Sort the csv file by the percentual variation of the metric
	data = data.sort_values(by=["Percentual Variation"], ascending=False)
	# Write the sorted csv file to a new csv file
	data.to_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}", index=False)

def read_csv_as_dict(file_path):
	"""
	Reads the CSV file into a dictionary format where the key is the repository name.
	
	:param file_path: Path to the CSV file
	:return: Dictionary containing repository data
	"""

	repository_data = {} # Initialize the dictionary to hold the repository data
	if os.path.exists(file_path): # If the file path exists
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
	else:
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
		writer.writerow(["Repository Name", "Number of Classes", "Lines of Code (LOC)", "Number of Commits", "Execution Time (Minutes)", "Size (GB)"])
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

	# Read the existing CSV data
	repositories_attributes = read_csv_as_dict(FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH)

	if repository_name in repositories_attributes:
		# Update the attributes for the specified repository
		repositories_attributes[repository_name]["execution_time_in_minutes"] = round(repositories_attributes[repository_name]["execution_time_in_minutes"] + elapsed_time / 60, 2)
		repositories_attributes[repository_name]["size_in_gb"] += get_output_directories_size_in_gb(repository_name, OUTPUT_DIRECTORIES)
	else:
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} repository was not found in the {BackgroundColors.CYAN}repositories attributes{BackgroundColors.RED} file.{Style.RESET_ALL}")
		return # Return if the repository was not found in the repositories attributes file

	return repositories_attributes # Return the updated repositories attributes

def process_repository(repository_name):
	"""
	Processes the specified repository.

	:param repository_name: The name of the repository to be analyzed
	:return: None
	"""

	# Start the timer
	start_time = time.time()

	# Verify if the ck metrics were already calculated, which are the source of the data processed by traverse_directory(repository_ck_metrics).
	if not verify_ck_metrics_folder(repository_name):
		print(f"{BackgroundColors.RED}The metrics for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} were not calculated. Please run the {BackgroundColors.CYAN}code_metrics.py{BackgroundColors.RED} file first{Style.RESET_ALL}")
		return # Return if the ck metrics were not calculated

	# Get the directory path for the specified repository name
	repository_ck_metrics_path = get_directory_path(repository_name)
	
	# Create the desired directory if it does not exist
	create_directories(repository_name)

	# Traverse the directory and get the method metrics
	metrics_track_record = traverse_directory(repository_name, repository_ck_metrics_path)

	# Sort the commit_hashes list for each entry in the metrics_track_record dictionary by the commit number
	sorted_metrics_track_record = sort_commit_hashes_by_commit_number(metrics_track_record)

	# Write the metrics_track_record to a txt file
	write_metrics_track_record_to_txt(repository_name, sorted_metrics_track_record)

	# Write, for each identifier, the metrics evolution values to a csv file
	write_metrics_evolution_to_csv(repository_name, sorted_metrics_track_record)

	# Generate the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
	generate_metrics_track_record_statistics(repository_name, sorted_metrics_track_record)

	# Sort the csv file by the number of changes
	sort_csv_by_changes(repository_name)

	# Remove the old csv file
	old_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}"
	os.remove(old_csv_file_path)

	# Sort the interesting changes csv file by the percentual variation of the metric
	sort_csv_by_percentual_variation(repository_name)

	# Output the elapsed time to process this repository
	elapsed_time = time.time() - start_time # Calculate the elapsed time

	repositories_attributes = update_repository_attributes(repository_name, elapsed_time) # Update the attributes of the repositories file with the elapsed time and output data size in GB
	write_dict_to_csv(FULL_REPOSITORIES_ATTRIBUTES_FILE_PATH, repositories_attributes) # Write the updated data back to the CSV file

	elapsed_time_string = f"Time taken to generate the {BackgroundColors.CYAN}metrics evolution records, metrics statistics and linear regression{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS}{BackgroundColors.GREEN} in {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
	output_time(elapsed_time_string, round(elapsed_time, 2)) # Output the elapsed time

def process_all_repositories():
	"""
	Processes all the repositories in the DEFAULT_REPOSITORIES_NAMES list.

	:return: None
	"""

	for repository_name in DEFAULT_REPOSITORIES_NAMES: # Loop through the DEFAULT_REPOSITORY_NAME list
		print(f"") # Print an empty line
		print(f"{BackgroundColors.GREEN}Processing the {BackgroundColors.CYAN}metrics evolution history, metrics statistics, linear regression, substantial changes and refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS}{BackgroundColors.GREEN} from the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
		process_repository(repository_name) # Process the current repository
		print(f"\n------------------------------------------------------------") # Print a separator

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

def main():
	"""
   Main function.

   :return: None
   """
   
	# Verify if the path constants contains whitespaces
	if path_contains_whitespaces():
		print(f"{BackgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
		return # Exit the program
	
	global SOUND_FILE_PATH # Declare the SOUND_FILE_PATH as a global variable
	SOUND_FILE_PATH = update_sound_file_path() # Update the sound file path
	
	# Verify if the refactoring miner tool exists in the specified path
	if not verify_file(RELATIVE_REFACTORING_MINER_DIRECTORY_PATH):
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}RefactoringMiner{BackgroundColors.RED} tool was not found in the specified path: {BackgroundColors.GREEN}{RELATIVE_REFACTORING_MINER_DIRECTORY_PATH}{Style.RESET_ALL}")
		return # Exit the program

	verify_and_update_repositories() # Verify and update the repositories

	# Print the welcome message
	print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Metrics Changes Generator{BackgroundColors.GREEN}! This script is part of the {BackgroundColors.CYAN}Worked Example Miner (WEM){BackgroundColors.GREEN} project.{Style.RESET_ALL}")
	print(f"{BackgroundColors.GREEN}This script generates the {BackgroundColors.CYAN}classes or methods metrics evolution history, metrics statistics, linear regression, substantial changes and refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{list(DEFAULT_REPOSITORIES_NAMES)}{BackgroundColors.GREEN} repositories based on the {BackgroundColors.CYAN}ck metrics files, the commit hashes list file and the diffs of each commit{BackgroundColors.GREEN} generated by the {BackgroundColors.CYAN}./code_metrics.py{BackgroundColors.GREEN} code.{Style.RESET_ALL}")
	print(f"{BackgroundColors.RED}This Python code avoids using threads due to its high memory usage. It stores metric values, generates regression graphs, and detects substantial changes, which demands a lot of RAM.{Style.RESET_ALL}\n")

	# Prompt the user with a timeout
	user_response = input_with_timeout(f"{BackgroundColors.GREEN}Do you want to process the {BackgroundColors.CYAN}class.csv{BackgroundColors.GREEN} file {BackgroundColors.RED}(True/False){BackgroundColors.GREEN}? {Style.RESET_ALL}", 60)
	
	if user_response is None:
		# No input received within timeout
		print(f"{BackgroundColors.RED}No input received within the timeout. Processing both classes and methods.{Style.RESET_ALL}")
		process_classes_and_methods() # Process both classes and methods
	else:
		process_based_on_user_input(user_response) # Process based on user input

	# Output the message that the Metrics Changes Generator has finished
	print(f"\n{BackgroundColors.GREEN}The {BackgroundColors.CYAN}Metrics Changes Generator{BackgroundColors.GREEN} has finished processing the {BackgroundColors.CYAN}classes or methods metrics evolution history, metrics statistics and linear regression, substantial changes and refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{list(DEFAULT_REPOSITORIES_NAMES)}{BackgroundColors.GREEN} repositories.{Style.RESET_ALL}")
		
if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
