import atexit # For playing a sound when the program finishes
import os # OS module in Python provides functions for interacting with the operating system
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool
import platform # For getting the operating system name
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import threading # The threading module provides a high-level interface for running tasks in separate threads
import time # This module provides various time-related functions
from colorama import Style # For coloring the terminal

# Macros:
class backgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red
    
# Default paths:
START_PATH = os.getcwd() # Get the current working directory
        
# Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The sound commands for each operating system
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# File Formats:
JSON_FILE_FORMAT = "json" # The extension of the generated file by the RefactoringMiner Tool.

# Default values:
DEFAULT_REPOSITORY = "zookeeper" # The default repository to be analyzed
CLASSES_OR_METHODS = "methods" # The default class or method to be analyzed
DEFAULT_REPOSITORIES = {"commons-lang": "https://github.com/apache/commons-lang", "jabref": "https://github.com/JabRef/jabref", "kafka": "https://github.com/apache/kafka", "zookeeper": "https://github.com/apache/zookeeper"} # The default repositories to be analyzed
FILES_TO_ANALYZE = {"org.apache.zookeeper.server.quorum.Leader": "lead", "org.apache.zookeeper.server.quorum.LeaderElection": "lookForLeader", "org.apache.zookeeper.server.quorum.Follower": "followLeader"} # The desired classes or methods of each repository

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
      print(f"{backgroundColors.GREEN}The creation of the {backgroundColors.CYAN}{relative_directory_name}{backgroundColors.GREEN} directory failed{Style.RESET_ALL}")
      
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
   output_string = f"{backgroundColors.GREEN}Time needed to {backgroundColors.CYAN}generate the JSON files for the commits in {backgroundColors.CYAN} {list(FILES_TO_ANALYZE.items())} {backgroundColors.GREEN}for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
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

   repository_directory_path = f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   for commit_hash in commits_hashes: # For each commit, generate the JSON file
      # Split the commit_hash into two parts, the substring before the first hyphen and the substring after the first hyphen, and store them in two variables: index and commit_hash
      index, commit_hash = commit_hash.split("-", 1)

      json_filepath = f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}/{index}-{commit_hash}.{JSON_FILE_FORMAT}" # The path to the output JSON file

      # Run the Refactoring Miner Command: REFACTORING_MINER_ABSOLUTE_PATH -c COMMIT_HASH REPOSITORY_DIRECTORY_PATH -json JSON_FILES_DIRECTORY_PATH 
      thread = subprocess.Popen([f"{ABSOLUTE_REFACTORING_MINER_PATH}", "-c", f"{commit_hash}", f"{repository_directory_path}", "-json", f"{json_filepath}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # print the output of the thread
      print(thread.stdout.read().decode("utf-8"))
      # Wait for the thread to finish
      thread.wait()

   
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
   print(f"{output_string}{backgroundColors.CYAN}{rounded_time} {time_unit}{Style.RESET_ALL}")

# @brief: This function defines the command to play a sound when the program finishes
# @param: None
# @return: None
def play_sound():
	if os.path.exists(SOUND_FILE):
		if platform.system() in SOUND_COMMANDS: # if the platform.system() is in the SOUND_COMMANDS dictionary
			os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
		else: # if the platform.system() is not in the SOUND_COMMANDS dictionary
			print(f"{backgroundColors.RED}The {backgroundColors.CYAN}platform.system(){backgroundColors.RED} is not in the {backgroundColors.CYAN}SOUND_COMMANDS dictionary{backgroundColors.RED}. Please add it!{Style.RESET_ALL}")
	else: # if the sound file does not exist
		print(f"{backgroundColors.RED}Sound file {backgroundColors.CYAN}{SOUND_FILE}{backgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

# @brief: This function is used to run the main function
def main():
   # Verify if the path contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.RED}The {backgroundColors.CYAN}{START_PATH}{backgroundColors.RED} constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
      
   print(f"{backgroundColors.GREEN}This Script will generate de refactors for the commits in {backgroundColors.CYAN}{list(FILES_TO_ANALYZE.items())} {CLASSES_OR_METHODS}{backgroundColors.GREEN} for the {backgroundColors.CYAN}{DEFAULT_REPOSITORY}{backgroundColors.GREEN} repository.{Style.RESET_ALL}")

   # Create the json directory
   create_directory(f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}")
   # Create the repositories directory
   create_directory(f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}", f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}")

   # Process the repository
   process_repository(DEFAULT_REPOSITORY, DEFAULT_REPOSITORIES[DEFAULT_REPOSITORY])
    
# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function
