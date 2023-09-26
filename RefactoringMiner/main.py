import atexit # For playing a sound when the program finishes
import os # OS module in Python provides functions for interacting with the operating system
import platform # For getting the operating system name
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import threading # The threading module provides a high-level interface for running tasks in separate threads
import time # This module provides various time-related functions
from colorama import Style # For coloring the terminal
from tqdm import tqdm # For Generating the Progress Bars

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
ITERATIONS_PER_SECOND = {"commons-lang": 3, "jabref": 3, "kafka": 3, "zookeeper": 3} # The duration of the iterations for each repository

# Relative paths:
RELATIVE_REFACTORING_MINER_PATH = "/RefactoringMiner-2.4.0/bin/RefactoringMiner" # The relative path to the RefactoringMiner Tool
RELATIVE_JSON_FILES_DIRECTORY_PATH = "/json_files" # The relative path of the directory that contains the generated JSON files
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

# @brief: This function is used to process each repositorie name concurrently, using threads
# @param: None
# @return: None 
def process_repositories_concurrently():
   threads = [] # The threads list
   # Loop through the default repositories
   with tqdm(total=len(DEFAULT_REPOSITORIES), desc=f"{backgroundColors.GREEN}Running {backgroundColors.CYAN}RefactoringMiner{backgroundColors.GREEN} for {backgroundColors.CYAN}{list(DEFAULT_REPOSITORIES.keys())}{Style.RESET_ALL}", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
      for repository_name, repository_url in DEFAULT_REPOSITORIES.items():
         estimated_time_string = f"{backgroundColors.GREEN}Estimated time for running all of the iterations for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
         output_time(estimated_time_string, round(((ITERATIONS_PER_SECOND[repository_name] * COMMITS_NUMBER[repository_name])/60), 2))
         thread = threading.Thread(target=process_repository, args=(repository_name, repository_url,)) # Create a thread to process the repository
         threads.append(thread) # Append the thread to the threads list
         thread.start() # Start the thread

   # Wait for all threads to finish
   for thread in threads:
      thread.join() # Wait for the thread to finish
      # Update the progress bar ever time a thread finishes
      pbar.update(1)

def main():
	# Verify if the path contains whitespaces
	if path_contains_whitespaces():
		print(f"{backgroundColors.RED}The {backgroundColors.CYAN}{START_PATH}{backgroundColors.RED} constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
		return
     
   # Process the repositories concurrently
	process_repositories_concurrently()

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function