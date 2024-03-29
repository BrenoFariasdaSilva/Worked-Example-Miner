import atexit # For playing a sound when the program finishes
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool
import json # JSON (JavaScript Object Notation) is a lightweight data-interchange format
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import threading # The threading module provides a high-level interface for running tasks in separate threads
import time # This module provides various time-related functions
from colorama import Style # For coloring the terminal
from repositories_refactors import BackgroundColors # Import the BackgroundColors class
from repositories_refactors import START_PATH, JSON_FILE_FORMAT, DEFAULT_REPOSITORIES, RELATIVE_JSON_FILES_DIRECTORY_PATH, RELATIVE_REPOSITORIES_DIRECTORY_PATH, FULL_REFACTORING_MINER_PATH, FULL_JSON_FILES_DIRECTORY_PATH, FULL_REPOSITORIES_DIRECTORY_PATH, VERBOSE # Import the constants
from repositories_refactors import clone_repository, create_directory, output_time, path_contains_whitespaces, play_sound # Import the functions
from tqdm import tqdm # Import tqdm for the progress bar functionality

# Default values that can be changed:
DESIRED_REFACTORINGS_ONLY = True # If True, only the desired refactoring types will be considered
DESIRED_REFACTORING_TYPES = ["Extract Method", "Extract Class", "Pull Up Method", "Push Down Method", "Extract Superclass", "Move Method"] # The desired refactoring types
DEFAULT_REPOSITORY = "zookeeper" # The default repository to be analyzed
FILES_TO_ANALYZE = {"org.apache.zookeeper.server.quorum.Leader": "lead", "org.apache.zookeeper.server.quorum.LeaderElection": "lookForLeader", "org.apache.zookeeper.server.quorum.Follower": "followLeader"} # The desired methods of each repository

# Constants:
CLASSES_TYPE = {"class", "interface", "enum", "innerclass", "anonymous"} # The types of classes.
CLASSES_OR_METHODS = "classes" if any(class_type in FILES_TO_ANALYZE.values() for class_type in CLASSES_TYPE) else "methods" # The default class or method to be analyzed

# Relative paths:
RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH = "/metrics_evolution_refactors" # The relative path of the directory that contains the metrics evolution refactors files
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "../PyDriller/metrics_evolution" # The relative path of the directory that contains the metrics evolution files

# Functions:

