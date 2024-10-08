import atexit # For playing a sound when the program finishes
import os # OS module in Python provides functions for interacting with the operating system
import platform # For getting the operating system name
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import time # This module provides various time-related functions
from colorama import Style # For coloring the terminal
from concurrent.futures import ThreadPoolExecutor # For managing threads
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # For creating progress bars

# Macros:
class BackgroundColors: # Colors for the terminal
   CYAN = "\033[96m" # Cyan
   GREEN = "\033[92m" # Green
   YELLOW = "\033[93m" # Yellow
   RED = "\033[91m" # Red
   BOLD = "\033[1m" # Bold
   UNDERLINE = "\033[4m" # Underline
   CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal
    
# Default values that can be changed:
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function.
DEFAULT_REPOSITORIES = {"zookeeper": "https://github.com/apache/zookeeper"} # The default repositories to be analyzed
   
# Default paths:
START_PATH = os.getcwd() # Get the current working directory

# Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} 
SOUND_FILE = "../.assets/Sounds/NotificationSound.wav" # The path to the sound file

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# File Formats:
JSON_FILE_FORMAT = "json" # The extension of the generated file by the RefactoringMiner Tool.

# Relative paths:
RELATIVE_REFACTORING_MINER_PATH = "/RefactoringMiner-2.4.0/bin/RefactoringMiner" # The relative path to the RefactoringMiner Tool
RELATIVE_JSON_FILES_DIRECTORY_PATH = "/json_files" # The relative path of the directory that contains the generated JSON files
RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH = "/repositories_refactorings" # The relative path of the directory that contains the generated JSON files 
RELATIVE_REPOSITORIES_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories

# Full paths (Start Path + Relative Paths):
FULL_REFACTORING_MINER_PATH = START_PATH + RELATIVE_REFACTORING_MINER_PATH # The Full path to the RefactoringMiner Tool
FULL_JSON_FILES_DIRECTORY_PATH = START_PATH + RELATIVE_JSON_FILES_DIRECTORY_PATH # The Full path of the directory that contains the generated JSON files
FULL_REPOSITORIES_DIRECTORY_PATH = START_PATH + RELATIVE_REPOSITORIES_DIRECTORY_PATH # The Full path of the directory that contains the repositories

def verbose_output(true_string="", false_string=""):
   """
   Outputs a message if the VERBOSE constant is set to True.

   :param true_string: The string to be outputted if the VERBOSE constant is set to True.
   :param false_string: The string to be outputted if the VERBOSE constant is set to False.
   :return: None
   """

   if VERBOSE and true_string != "": # If the VERBOSE constant is set to True and the true_string is set
      print(true_string) # Output the true statement string
   elif false_string != "":
      print(false_string) # Output the false statement string

def path_contains_whitespaces():
   """
   Verify if the PATH constant contains whitespaces.

   :return: True if the PATH constant contains whitespaces, False otherwise
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the {BackgroundColors.CYAN}PATH{BackgroundColors.GREEN} constant contains whitespaces...{Style.RESET_ALL}")

   # Verify if the PATH constant contains whitespaces
   if " " in START_PATH: # If the PATH constant contains whitespaces
      return True # Return True if the PATH constant contains whitespaces
   return False # Return False if the PATH constant does not contain whitespaces

def verify_refactorings():
   """
   Verify if the RefactoringMiner Refactorings were already processed for the DEFAULT_REPOSITORIES and return the repositories that weren't processed yet.

   :return: Returns a new dictionary with the repositories that weren't processed yet
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the {BackgroundColors.CYAN}Refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}DEFAULT_REFACTORINGS{BackgroundColors.GREEN} were already generated...{Style.RESET_ALL}")
   
   repositories = {} # The repositories dictionary
   # Loop through the default repositories
   for repository_name, repository_url in DEFAULT_REPOSITORIES.items():
      json_repository_filepath = f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH}/{repository_name}.{JSON_FILE_FORMAT}" # The path to the json directory
      # Verify if the JSON file already exists
      if not os.path.isfile(json_repository_filepath):
         repositories[repository_name] = repository_url # Add the repository to the repositories dictionary
      else:
         print(f"{BackgroundColors.GREEN}The {BackgroundColors.CYAN}Refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository were already generated.{Style.RESET_ALL}")
   return repositories # Return the repositories dictionary

