# @TODO: In the verify_substantial_metric_decrease function, also add a column with the refactor type identified for that commit hash (sha1) and class_name (codeElement) from RefactoringMiner.
# @TODO: Also, create a list to use as filter for only writing in the CSV of the substantial changes specific refactorings of interest ("Extract Method", "Extract Class", "Pull Up Method", "Push Down Method", "Extract Superclass", "Move Method").

import atexit # For playing a sound when the program finishes
import csv # for reading csv files
import matplotlib.pyplot as plt # for plotting the graphs
import numpy as np # for calculating the min, max, avg, and third quartile of each metric
import os # for walking through directories
import pandas as pd # for the csv file operations
import time # For measuring the time
from colorama import Style # For coloring the terminal
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from sklearn.linear_model import LinearRegression # for the linear regression
from tqdm import tqdm # for progress bar

# Import from the main.py file
from code_metrics import BackgroundColors # For coloring the terminal outputs
from code_metrics import START_PATH, CK_METRICS_FILES, CSV_FILE_EXTENSION, DEFAULT_REPOSITORIES, FULL_CK_METRICS_DIRECTORY_PATH, FULL_REPOSITORIES_DIRECTORY_PATH # Importing constants from the code_metrics.py file
from code_metrics import create_directory, output_time, path_contains_whitespaces, play_sound, verify_ck_metrics_folder # Importing functions from the code_metrics.py file

# CONSTANTS:
PROCESS_CLASSES = input(f"{BackgroundColors.GREEN}Do you want to process the {BackgroundColors.CYAN}class.csv{BackgroundColors.GREEN} file {BackgroundColors.RED}(True/False){BackgroundColors.GREEN}? {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 3 # The number of metrics
DESIRED_DECREASED = 0.20 # The desired decreased in the metric
IGNORE_CLASS_NAME_KEYWORDS = ["test"] # The keywords to ignore in the class name
IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS = ["anonymous"] # The keywords to ignore in the variable attribute
SUBSTANTIAL_CHANGE_METRIC = "CBO" # The desired metric to check for substantial changes
DEFAULT_REPOSITORY_NAMES = list(DEFAULT_REPOSITORIES.keys()) # The default repository names
METRICS_POSITION = {"CBO": 0, "WMC": 1, "RFC": 2}

# Extensions:
PNG_FILE_EXTENSION = ".png" # The extension of the PNG files

# Filenames:
CK_CSV_FILE = CK_METRICS_FILES[0] if PROCESS_CLASSES else CK_METRICS_FILES[1] # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
UNSORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_unsorted_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the top changed methods
SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the sorted top changed methods
SUBSTANTIAL_CHANGES_FILENAME = f"substantial_{SUBSTANTIAL_CHANGE_METRIC}_{CLASSES_OR_METHODS}_changes{CSV_FILE_EXTENSION}" # The relative path to the directory containing the interesting changes
RELATIVE_METRICS_DATA_DIRECTORY_PATH = "/metrics_data" # The relative path to the directory containing the metrics evolution
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution" # The relative path to the directory containing the metrics evolution
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics" # The relative path to the directory containing the metrics statistics
RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH = "/metrics_predictions" # The relative path to the directory containing the metrics prediction

# Directories Paths:
FULL_METRICS_DATA_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_DATA_DIRECTORY_PATH}" # The full path to the directory containing the metrics evolution
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics evolution
FULL_METRICS_STATISTICS_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}" # The full path to the directory containing the metrics statistics
FULL_METRICS_PREDICTION_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics prediction

