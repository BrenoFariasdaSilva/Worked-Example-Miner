import atexit # For playing a sound when the program finishes
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import os # OS module in Python provides functions for interacting with the operating system
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
import platform # For getting the operating system name
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import threading # The threading module provides a high-level interface for running tasks in separate threads
import time # This module provides various time-related functions
from colorama import Style # For coloring the terminal
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # for progress bar

# Macros:
class backgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red
        
# Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The sound commands for each operating system
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file
        
# Default paths:
PATH = os.getcwd() # Get the current working directory
DEFAULT_FOLDER = PATH # Get the current working directory

# Extensions:
COMMIT_HASHES_FILE_EXTENSION = ".csv" # The extension of the file that contains the commit hashes
DIFF_FILE_EXTENSION = ".diff" # The diff file extension

# CK Generated Files:
CK_METRICS_FILES = ["class.csv", "method.csv"] # The files that are generated by CK

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day
 
# Relative paths:
RELATIVE_CK_METRICS_DIRECTORY_PATH = "/ck_metrics" # The relative path of the directory that contains the CK generated files
DEFAULT_DIFFS_DIRECTORY = "/diffs" # The relative path of the directory that contains the diffs
RELATIVE_REPOSITORIES_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar" # The relative path of the CK JAR file

# Default values:
DEFAULT_REPOSITORIES = {"commons-lang": "https://github.com/apache/commons-lang", "jabref": "https://github.com/JabRef/jabref", "kafka": "https://github.com/apache/kafka", "zookeeper": "https://github.com/apache/zookeeper"} # The default repositories to be analyzed
COMMITS_NUMBER = {"commons-lang": 8000, "jabref": 20000, "kafka": 12000, "zookeeper": 3000} # The number of commits of each repository
ITERATIONS_DURATION = {"commons-lang": 4, "jabref": 20, "kafka": 18, "zookeeper": 12} # The duration of the iterations for each repository
FULL_CK_METRICS_DIRECTORY_PATH = PATH + RELATIVE_CK_METRICS_DIRECTORY_PATH # The full path of the directory that contains the CK generated files
FULL_REPOSITORIES_DIRECTORY_PATH = PATH + RELATIVE_REPOSITORIES_DIRECTORY_PATH # The full path of the directory that contains the repositories
FULL_CK_JAR_PATH = PATH + RELATIVE_CK_JAR_PATH # The full path of the CK JAR file

# @brief: This function is used to verify if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Verify if the PATH constant contains whitespaces
   if " " in PATH: # If the PATH constant contains whitespaces
      return True # Return True if the PATH constant contains whitespaces
   return False # Return False if the PATH constant does not contain whitespaces

# @brief: This function is used to process the repositories concurrently, using threads
# @param: None
# @return: None 
def process_repositories_concurrently():
   threads = [] # The threads list
   # Loop through the default repositories
   for repository_name, repository_url in DEFAULT_REPOSITORIES.items():
      estimated_time_string = f"Estimated time for running all of the iterations for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
      output_time(estimated_time_string, round((ITERATIONS_DURATION[repository_name] * COMMITS_NUMBER[repository_name]), 2))
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
   # Verify if the metrics were already calculated
   if verify_ck_metrics_folder(repository_name):
      print(f"{backgroundColors.GREEN}The metrics for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} were already calculated{Style.RESET_ALL}")
      return

   # Create the ck metrics directory
   create_directory(FULL_CK_METRICS_DIRECTORY_PATH, RELATIVE_CK_METRICS_DIRECTORY_PATH)
   # Create the repositories directory
   create_directory(FULL_REPOSITORIES_DIRECTORY_PATH, RELATIVE_REPOSITORIES_DIRECTORY_PATH)

   # Clone the repository
   clone_repository(repository_name, repository_url)

   # Get the number of commits, which is needed to traverse the repository
   number_of_commits = len(list(Repository(repository_url).traverse_commits()))
   # Traverse the repository to run ck for every commit hash in the repository
   commit_hashes = traverse_repository(repository_name, repository_url, number_of_commits)

   # Write the commit hashes to a csv file
   write_commit_hashes_to_csv(repository_name, commit_hashes)

   # Checkout the main branch
   checkout_branch("main")

# @brief: Update the repository using "git pull"
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def update_repository(repository_name):
   repository_directory_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   os.chdir(repository_directory_path) # Change the current working directory to the repository directory
   
   # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + '/' + repository_name
   update_thread = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   update_thread.wait() # Wait for the thread to finish
   os.chdir(DEFAULT_FOLDER) # Change the current working directory to the default one

