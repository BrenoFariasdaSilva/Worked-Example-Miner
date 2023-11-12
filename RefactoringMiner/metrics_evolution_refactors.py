import atexit # For playing a sound when the program finishes
import os # OS module in Python provides functions for interacting with the operating system
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool
import json # JSON (JavaScript Object Notation) is a lightweight data-interchange format
import platform # For getting the operating system name
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import threading # The threading module provides a high-level interface for running tasks in separate threads
import time # This module provides various time-related functions
from colorama import Style # For coloring the terminal

# Macros:
class BackgroundColors: # Colors for the terminal
   CYAN = "\033[96m" # Cyan
   GREEN = "\033[92m" # Green
   YELLOW = "\033[93m" # Yellow
   RED = "\033[91m" # Red
   BOLD = "\033[1m" # Bold
   UNDERLINE = "\033[4m" # Underline
   CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal
    
# Default paths:
START_PATH = os.getcwd() # Get the current working directory
        
# Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} 
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file
DESIRED_REFACTORING_TYPES = ["Extract Method", "Extract Class", "Pull Up Method", "Push Down Method", "Extract Superclass", "Move Method"] # The desired refactoring types

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# File Formats:
JSON_FILE_FORMAT = "json" # The extension of the generated file by the RefactoringMiner Tool.

# Default values:
DEFAULT_REPOSITORY = "zookeeper" # The default repository to be analyzed
DEFAULT_REPOSITORIES = {"commons-lang": "https://github.com/apache/commons-lang", "jabref": "https://github.com/JabRef/jabref", "kafka": "https://github.com/apache/kafka", "zookeeper": "https://github.com/apache/zookeeper"} # The default repositories to be analyzed
CLASSES_TYPE = {"class", "interface", "enum", "innerclass", "anonymous"} # The types of classes.
FILES_TO_ANALYZE = {"org.apache.zookeeper.server.quorum.Leader": "lead", "org.apache.zookeeper.server.quorum.LeaderElection": "lookForLeader", "org.apache.zookeeper.server.quorum.Follower": "followLeader"} # The desired methods of each repository
# FILES_TO_ANALYZE = {"org.apache.zookeeper.server.quorum.Learner": "class"} # The desired classes of each repository
CLASSES_OR_METHODS = "classes" if any(class_type in FILES_TO_ANALYZE.values() for class_type in CLASSES_TYPE) else "methods" # The default class or method to be analyzed

# Relative paths:
RELATIVE_REFACTORING_MINER_PATH = "/RefactoringMiner-2.4.0/bin/RefactoringMiner" # The relative path to the RefactoringMiner Tool
RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH = "/metrics_evolution_refactors" # The relative path of the directory that contains the metrics evolution refactors files
RELATIVE_JSON_FILES_DIRECTORY_PATH = "/json_files" # The relative path of the directory that contains the generated JSON files
RELATIVE_REPOSITORIES_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "../PyDriller/metrics_evolution" # The relative path of the directory that contains the metrics evolution files

# Absolute paths:
ABSOLUTE_REFACTORING_MINER_PATH = START_PATH + RELATIVE_REFACTORING_MINER_PATH # The absolute path to the RefactoringMiner Tool
ABSOLUTE_JSON_FILES_DIRECTORY_PATH = START_PATH + RELATIVE_JSON_FILES_DIRECTORY_PATH # The absolute path of the directory that contains the generated JSON files
ABSOLUTE_REPOSITORIES_DIRECTORY_PATH = START_PATH + RELATIVE_REPOSITORIES_DIRECTORY_PATH # The absolute path of the directory that contains the repositories

# @brief: This function is used to verify if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Verify if the PATH constant contains whitespaces
   if " " in START_PATH: # If the PATH constant contains whitespaces
      return True # Return True if the PATH constant contains whitespaces
   return False # Return False if the PATH constant does not contain whitespaces