# @brief: This function loops through the DEFAULT_REPOSITORY_NAME list and calls the process_repository function for each repository
# @param: None
# @return: None
def process_all_repositories():
	for repository_name in DEFAULT_REPOSITORY_NAMES: # Loop through the DEFAULT_REPOSITORY_NAME list
		print(f"")
		print(f"{BackgroundColors.GREEN}Processing the {BackgroundColors.CYAN}{CLASSES_OR_METHODS} metrics evolution history, metrics statistics and linear regression{BackgroundColors.GREEN} for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
		process_repository(repository_name) # Process the current repository
		print(f"------------------------------------------------------------")

# @brief: This function call the procedures to process the specified repository
# @param: repository_name: The name of the repository to be analyzed 
# @return: None
def process_repository(repository_name):
	# Start the timer
	start_time = time.time()

	# Verify if the ck metrics were already calculated, which are the source of the data processed by traverse_directory(repository_ck_metrics).
	if not verify_ck_metrics_folder(repository_name):
		print(f"{BackgroundColors.RED}The metrics for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.RED} were not calculated. Please run the {BackgroundColors.CYAN}code_metrics.py{BackgroundColors.RED} file first{Style.RESET_ALL}")
		return

	# Get the directory path for the specified repository name
	repository_ck_metrics_path = get_directory_path(repository_name)
	
	# Create the desired directory if it does not exist
	create_directories(repository_name)

	# Traverse the directory and get the method metrics
	metrics_track_record = traverse_directory(repository_name, repository_ck_metrics_path)

	# Loop through the metrics_track_record and sort the commit hashes list for each class or method
	for key in metrics_track_record:
		# Sort the commit hashes list for each class or method
		metrics_track_record[key]["commit_hashes"].sort(key=lambda x: int(x.split("-")[0]))

	# Write the metrics_track_record to a txt file
	write_metrics_track_record_to_txt(repository_name, metrics_track_record)

	# Write, for each identifier, the metrics evolution values to a csv file
	write_metrics_evolution_to_csv(repository_name, metrics_track_record)

	# Generate the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
	generate_metrics_track_record_statistics(repository_name, metrics_track_record)

	# Sort the csv file by the number of changes
	sort_csv_by_changes(repository_name)

	# Remove the old csv file
	old_csv_file_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}"
	os.remove(old_csv_file_path)

	# Sort the interesting changes csv file by the percentual variation of the metric
	sort_csv_by_percentual_variation(repository_name)

	# Output the elapsed time to process this repository
	elapsed_time = time.time() - start_time
	elapsed_time_string = f"Time taken to generate the {BackgroundColors.CYAN}metrics evolution records, metrics statistics and linear regression{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{CLASSES_OR_METHODS}{BackgroundColors.GREEN} in {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
	output_time(elapsed_time_string, round(elapsed_time, 2))

# @brief: Gets the path to the directory of the CK metrics related to the repository
# @param: repository_name
# @return: The path to the directory of the CK metrics related to the repository
def get_directory_path(repository_name):
	repository_ck_metrics_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}"
	return repository_ck_metrics_path

# @brief: This function create all the desired directories
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def create_directories(repository_name):
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

# @brief: Validate the class name, that is, if it contains any dots in the name
# @param class_name: The name of the class
# @return: True if the class name is valid, False otherwise
def valid_class_name(class_name):
	return "." in class_name

# @brief: Gets the package name of the class, which is, get the substring between that starts with "/src/"(excluded) until the last dot(excluded)
# @param file_name: The file name where the class is located
# @return: The package name of the class
def get_class_package_name(file_name):
	start_substring = "/src/"
	package_name = file_name[file_name.find(start_substring) + len(start_substring):file_name.rfind(".")]

	# Replace the slashes with dots
	package_name = package_name.replace("/", ".")

	return package_name

# @brief: Gets the identifier and metrics of the method or class from the row
# @param row: The row of the csv file
# @return: The identifier and metrics of the method or class
def get_identifier_and_metrics(row):
	class_name = row["class"]
	if PROCESS_CLASSES:
		if not valid_class_name(class_name):
			class_name = get_class_package_name(row["file"])
		variable_attribute = row["type"]
	else:
		variable_attribute = row["method"]

	cbo = float(row["cbo"])
	wmc = float(row["wmc"])
	rfc = float(row["rfc"])

	# Create a tuple containing the metrics
	metrics = (cbo, wmc, rfc)
	identifier = f"{class_name} {variable_attribute}"

	return identifier, metrics

# @brief: Checks if the file was modified
# @param commit_dict: A dictionary containing the commit hashes as keys and the commit objects as values
# @param commit_hash: The commit hash of the current row
# @param row: The row of the csv file
# @return: True if the file was modified, False otherwise
def was_file_modified(commit_dict, commit_hash, row):	
	# The file_path is the substring that comes after the: FULL_REPOSITORIES_DIRECTORY_PATH/repository_name/
	file_path = row["file"][row["file"].find(FULL_REPOSITORIES_DIRECTORY_PATH) + len(FULL_REPOSITORIES_DIRECTORY_PATH) + 1:]
	repository_name = file_path.split('/')[0]
	file_path = file_path[len(repository_name) + 1:] # Get the substring that comes after the: repository_name/
			
	modified_files_paths = commit_dict[commit_hash]
	for modified_file_path in modified_files_paths:
		# If the modified file path is equal to the file path, then the file was modified
		if modified_file_path == file_path:
			return True # The file was modified
	return False # The file was not modified