# @brief: Clone the repository to the repository directory
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @return: None
def clone_repository(repository_name, repository_url):
   repository_directory_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   # Verify if the repository directory already exists and if it is not empty
   if os.path.isdir(repository_directory_path) and os.listdir(repository_directory_path):
      update_repository(repository_name) # Update the repository
      return
   else:
      print(f"{backgroundColors.GREEN}Cloning the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository...{Style.RESET_ALL}")
      # Create a thread to clone the repository
      thread = subprocess.Popen(["git", "clone", repository_url, repository_directory_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # Wait for the thread to finish
      thread.wait()
      print(f"{backgroundColors.GREEN}Successfully cloned the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository{Style.RESET_ALL}")

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

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def verify_ck_metrics_folder(repository_name):
   data_path = os.path.join(PATH, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]) # Join the PATH with the relative path of the ck metrics directory
   repo_path = os.path.join(data_path, repository_name) # Join the data path with the repository name
   commit_file = f"{repository_name}-commits_list{COMMIT_HASHES_FILE_EXTENSION}" # The name of the commit hashes file
   commit_file_path = os.path.join(data_path, commit_file) # Join the data path with the commit hashes file

   # Verify if the repository exists
   if not os.path.exists(commit_file_path):
      return False # Return False because the repository commit list does not exist

   # Read the commit hashes csv file and get the commit_hashes column, but ignore the first line
   commit_hashes = pd.read_csv(commit_file_path, sep=",", usecols=["commit hash"], header=0).values.tolist()

   # Verify if the repository exists
   i = 0
   for commit_hash in commit_hashes:
      commit_hash = commit_hash[0] # This removes the [] and the '' from the commit hash
      commit_file_filename = f"{i}-{commit_hash}" # The name of the folder
      folder_path = os.path.join(repo_path, commit_file_filename) # Join the repo path with the folder name
      i += 1

      if os.path.exists(folder_path): # Verify if the folder exists
         for ck_metric_file in CK_METRICS_FILES: # Verify if all the ck metrics files exist inside the folder
            ck_metric_file_path = os.path.join(folder_path, ck_metric_file)
            if not os.path.exists(ck_metric_file_path): # If the file does not exist
               return False # If the file does not exist, then the metrics are not calculated
   return True # If all the metrics are already calculated

# @brief: This function is used to checkout a specific branch
# @param: branch_name: Name of the branch to be checked out
# @return: None
def checkout_branch(branch_name):
   # Create a thread to checkout the branch
   checkout_thread = subprocess.Popen(["git", "checkout", branch_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   # Wait for the thread to finish
   checkout_thread.wait()

# @brief: This function is used to run the command that runs the CK metrics generator in a subprocess
# @param: cmd: Command to be executed
# @return: None
def run_ck_metrics_generator(cmd):
   # Create a thread to run the cmd command
   thread = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = thread.communicate()

# @brief: This function generates the output directory path for the CK metrics generator
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hash: Commit hash of the commit to be analyzed
# @param: commit_number: Number of the commit to be analyzed
# @return: The output_directory and relative_output_directory paths
def generate_output_directory_paths(repository_name, commit_hash, commit_number):
   output_directory = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}/{commit_number}-{commit_hash}/"
   relative_output_directory = f"{RELATIVE_CK_METRICS_DIRECTORY_PATH}/{repository_name}/{commit_number}-{commit_hash}/"
   return output_directory, relative_output_directory

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
   print(f"{backgroundColors.GREEN}{output_string}{backgroundColors.CYAN}{rounded_time} {time_unit}{Style.RESET_ALL}")

# @brief: This function outputs the execution time of the CK metrics generator
# @param: first_iteration_duration: Duration of the first iteration
# @param: elapsed_time: Elapsed time of the execution
# @param: number_of_commits: Number of commits to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def show_execution_time(first_iteration_duration, elapsed_time, number_of_commits, repository_name):
   estimated_time_string = f"Estimated time for running all the of the iterations in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
   output_time(estimated_time_string, round(first_iteration_duration * number_of_commits, 2))
   time_taken_string = f"Time taken to generate CK metrics for {backgroundColors.CYAN}{number_of_commits}{backgroundColors.GREEN} commits in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository: "
   output_time(time_taken_string, round(elapsed_time, 2))

# @brief: This function generates the diffs for the commits of a repository
# @param: repository_name - The name of the repository
# @param: commit_hash - The commit hash of the commit to be analyzed
# @param: commit_number - The number of the commit to be analyzed
# @return: None
def generate_diffs(repository_name, commit_hash, commit_number):
   # Loop through the modified files of the commit
   for modified_file in commit_hash.modified_files:
      file_diff = modified_file.diff # Get the diff of the modified file
      diff_file_directory = f"{PATH}{DEFAULT_DIFFS_DIRECTORY}/{repository_name}/{commit_number}-{commit_hash.hash}/" # Define the directory to save the diff file

      # Validate if the directory exists, if not, create it
      if not os.path.exists(diff_file_directory):
         os.makedirs(diff_file_directory, exist_ok=True) # Create the directory
      # Save the diff file
      with open(f"{diff_file_directory}{modified_file.filename}{DIFF_FILE_EXTENSION}", "w", encoding="utf-8", errors="ignore") as diff_file:
         diff_file.write(file_diff) # Write the diff to the file

# @brief: This function traverses the repository
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @param: number_of_commits: Number of commits to be analyzed
# @return: The commit hashes of the repository
def traverse_repository(repository_name, repository_url, number_of_commits):
   start_time = time.time()  # Start measuring time
   first_iteration_duration = 0  # Duration of the first iteration
   i = 1
   commit_hashes = []

   # Create a progress bar with the total number of commits
   with tqdm(total=number_of_commits, unit=f" {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} commits{Style.RESET_ALL}") as pbar:
      for commit in Repository(repository_url).traverse_commits():
         # Store the commit hash, commit message and commit date in one line of the list, separated by commas
         current_tuple = (commit.hash, commit.msg.split('\n')[0], commit.committer_date)
         commit_hashes.append(current_tuple)

         # Save the diff of the modified files of the current commit
         generate_diffs(repository_name, commit, i)

         # Change working directory to the repository directory
         workdir = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}"
         os.chdir(workdir)        

         # Checkout the commit hash branch to run ck
         checkout_branch(commit.hash)

         # Create the ck_metrics directory paths
         output_directory, relative_output_directory = generate_output_directory_paths(repository_name, commit.hash, i)
         # Create the ck_metrics directory
         create_directory(output_directory, relative_output_directory)

         # Change working directory to the repository directory
         os.chdir(output_directory)

         # Run ck metrics for the current commit hash
         cmd = f"java -jar {FULL_CK_JAR_PATH} {workdir} false 0 false {output_directory}"
         run_ck_metrics_generator(cmd)

         if i == 1:
            first_iteration_duration = time.time() - start_time  # Calculate the duration of the first iteration

         i += 1
         pbar.update(1) # Update the progress bar

   elapsed_time = time.time() - start_time  # Calculate elapsed time
   show_execution_time(first_iteration_duration, elapsed_time, number_of_commits, repository_name)

   return commit_hashes

# @brief: This function writes the commit hashes to a csv file
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hashes: List of tuples containing the commit hashes, commit messages and commit dates
# @return: None
def write_commit_hashes_to_csv(repository_name, commit_hashes):
   file_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}-commits_list{COMMIT_HASHES_FILE_EXTENSION}"
   with open(file_path, "w", newline='') as csv_file:
      writer = csv.writer(csv_file)
      # Write the header
      writer.writerow(["commit hash", "commit message", "commit date"])
      # Write the commit hashes
      writer.writerows(commit_hashes)

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

# @brief: Main function
# @param: None
# @return: None
def main():
   # Verify if the path constants contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   # Verify if the CK JAR file exists
   if not os.path.exists(FULL_CK_JAR_PATH):
      print(f"{backgroundColors.RED}The CK JAR file does not exist. Please download it and place it in {backgroundColors.CYAN}{RELATIVE_CK_JAR_PATH[0:RELATIVE_CK_JAR_PATH.find('/', 1)]}/{backgroundColors.RED}.{Style.RESET_ALL}")
      return

   print(f"{backgroundColors.GREEN}This script will process the repositories: {backgroundColors.CYAN}{list(DEFAULT_REPOSITORIES.keys())}{backgroundColors.GREEN} concurrently.{Style.RESET_ALL}")
   print(f"{backgroundColors.GREEN}The files that this script will generate are the {backgroundColors.CYAN}ck metrics files, the commit hashes list file and the diffs of each commit{backgroundColors.GREEN}.{Style.RESET_ALL}")
   
   process_repositories_concurrently()

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function