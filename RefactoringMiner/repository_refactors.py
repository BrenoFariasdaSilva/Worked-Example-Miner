import atexit # For playing a sound when the program finishes
import os # OS module in Python provides functions for interacting with the operating system
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
DEFAULT_REPOSITORIES = {"commons-lang": "https://github.com/apache/commons-lang", "jabref": "https://github.com/JabRef/jabref", "kafka": "https://github.com/apache/kafka", "zookeeper": "https://github.com/apache/zookeeper"} # The default repositories to be analyzed
COMMITS_NUMBER = {"commons-lang": 8000, "jabref": 20000, "kafka": 12000, "zookeeper": 3000} # The number of commits of each repository
ITERATIONS_PER_SECOND = {"commons-lang": 4, "jabref": 4, "kafka": 4, "zookeeper": 4} # The duration of the iterations for each repository

# Relative paths:
RELATIVE_REFACTORING_MINER_PATH = "/RefactoringMiner-2.4.0/bin/RefactoringMiner" # The relative path to the RefactoringMiner Tool
RELATIVE_JSON_FILES_DIRECTORY_PATH = "/json_files" # The relative path of the directory that contains the generated JSON files
RELATIVE_REPOSITORY_REFACTORS_DIRECTORY_PATH = "/repository_refactors" # The relative path of the directory that contains the generated JSON files 
RELATIVE_REPOSITORIES_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories

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

# @brief: This function is used to verify if the RefactoringMiner for the DEFAULT_REFACTORINGS were already generated
# @param: None
# @return: Returns a new dictionary with the DEFAULT_REFACTORINGS that were not generated
def verify_refactorings():
   refactorings = {} # The refactorings dictionary
   # Loop through the default repositories
   for repository_name, repository_url in DEFAULT_REPOSITORIES.items():
      json_repository_filepath = f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORY_REFACTORS_DIRECTORY_PATH}/{repository_name}.{JSON_FILE_FORMAT}" # The path to the json directory
      # Verify if the JSON file already exists
      if not os.path.isfile(json_repository_filepath):
         refactorings[repository_name] = repository_url # Add the repository to the refactorings dictionary
      else:
         print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}Refactorings{backgroundColors.GREEN} for the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository were already generated.{Style.RESET_ALL}")
   return refactorings # Return the refactorings dictionary

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

# @brief: This function is used to process each repositorie name concurrently, using threads
# @param: repositories: The repositories dictionary to be analyzed
# @return: None 
def process_repositories_concurrently(repositories):
   threads = [] # The threads list
   # Loop through the default repositories
   for repository_name, repository_url in repositories.items():
      estimated_time_string = f"{backgroundColors.GREEN}Estimated time for {backgroundColors.CYAN}generating the refactoring{backgroundColors.GREEN} for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
      output_time(estimated_time_string, round((COMMITS_NUMBER[repository_name]/(ITERATIONS_PER_SECOND[repository_name])), 2))
      thread = threading.Thread(target=process_repository, args=(repository_name, repository_url,)) # Create a thread to process the repository
      threads.append(thread) # Append the thread to the threads list
      thread.start() # Start the thread

   # Wait for all threads to finish
   for thread in threads:
      thread.join() # Wait for the thread to finish
      
# @brief: This function is used to process the repository
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @return: None
def process_repository(repository_name, repository_url):
   start_time = time.time() # Get the start time

   # Clone the repository or update it if it already exists
   clone_repository(repository_name, repository_url)

   # Run the RefactoringMiner command to generate the JSON files
   generate_commit_refactors(repository_name)

   end_time = time.time() # Get the end time

   # Output the time needed to generate the JSON files for the repository
   output_string = f"{backgroundColors.GREEN}Time needed to {backgroundColors.CYAN}generate the JSON files {backgroundColors.GREEN}for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
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
      
# This function runs the RefactoringMiner command to generate the JSON files
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def generate_commit_refactors(repository_name):
   repository_directory_path = f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   json_output_filepath = f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORY_REFACTORS_DIRECTORY_PATH}/{repository_name}.{JSON_FILE_FORMAT}" # The path to the json directory

   # Run the Refactoring Miner Command: REFACTORING_MINER_ABSOLUTE_PATH -a REPOSITORY_DIRECTORY_PATH -json JSON_FILES_DIRECTORY_PATH
   thread = subprocess.Popen([ABSOLUTE_REFACTORING_MINER_PATH, "-a", repository_directory_path, "-json", json_output_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = thread.communicate() # Get the output of the thread
   
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
      
   repositories = verify_refactorings() # Verify if the RefactoringMiner for the DEFAULT_REFACTORINGS were already generated
   if not repositories:
      return
   
   print(f"{backgroundColors.GREEN}This script will {backgroundColors.CYAN}generate de refactors{backgroundColors.GREEN} using {backgroundColors.CYAN}RefactoringMiner{backgroundColors.GREEN} for the {backgroundColors.CYAN}{list(repositories.keys())}{backgroundColors.GREEN} repositories.{Style.RESET_ALL}")

   # Create the json directory
   create_directory(f"{ABSOLUTE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORY_REFACTORS_DIRECTORY_PATH}", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORY_REFACTORS_DIRECTORY_PATH}")
   # Create the repositories directory
   create_directory(f"{ABSOLUTE_REPOSITORIES_DIRECTORY_PATH}", f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}")

   # Process the repositories concurrently
   process_repositories_concurrently(repositories)

   print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}refactors{backgroundColors.GREEN} for the {backgroundColors.CYAN}{list(repositories.keys())}{backgroundColors.GREEN} repositories were generated.{Style.RESET_ALL}")
    
# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function