# @brief: Processes a csv file containing the metrics of a method nor class
# @param commit_dict: A dictionary containing the commit hashes as keys and the commit objects as values
# @param file_path: The path to the csv file
# @param metrics_track_record: A dictionary containing the track record of the metrics of each method nor class
# @return: None
def process_csv_file(commit_dict, file_path, metrics_track_record):
	# Open the csv file
	with open(file_path, "r") as csvfile:
		# Read the csv file
		reader = csv.DictReader(csvfile)
		# Iterate through each row, that is, for each method in the csv file
		for row in reader:
			# Get the identifier and metrics of the method
			identifier, ck_metrics = get_identifier_and_metrics(row)

			# If the identifier is not in the dictionary, then add it
			if identifier not in metrics_track_record:
				metrics_track_record[identifier] = {"metrics": [], "commit_hashes": [], "changed": 0}

			# Get the metrics_changes list for the method
			metrics_changes = metrics_track_record[identifier]["metrics"]
			# Get the commit hashes list for the method
			commit_hashes = metrics_track_record[identifier]["commit_hashes"]
			# Get the commit number of the current row (i-commit_hash)
			commit_number = file_path[file_path.rfind("/", 0, file_path.rfind("/")) + 1:file_path.rfind("/")]
			# Get the commit hash of the current row
			commit_hash = commit_number.split("-")[1]

			# Verify if the file in the current row of the file path was actually modified
			if (commit_hash not in commit_hashes or (ck_metrics not in metrics_changes)) and (was_file_modified(commit_dict, commit_hash, row)):
				# Append the metrics to the list
				metrics_changes.append(ck_metrics)
				# Increment the number of changes
				metrics_track_record[identifier]["changed"] += 1
				# Append the commit hash to the list
				commit_hashes.append(commit_number)

# @brief: This function generates the commit dictionary, which is a dictionary containing the modified files for each commit
# @param repository_name: The name of the repository
# @return: A dictionary containing the modified files for each commit
def generate_commit_dict(repository_name):
	commit_dict = {} # A dictionary containing the commit hashes as keys and the commit objects as values

	# Traverse the repository and get the modified files for each commit and store it in the commit_dict
	for commit in Repository(DEFAULT_REPOSITORIES[repository_name]).traverse_commits():
		commit_dict[commit.hash] = [] # Initialize the commit hash list
		for modified_file in commit.modified_files: # For each modified file in the commit
			commit_dict[commit.hash].append(modified_file.new_path) # Append the modified file path to the commit hash list
	return commit_dict

# @brief: Traverses a directory and processes all the csv files
# @param repository_ck_metrics_path: The path to the directory
# @param repository_name: The name of the repository
# @return: A dictionary containing the metrics of each class and method combination
def traverse_directory(repository_name, repository_ck_metrics_path):
	metrics_track_record = {} # Dictionary containing the track record of the metrics of each method nor class. The key is the identifier and the value is a dictionary containing the metrics, commit hashes and the number of times the metrics changed.
	file_count = 0
	progress_bar = None

	commit_dict = generate_commit_dict(repository_name) # A dictionary containing the commit hashes as keys and the commit objects as values

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
						process_csv_file(commit_dict, file_path, metrics_track_record) # Process the csv file
						file_count += 1 # Increment the file count

						if progress_bar is None: # If the progress bar is not initialized
							progress_bar = tqdm(total=file_count) # Initialize the progress bar
						else:
							progress_bar.update(1) # Update the progress bar

	# Close the progress bar
	if progress_bar is not None:
		progress_bar.close()

	# Return the method metrics, which is a dictionary containing the metrics of each method  
	return metrics_track_record

# @brief: This function writes the metrics_track_record to a txt file
# @param: repository_name: The name of the repository
# @param: metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def write_metrics_track_record_to_txt(repository_name, metrics_track_record):
	with open(f"{FULL_METRICS_DATA_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}_track_record.txt", "w") as file:
		for key, value in metrics_track_record.items():
			file.write(f"{key}: \n")
			file.write(f"\tMetrics: {value['metrics']}\n")
			file.write(f"\tCommit Hashes: {value['commit_hashes']}\n")
			file.write(f"\tChanged: {value['changed']}\n")
			file.write(f"\n")