# @brief: Create a directory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      return
   try: # Try to create the directory
      os.makedirs(full_directory_name)
   except OSError: # If the directory cannot be created
      print(f"{BackgroundColors.GREEN}The creation of the {BackgroundColors.CYAN}{relative_directory_name}{BackgroundColors.GREEN} directory failed{Style.RESET_ALL}")
      
# @brief: This function is used to process the repository
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @return: None
def process_repository(repository_name, repository_url):
   start_time = time.time() # Get the start time

   # Clone the repository or update it if it already exists
   clone_repository(repository_name, repository_url)

   # Create a thread and call the generate_commit_refactors_for_class_or_methods for each FILES_TO_ANALYZE
   generate_refactorings_concurrently(repository_name)

   end_time = time.time() # Get the end time

   # Output the time needed to generate the JSON files for the repository
   output_string = f"{BackgroundColors.GREEN}Time needed to {BackgroundColors.CYAN}generate the JSON files for the commits in {BackgroundColors.CYAN} {list(FILES_TO_ANALYZE.items())} {BackgroundColors.GREEN}for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
   output_time(output_string, end_time - start_time)

# @brief: Clone the repository to the repository directory
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @return: None
def clone_repository(repository_name, repository_url):
   repository_directory_path = f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   # Verify if the repository directory already exists and if it is not empty
   if os.path.isdir(repository_directory_path) and os.listdir(repository_directory_path):
      update_repository(repository_name) # Update the repository
      return
   else:
      # Create a thread to clone the repository
      thread = subprocess.Popen(["git", "clone", repository_url, repository_directory_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # Wait for the thread to finish
      thread.wait()

# @brief: Update the repository using "git pull"
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def update_repository(repository_name):
   repository_directory_path = f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   os.chdir(repository_directory_path) # Change the current working directory to the repository directory
   
   # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + '/' + repository_name
   update_thread = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   update_thread.wait() # Wait for the thread to finish
   os.chdir(START_PATH) # Change the current working directory to the default one

# @brief: This function is used to create a thread and call the generate_commit_refactors_for_class_or_methods for each FILES_TO_ANALYZE
# @param: repository_name
# @return: None
def generate_refactorings_concurrently(repository_name):
   threads = [] # List of threads
   for classname, variable_attribute in FILES_TO_ANALYZE.items(): # For each class or method to be analyzed
      thread = threading.Thread(target=generate_commit_refactors_for_class_or_methods, args=(repository_name,classname,variable_attribute,)) # Create a thread
      threads.append(thread) # Append the thread to the list of threads
      thread.start() # Start the thread
   for thread in threads: # For each thread
      thread.join() # Wait for the thread to finish

# This function runs the RefactoringMiner command to generate the JSON files
# @param: repository_name: Name of the repository to be analyzed
# @param: classname: Name of the class to be analyzed
# @param: variable_attribute: Name of the variable or attribute to be analyzed
# @return: None
def generate_commit_refactors_for_class_or_methods(repository_name, classname, variable_attribute):
   # Open the metrics_evolutions desired file
   csv_file_path = f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}.csv"
   # Open the csv file and read the column "Commit Hash"
   csv_file = pd.read_csv(csv_file_path, usecols=["Commit Hash"])
   # Get the list of commits
   commits_hashes = csv_file["Commit Hash"].tolist()

   # Create the output directory for the JSON files
   create_directory(f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}/", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}")
   create_directory(f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}-filtered/", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}-filtered")

   repository_directory_path = f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   for commit_hash in commits_hashes: # For each commit, generate the JSON file
      # Split the commit_hash into two parts, the substring before the first hyphen and the substring after the first hyphen, and store them in two variables: index and commit_hash
      index, commit_hash = commit_hash.split("-", 1)

      json_filepath = f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}/{index}-{commit_hash}.{JSON_FILE_FORMAT}" # The path to the output JSON file
      json_filtered_filepath = f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}-filtered/{index}-{commit_hash}.{JSON_FILE_FORMAT}" # The path to the filtered JSON file

      # Run the Refactoring Miner Command: REFACTORING_MINER_ABSOLUTE_PATH -c REPOSITORY_DIRECTORY_PATH COMMIT_HASH -json JSON_FILES_DIRECTORY_PATH 
      thread = subprocess.Popen([f"{ABSOLUTE_REFACTORING_MINER_PATH}", "-c", f"{repository_directory_path}", f"{commit_hash}", "-json", f"{json_filepath}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # Wait for the thread to finish
      thread.wait()

      # Filter the JSON file
      filter_json_file(classname, json_filepath, json_filtered_filepath)

# @brief: This function is used to filter the JSON file
# @param: classname: Name of the class to be analyzed
# @param: json_filepath: Path to the JSON file to be filtered
# @param: json_filtered_filepath: Path to the JSON file to be filtered
# @return: None
def filter_json_file(classname, json_filepath, json_filtered_filepath):
   # Read the JSON data from the file
   with open(json_filepath, 'r') as json_file:
      json_data = json.load(json_file)

   filtered_json_data = [] # Initialize the filtered JSON data

   # Filter out refactoring instances that are not in the desired types
   for commit in json_data['commits']:
      for refactoring in commit["refactorings"]:
         if refactoring["type"] in DESIRED_REFACTORING_TYPES:
            for rightSideLocation, leftSideLocation in zip(refactoring["rightSideLocations"], refactoring["leftSideLocations"]):
               file_classname = classname.replace(".", "/")
               file_classname = f"{file_classname}.java"
               if file_classname in rightSideLocation["filePath"] or file_classname in leftSideLocation["filePath"]:
                  filtered_json_data.append(refactoring)

   # Write the filtered JSON data to the file if it is not empty
   if filtered_json_data:
      with open(json_filtered_filepath, 'w') as json_file:
         json.dump(filtered_json_data, json_file, indent=1) # Write the filtered JSON data to the file
   
# @brief: This function outputs time, considering the appropriate time unit
# @param: output_string: String to be outputted
# @param: time: Time to be outputted
# @return: None
def output_time(output_string, time):
   if float(time) < int(TIME_UNITS[0]):
      time_unit = "seconds"
      time_value = time
   elif float(time) < float(TIME_UNITS[1]):
      time_unit = "minutes"
      time_value = time / TIME_UNITS[0]
   elif float(time) < float(TIME_UNITS[2]):
      time_unit = "hours"
      time_value = time / TIME_UNITS[1]
   else:
      time_unit = "days"
      time_value = time / TIME_UNITS[2]

   rounded_time = round(time_value, 2)
   print(f"{output_string}{BackgroundColors.CYAN}{rounded_time} {time_unit}{Style.RESET_ALL}")

This function defines the command to play a sound when the program finishes
def play_sound():
	if os.path.exists(SOUND_FILE):
		if platform.system() in SOUND_COMMANDS: # if the platform.system() is in the SOUND_COMMANDS dictionary
			os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
		else: # if the platform.system() is not in the SOUND_COMMANDS dictionary
			print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
	else: # if the sound file does not exist
		print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

# @brief: This function is used to run the main function
def main():
   # Verify if the path contains whitespaces
   if path_contains_whitespaces():
      print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{START_PATH}{BackgroundColors.RED} constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
      
   print(f"{BackgroundColors.GREEN}This Script will generate de refactors for the commits in {BackgroundColors.CYAN}{list(FILES_TO_ANALYZE.items())} {CLASSES_OR_METHODS}{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{DEFAULT_REPOSITORY}{BackgroundColors.GREEN} repository.{Style.RESET_ALL}")

   # Create the json directory
   create_directory(f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}")
   # Create the repositories directory
   create_directory(f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}", f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}")

   # Process the repository
   process_repository(DEFAULT_REPOSITORY, DEFAULT_REPOSITORIES[DEFAULT_REPOSITORY])
    
# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function