def create_directory(full_directory_name, relative_directory_name):
   """
   Create a directory.

   :param full_directory_name: Name of the directory to be created
   :param relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Creating the {BackgroundColors.CYAN}{relative_directory_name}{BackgroundColors.GREEN} directory...{Style.RESET_ALL}")
   
   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      return # Return if the directory already exists
   try: # Try to create the directory
      os.makedirs(full_directory_name)
   except OSError: # If the directory cannot be created
      print(f"{BackgroundColors.GREEN}The creation of the {BackgroundColors.CYAN}{relative_directory_name}{BackgroundColors.GREEN} directory failed{Style.RESET_ALL}")

def output_time(output_string, time):
   """
   Outputs time, considering the appropriate time unit.

   :param output_string: String to be outputted.
   :param time: Time to be outputted.
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Outputting the time in the most appropriate time unit...{Style.RESET_ALL}")

   if float(time) < int(TIME_UNITS[0]): # If the time is less than 60 seconds
      time_unit = "seconds" # Set the time unit to seconds
      time_value = time # Set the time value to time
   elif float(time) < float(TIME_UNITS[1]): # If the time is less than 3600 seconds
      time_unit = "minutes" # Set the time unit to minutes
      time_value = time / TIME_UNITS[0] # Set the time value to time divided by 60
   elif float(time) < float(TIME_UNITS[2]): # If the time is less than 86400 seconds
      time_unit = "hours" # Set the time unit to hours
      time_value = time / TIME_UNITS[1] # Set the time value to time divided by 3600
   else: # If the time is greater than or equal to 86400 seconds
      time_unit = "days" # Set the time unit to days
      time_value = time / TIME_UNITS[2] # Set the time value to time divided by 86400

   rounded_time = round(time_value, 2) # Round the time value to two decimal places
   print(f"{BackgroundColors.GREEN}{output_string}{BackgroundColors.CYAN}{rounded_time} {time_unit}{BackgroundColors.GREEN}.{Style.RESET_ALL}")