def process_repository(repository_name, repository_url):
   """
   Process the repository.

   :param repository_name: Name of the repository to be analyzed
   :param repository_url: URL of the repository to be analyzed
   :return: None
   """

   if VERBOSE: # If the VERBOSE constant is set to True
      print(f"{BackgroundColors.GREEN}Processing the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

   start_time = time.time() # Get the start time

   # Clone the repository or update it if it already exists
   clone_repository(repository_name, repository_url)

   # Create a thread and call the generate_commit_refactors_for_class_or_methods for each FILES_TO_ANALYZE
   generate_refactorings_concurrently(repository_name)

   end_time = time.time() # Get the end time

   # Output the time needed to generate the JSON files for the repository
   output_string = f"{BackgroundColors.GREEN}Time needed to {BackgroundColors.CYAN}generate the JSON files for the commits in {BackgroundColors.CYAN} {list(FILES_TO_ANALYZE.items())} {BackgroundColors.GREEN}for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
   output_time(output_string, end_time - start_time)

def generate_refactorings_concurrently(repository_name):
   """
   Generate the refactoring instances concurrently.

   :param repository_name: Name of the repository to be analyzed
   :return: None
   """

   if VERBOSE: # If the VERBOSE constant is set to True
      print(f"{BackgroundColors.GREEN}Generating the refactoring instances concurrently for the {BackgroundColors.CYAN}{list(FILES_TO_ANALYZE.items())} {CLASSES_OR_METHODS}{BackgroundColors.GREEN} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

   threads = [] # List of threads
   # For each class or method to be analyzed, wrap the iteration with tqdm for a progress bar
   for classname, variable_attribute in tqdm(FILES_TO_ANALYZE.items(), desc="Processing Refactorings", unit="file"):
      thread = threading.Thread(target=generate_commit_refactors_for_class_or_methods, args=(repository_name, classname, variable_attribute,)) # Create a thread
      threads.append(thread) # Append the thread to the list of threads
      thread.start() # Start the thread
   
   for thread in tqdm(threads, desc="Joining Threads", unit="thread"): # For each thread, also show progress for joining
      thread.join() # Wait for the thread to finish

def generate_commit_refactors_for_class_or_methods(repository_name, classname, variable_attribute):
   """
   Generate the refactoring instances for the class or method.

   :param repository_name: Name of the repository to be analyzed
   :param classname: Name of the class to be analyzed
   :param variable_attribute: Name of the variable or attribute to be analyzed
   :return: None
   """

   if VERBOSE: # If the VERBOSE constant is set to True
      print(f"{BackgroundColors.GREEN}Generating the refactoring instances for the {BackgroundColors.CYAN}{classname}{BackgroundColors.GREEN} {CLASSES_OR_METHODS} in the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   # Open the metrics_evolutions desired file
   csv_file_path = f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}.csv"
   # Open the csv file and read the column "Commit Hash"
   csv_file = pd.read_csv(csv_file_path, usecols=["Commit Hash"])
   # Get the list of commits
   commits_hashes = csv_file["Commit Hash"].tolist()

   # Create the output directory for the JSON files
   create_directory(f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}/", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}")
   create_directory(f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}-filtered/", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}-filtered")

   repository_directory_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   for commit_hash in commits_hashes: # For each commit, generate the JSON file
      # Split the commit_hash into two parts, the substring before the first hyphen and the substring after the first hyphen, and store them in two variables: index and commit_hash
      index, commit_hash = commit_hash.split("-", 1)

      json_filepath = f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}/{index}-{commit_hash}.{JSON_FILE_FORMAT}" # The path to the output JSON file
      json_filtered_filepath = f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_METRICS_EVOLUTION_REFACTORS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{classname}/{variable_attribute}-filtered/{index}-{commit_hash}.{JSON_FILE_FORMAT}" # The path to the filtered JSON file

      # Run the Refactoring Miner Command: REFACTORING_MINER_FULL_PATH -c REPOSITORY_DIRECTORY_PATH COMMIT_HASH -json JSON_FILES_DIRECTORY_PATH 
      thread = subprocess.Popen([f"{FULL_REFACTORING_MINER_PATH}", "-c", f"{repository_directory_path}", f"{commit_hash}", "-json", f"{json_filepath}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # Wait for the thread to finish
      thread.wait()

      # Filter the JSON file according to the desired refactoring types if DESIRED_REFACTORINGS_ONLY is set to True
      if DESIRED_REFACTORINGS_ONLY:
         filter_json_file(classname, json_filepath, json_filtered_filepath)

def filter_json_file(classname, json_filepath, json_filtered_filepath):
   """
   Filter the JSON file according to the desired refactoring types.

   :param classname: Name of the class to be analyzed
   :param json_filepath: Path to the JSON file to be filtered
   :param json_filtered_filepath: Path to the filtered JSON file
   :return: None
   """

   if VERBOSE: # If the VERBOSE constant is set to True
      print(f"{BackgroundColors.GREEN}Filtering the JSON file {BackgroundColors.CYAN}{json_filepath}{BackgroundColors.GREEN} according to the desired refactoring types...{Style.RESET_ALL}")
   
   # Read the JSON data from the file
   with open(json_filepath, "r") as json_file:
      json_data = json.load(json_file)

   filtered_json_data = [] # Initialize the filtered JSON data

   # Filter out refactoring instances that are not in the desired types
   for commit in json_data["commits"]: # For each commit
      for refactoring in commit["refactorings"]: # For each refactoring instance
         if refactoring["type"] in DESIRED_REFACTORING_TYPES: # If the refactoring type is in the desired refactoring types
            for rightSideLocation, leftSideLocation in zip(refactoring["rightSideLocations"], refactoring["leftSideLocations"]): # For each rightSideLocation and leftSideLocation
               file_classname = classname.replace(".", "/") # Replace the dots with slashes
               file_classname = f"{file_classname}.java" # Append the Java file extension
               if file_classname in rightSideLocation["filePath"] or file_classname in leftSideLocation["filePath"]: # If the file_classname is in the rightSideLocation or leftSideLocation
                  filtered_json_data.append(refactoring) # Append the refactoring instance to the filtered JSON data

   # Write the filtered JSON data to the file if it is not empty
   if filtered_json_data:
      # Open the JSON file for writing
      with open(json_filtered_filepath, "w") as json_file:
         json.dump(filtered_json_data, json_file, indent=1) # Write the filtered JSON data to the file

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

def main():
   """
   Main function.

   :return: None
   """

   # Verify if the path contains whitespaces
   if path_contains_whitespaces():
      print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{START_PATH}{BackgroundColors.RED} constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
      
   # Print the welcome message
   print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Metrics Evolution Refactors{BackgroundColors.GREEN}! This script is part of the {BackgroundColors.CYAN}Worked Example Miner (WEM){BackgroundColors.GREEN} project.{Style.RESET_ALL}")
   print(f"{BackgroundColors.GREEN}This Script will generate the refactors for the commits in {BackgroundColors.CYAN}{list(FILES_TO_ANALYZE.items())} {CLASSES_OR_METHODS}{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{DEFAULT_REPOSITORY}{BackgroundColors.GREEN} repository that were selected by analyzing the generated data from {BackgroundColors.CYAN}PyDriller/metrics_changes.py{BackgroundColors.GREEN} code.{Style.RESET_ALL}", end="\n\n")

   # Create the json directory
   create_directory(f"{FULL_JSON_FILES_DIRECTORY_PATH}", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}")
   # Create the repositories directory
   create_directory(f"{FULL_REPOSITORIES_DIRECTORY_PATH}", f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}")

   # Process the repository
   process_repository(DEFAULT_REPOSITORY, DEFAULT_REPOSITORIES[DEFAULT_REPOSITORY])

   # Output the message that the script has finished
   print(f"\n{BackgroundColors.GREEN}The {BackgroundColors.CYAN}Metrics Evolution Refactors{BackgroundColors.GREEN} script has finished!{Style.RESET_ALL}")

if __name__ == '__main__':
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