# @brief: This function receives an id and verify if it contains slashes, if so, it returns the id without the slashes
# @param: id: ID of the class or method to be analyzed
# @return: ID of the class or method to be analyzed without the slashes
def get_clean_id(id):
   # If the id contains slashes, remove them
   if "/" in id:
      return str(id.split("/")[0:-1])[2:-2]
   else:
      return id

# @brief: This function verifies if a specified folder exists, if not, it creates it
# @param: folder_path: The path to the folder
# @return: True if the folder already exists, False otherwise
def verify_and_create_folder(folder_path):
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
		return False
	return True

# @brief: This function verifies if a specified file exists
# @param: file_path: The path to the file
# @return: True if the file already exists, False otherwise
def verify_file(file_path):
	return os.path.exists(file_path)

# @brief: This function verifies if the class or method has had a substantial decrease in the current metric
# @param: metrics: A list containing the metrics values for linear regression
# @param: class_name: The class name of the current linear regression
# @param: raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
# @param: commit_hashes: The commit hashes list for the speficied class_name.
# @param: metric_name: The name of the metric
# @param: repository_name: The name of the repository
# @return: None
def verify_substantial_metric_decrease(metrics_values, class_name, raw_variable_attribute, commit_hashes, metric_name, repository_name):
	if any(keyword.lower() in class_name.lower() for keyword in IGNORE_CLASS_NAME_KEYWORDS):
		return # If any of the class name ignore keywords is found in the class name, return

	if any(keyword.lower() in raw_variable_attribute.lower() for keyword in IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS):
		return # If any of the variable/attribute ignore keywords is found in the variable attribute, return
	
	folder_path = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/"
	csv_filename = f"{folder_path}{SUBSTANTIAL_CHANGES_FILENAME}"

	# If the csv folder does not exist, create it
	if not verify_file(csv_filename):
		with open(f"{csv_filename}", "w") as csvfile:
			writer = csv.writer(csvfile)
			if PROCESS_CLASSES:
				writer.writerow(["Class", "Type", f"From {metric_name}", f"To {metric_name}", "Percentual Variation", "Commit Number", "Commit Hash"])
			else:
				writer.writerow(["Class", "Method", f"From {metric_name}", f"To {metric_name}", "Percentual Variation", "Commit Number", "Commit Hash"])

	biggest_change = [0, 0, 0.00] # The biggest change values in the metric
	commit_data = [0, 0] # The commit data [commit_number, commit_hash]

	# Check if the current metric decreased by more than DESIRED_DECREASED in any commit
	for i in range(1, len(metrics_values)):
		if metrics_values[i] >= metrics_values[i - 1] or metrics_values[i - 1] == 0:
			continue # If the current metric is bigger than the previous metric or the previous metric is zero, then continue

		current_percentual_variation = round((metrics_values[i - 1] - metrics_values[i]) / metrics_values[i - 1], 3)
		# If the current percentual variation is bigger than the desired decreased, then update the biggest_change list
		if current_percentual_variation > DESIRED_DECREASED and current_percentual_variation > biggest_change[2]:
			biggest_change = [metrics_values[i - 1], metrics_values[i], current_percentual_variation]
			commit_data = [commit_hashes[i - 1].split("-")[0], commit_hashes[i - 1].split("-")[1]]

	# Write the biggest change to the csv file if the percentual variation is bigger than the desired decreased
	if biggest_change[2] > DESIRED_DECREASED:
		with open(f"{csv_filename}", "a") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([class_name, raw_variable_attribute, biggest_change[0], biggest_change[1], round(biggest_change[2] * 100, 2), commit_data[0], commit_data[1]])
	 