def update_repository(repository_directory_path):
   """
   Update the repository using "git pull".

   :param repository_directory_path: The path to the repository directory
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Updating the {BackgroundColors.CYAN}{repository_directory_path.split('/')[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   os.chdir(repository_directory_path) # Change the current working directory to the repository directory
   
   # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + '/' + repository_name
   update_thread = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   update_thread.wait() # Wait for the thread to finish
   os.chdir(START_PATH) # Change the current working directory to the default one

def clone_repository(repository_directory_path, repository_url):
   """
   Clone the repository to the repository directory.

   :param repository_directory_path: The path to the repository directory
   :param repository_url: URL of the repository to be analyzed
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Cloning the {BackgroundColors.CYAN}{repository_directory_path.split('/')[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   # Create a thread to clone the repository
   thread = subprocess.Popen(["git", "clone", repository_url, repository_directory_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   # Wait for the thread to finish
   thread.wait()

def setup_repository(repository_name, repository_url):
   """"
   Setup the repository by cloning it or updating it if it already exists.

   :param repository_name: Name of the repository to be analyzed
   :param repository_url: URL of the repository to be analyzed
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Setting up the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   repository_directory_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   
   # Verify if the repository directory already exists and if it is not empty
   if os.path.isdir(repository_directory_path) and os.listdir(repository_directory_path):
      update_repository(repository_directory_path) # Update the repository
   else:
      clone_repository(repository_directory_path, repository_url) # Clone the repository

def generate_commit_refactorings(repository_name):
   """
   Generate the refactoring instances for the repository.

   :param repository_name: Name of the repository to be analyzed
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Generating the {BackgroundColors.CYAN}refactoring instances{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   repository_directory_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   json_output_filepath = f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH}/{repository_name}.{JSON_FILE_FORMAT}" # The path to the json directory

   # Run the Refactoring Miner Command: REFACTORING_MINER_FULL_PATH -a REPOSITORY_DIRECTORY_PATH -json JSON_FILES_DIRECTORY_PATH
   thread = subprocess.Popen([FULL_REFACTORING_MINER_PATH, "-a", repository_directory_path, "-json", json_output_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = thread.communicate() # Get the output of the thread

def process_repository(repository_name, repository_url):
   """
   Process the repository.

   :param repository_name: Name of the repository to be analyzed
   :param repository_url: URL of the repository to be analyzed
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   start_time = time.time() # Get the start time

   # Setup the repository
   setup_repository(repository_name, repository_url)

   # Run the RefactoringMiner command to generate the JSON files
   generate_commit_refactorings(repository_name)

   end_time = time.time() # Get the end time

   # Output the time needed to generate the JSON files for the repository
   output_string = f"{BackgroundColors.GREEN}Time needed to {BackgroundColors.CYAN}generate the JSON files {BackgroundColors.GREEN}for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
   output_time(output_string, end_time - start_time)

def process_repositories_concurrently(repositories):
   """
   Process the repositories concurrently.

   :param repositories: The repositories dictionary to be analyzed
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Processing the repositories {BackgroundColors.CYAN}{list(repositories.keys())}{BackgroundColors.GREEN} concurrently...{Style.RESET_ALL}")

   # Using ThreadPoolExecutor to manage threads and a tqdm progress bar
   with ThreadPoolExecutor(max_workers=len(repositories)) as executor, tqdm(total=len(repositories), desc="Processing Repositories") as progress:
      futures = [] # The list of futures (threads)

      # Loop through the repositories
      for repository_name, repository_url in repositories.items():
         estimated_time_string = f"{BackgroundColors.GREEN}Estimated time for {BackgroundColors.CYAN}generating the refactoring{BackgroundColors.GREEN} for {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN}: "
         commits_number = sum(1 for _ in Repository(repository_url).traverse_commits()) # Get the number of commits
         output_time(estimated_time_string, commits_number / 2) # Output the estimated time for running all of the iterations for the repository

         # Schedule the execution of the process_repository function
         future = executor.submit(process_repository, repository_name, repository_url)
         future.add_done_callback(lambda p: progress.update(1)) # Update progress bar upon task completion
         futures.append(future) # Add the future to the list

      # Ensures all of the futures are completed
      for future in futures:
         future.result() # Wait for the thread (task) to finish

def play_sound():
   """
   Plays a sound when the program finishes.

   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Playing a {BackgroundColors.CYAN}sound{BackgroundColors.GREEN} when the program finishes...{Style.RESET_ALL}")

   if os.path.exists(SOUND_FILE):
      if platform.system() in SOUND_COMMANDS: # if the platform.system() is in the SOUND_COMMANDS dictionary
         os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
      else: # if the platform.system() is not in the SOUND_COMMANDS dictionary
         print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
   else: # if the sound file does not exist
      print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

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
      return # Exit the program
      
   unprocessed_repositories = verify_refactorings() # Verify if the RefactoringMiner for the DEFAULT_REFACTORINGS were already generated

   # Verify if the unprocessed repositories dictionary is empty
   if not unprocessed_repositories:
      return # Return if the repositories dictionary is empty
   
   # Print the welcome message
   print(f"{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}RefactoringMiner{BackgroundColors.GREEN} script! This script is part of the {BackgroundColors.CYAN}Worked Example Miner (WEM){BackgroundColors.GREEN} project.{Style.RESET_ALL}")
   print(f"{BackgroundColors.GREEN}This script will {BackgroundColors.CYAN}generate the refactoring file{BackgroundColors.GREEN} using {BackgroundColors.CYAN}RefactoringMiner{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{list(unprocessed_repositories.keys())}{BackgroundColors.GREEN} repositories.{Style.RESET_ALL}", end="\n\n")

   # Create the json directory
   create_directory(f"{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH}", f"{RELATIVE_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH}")
   # Create the repositories directory
   create_directory(f"{FULL_REPOSITORIES_DIRECTORY_PATH}", f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}")

   # Process the repositories concurrently
   process_repositories_concurrently(unprocessed_repositories)

   # Output the message that the refactorings for the repositories were generated
   print(f"\n{BackgroundColors.GREEN}The {BackgroundColors.CYAN}refactorings{BackgroundColors.GREEN} for the {BackgroundColors.CYAN}{list(unprocessed_repositories.keys())}{BackgroundColors.GREEN} repositories were generated.{Style.RESET_ALL}")
    		
if __name__ == '__main__':
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """
   
   main() # Call the main function