# @brief: Perform linear regression on the given metrics and save the plot to a PNG file
# @param: metrics: A list containing the metrics values for linear regression
# @param: class_name: The class name of the current linear regression
# @param: variable_attribute: The variable attribute (class type or method name) of the current linear regression
# @param: commit_hashes: A list of the commit_hashes for the specified class_name/identifier.
# @param: raw_variable_attribute: The raw variable attribute (class type or method name) of the current linear regression
# @param: repository_name: The name of the repository
# @return: None
def linear_regression_graphics(metrics, class_name, variable_attribute, commit_hashes, raw_variable_attribute, repository_name):
	# Check for empty metrics list
	if not metrics:
		# print(f"{BackgroundColors.RED}Metrics list for {class_name} {variable_attribute} is empty!{Style.RESET_ALL}")
		return

	# Check for invalid values in the metrics
	if np.isnan(metrics).any() or np.isinf(metrics).any():
		print(f"{BackgroundColors.RED}Metrics list for {class_name} {variable_attribute} contains invalid values!{Style.RESET_ALL}")
		return
	
	# Loop through the metrics_position dictionary
	for metric_name, metric_position in METRICS_POSITION.items():
		# Extract the metrics values
		commit_number = np.arange(len(metrics)) # Create an array with the order of the commits numbers
		metric_values = np.array(metrics)[:, metric_position] # Considering the metric in the value variable for linear regression

		# For the CBO metric, check if there occurred any substantial decrease in the metric
		if metric_name == SUBSTANTIAL_CHANGE_METRIC:
			verify_substantial_metric_decrease(metric_values, class_name, raw_variable_attribute, commit_hashes, metric_name, repository_name)
			
		# Check for sufficient data points for regression
		if len(commit_number) < 2 or len(metric_values) < 2:
			return
		
		# Perform linear regression using Scikit-Learn
		model = LinearRegression()
		model.fit(commit_number.reshape(-1, 1), metric_values)
		linear_fit = model.predict(commit_number.reshape(-1, 1))

		# Create the plot
		plt.figure(figsize=(10, 6))
		plt.plot(commit_number, metric_values, "o", label=f"{metric_name}")
		plt.plot(commit_number, linear_fit, "-", label="Linear Regression Fit")
		plt.xlabel("Commit Number")
		plt.ylabel(f"{metric_name} Value")
		plt.title(f"Linear Regression for {metric_name} metric of {class_name} {variable_attribute}")
		plt.legend()

		# Create the Class/Method linear prediction directory if it does not exist
		verify_and_create_folder(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}")

		# Save the plot to a PNG file
		plt.savefig(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}/{metric_name}{PNG_FILE_EXTENSION}")
		
		# Close the plot
		plt.close()
   
# @brief: This function writes the metrics evolution to a csv file
# @param: repository_name: The name of the repository
# @param: metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def write_metrics_evolution_to_csv(repository_name, metrics_track_record):
	# For every identifier in the metrics_track_record, store each metrics values tuple in a row of the csv file
	with tqdm(total=len(metrics_track_record), unit=f" {BackgroundColors.CYAN}Creating Linear Regression and Metrics Evolution{Style.RESET_ALL}") as progress_bar:
		for identifier, record in metrics_track_record.items():
			metrics = record["metrics"]
			class_name = identifier.split(' ')[0] # Get the identifier which is currently the class name
			variable_attribute = get_clean_id(identifier.split(" ")[1]) # Get the variable attribute which could be the type of the class or the method name
			mkdir_path = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/"
			verify_and_create_folder(mkdir_path)
			metrics_filename = f"{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}"
			with open(metrics_filename, "w") as csvfile:
				writer = csv.writer(csvfile)
				if PROCESS_CLASSES:
					unique_identifier = class_name
					writer.writerow(["Class", "Commit Hash", "CBO", "WMC", "RFC"])
				else:
					unique_identifier = variable_attribute
					writer.writerow(["Method", "Commit Hash", "CBO", "WMC", "RFC"])
				
				# get the len of the metrics list
				metrics_len = len(metrics)
				for i in range(metrics_len):
					writer.writerow([unique_identifier, record["commit_hashes"][i], metrics[i][0], metrics[i][1], metrics[i][2]])

			linear_regression_graphics(metrics, class_name, variable_attribute, record["commit_hashes"], identifier.split(" ")[1], repository_name) # Perform linear regression on the metrics
			progress_bar.update(1) # Update the progress bar

# @brief: Calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param csv_writer: The csv writer object
# @param id: The id of the method
# @param key: The key of the method
# @param metrics: The list of metrics
# @param metrics_values: The list of metrics values
# @param first_commit_hash: The first commit hash of the method
# @param last_commit_hash: The last commit hash of the method
# @return: None
def write_method_metrics_statistics(csv_writer, id, key, metrics, metrics_values, first_commit_hash, last_commit_hash):
	cboMin = round(float(min(metrics_values[0])), 3)
	cboMax = round(float(max(metrics_values[0])), 3)
	cboAvg = round(float(sum(metrics_values[0])) / len(metrics_values[0]), 3)
	cboQ3 = round(float(np.percentile(metrics_values[0], 75)), 3)
	wmcMin = round(float(min(metrics_values[1])), 3)
	wmcMax = round(float(max(metrics_values[1])), 3)
	wmcAvg = round(float(sum(metrics_values[1])) / len(metrics_values[1]), 3)
	wmcQ3 = round(float(np.percentile(metrics_values[1], 75)), 3)
	rfcMin = round(float(min(metrics_values[2])), 3)
	rfcMax = round(float(max(metrics_values[2])), 3)
	rfcAvg = round(float(sum(metrics_values[2])) / len(metrics_values[2]), 3)
	rfcQ3 = round(float(np.percentile(metrics_values[2], 75)), 3)

	csv_writer.writerow([id, key, metrics["changed"], cboMin, cboMax, cboAvg, cboQ3, wmcMin, wmcMax, wmcAvg, wmcQ3, rfcMin, rfcMax, rfcAvg, rfcQ3, first_commit_hash, last_commit_hash])

# @brief: Process the metrics in metrics_track_record to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param repository_name: The name of the repository
# @param metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def generate_metrics_track_record_statistics(repository_name, metrics_track_record):
	# Open the csv file and process the metrics of each method
	unsorted_metrics_filename = f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}"
	with open(unsorted_metrics_filename, "w") as csvfile:
		writer = csv.writer(csvfile)	
		if PROCESS_CLASSES:
			writer.writerow(["Class", "Type", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash"])
		else:
			writer.writerow(["Class", "Method", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash"])

		# Loop inside the *metrics["metrics"] in order to get the min, max, avg, and third quartile of each metric (cbo, wmc, rfc)
		with tqdm(total=len(metrics_track_record), unit=f" {BackgroundColors.CYAN}Creating Metrics Statistics{Style.RESET_ALL}") as progress_bar:
			for identifier, metrics in metrics_track_record.items():
				# check if the metrics changes is greater than the minimum changes
				if metrics["changed"] < MINIMUM_CHANGES:
					continue

				# This stores the metrics values in a list of lists of each metric
				metrics_values = []
				for i in range(0, NUMBER_OF_METRICS):
					# This get the metrics values of each metric occurence in the method in order to, later on, be able to get the min, max, avg, and third quartile of each metric
					metrics_values.append([sublist[i] for sublist in metrics["metrics"]])

				# split the identifier to get the id and key which is separated by a space
				id = identifier.split(" ")[0]
				key = identifier.split(" ")[1]

				# Create a function to get the min, max, avg, and third quartile of each metric, the first commit hash and the last commit hash, and then write it to the csv file
				write_method_metrics_statistics(writer, id, key, metrics, metrics_values, metrics_track_record[identifier]["commit_hashes"][0], metrics_track_record[identifier]["commit_hashes"][-1])
				progress_bar.update(1) # Update the progress bar

# @brief: This function sorts the csv file according to the number of changes
# @param: repository_name: The name of the repository
# @return: None
def sort_csv_by_changes(repository_name):
	# print(f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}metrics statistics files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}number of changes{BackgroundColors.GREEN}.{Style.RESET_ALL}")
	# Read the csv file
	data = pd.read_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{UNSORTED_CHANGED_METHODS_CSV_FILENAME}")
	# Sort the csv file by the number of changes
	data = data.sort_values(by=["Changed"], ascending=False)
	# Write the sorted csv file to a new csv file
	data.to_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SORTED_CHANGED_METHODS_CSV_FILENAME}", index=False)

# @brief: This function sorts the interesting changes csv file according to the percentual variation of the metric
# @param: repository_name: The name of the repository
# @return: None
def sort_csv_by_percentual_variation(repository_name):
	# print(f"{BackgroundColors.GREEN}Sorting the {BackgroundColors.CYAN}interesting changes files{BackgroundColors.GREEN} by the {BackgroundColors.CYAN}percentual variation of the metric{BackgroundColors.GREEN}.{Style.RESET_ALL}")
	# Read the csv file
	data = pd.read_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}")
	# Sort the csv file by the percentual variation of the metric
	data = data.sort_values(by=["Percentual Variation"], ascending=False)
	# Write the sorted csv file to a new csv file
	data.to_csv(f"{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}", index=False)

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

# @brief: The main function
# @param: None
# @return: None
def main():
	# Check if the path constants contains whitespaces
	if path_contains_whitespaces():
		print(f"{BackgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
		return

	print(f"{BackgroundColors.GREEN}This script generates the {BackgroundColors.CYAN}classes or methods metrics evolution history, metrics statistics and linear regression{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{list(DEFAULT_REPOSITORY_NAMES)}{BackgroundColors.GREEN} repositories.{Style.RESET_ALL}")

	process_all_repositories() # Process all the repositories
		
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
   main() # Call the main function
