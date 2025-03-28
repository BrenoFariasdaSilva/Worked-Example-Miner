import atexit # For playing a sound when the program finishes
import concurrent.futures # For running tasks concurrently
import csv # For reading and writing CSV files
import json # For creating JSON output
import matplotlib.pyplot as plt # For creating plots, such as histograms
import numpy as np # For numerical operations
import os # For running a command in the terminal
import platform # For getting the operating system name
import random # For selecting random items
import requests # For making HTTP requests
import seaborn as sns # For creating plots with a high-level interface
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import sys # For exiting the program
import time # For sleeping the program
from collections import defaultdict # For counting the number of occurrences of each item
from colorama import Style # For coloring the terminal
from datetime import datetime, timedelta # For date manipulation
from dotenv import load_dotenv # For loading environment variables from .env file
from fpdf import FPDF # For creating PDFs
from glob import glob # For finding files matching a specified pattern

# Default values that can be changed:
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function
DATETIME_FILTER = None # The datetime filter for the repositories
HISTOGRAM_REPOSITORY_FIELDS = ["avg_code_churn", "avg_modified_files", "commits", "stars"] # The repository fields to create histograms
CANDIDATES = 3 # The number of repositories to select
EXCLUDE_REPOSITORIES_KEYWORDS = [] # Keywords to ignore in repository names
MINIMUM_COMMITS = 0 # The minimum number of commits a repository must have
MINIMUM_STARS = 50 # The minimum number of stars a repository must have
MAXIMUM_AVG_CODE_CHURN = None # The maximum average code churn allowed
MAXIMUM_AVG_FILES_MODIFIED = None # The maximum average files modified allowed
REPOSITORIES_SORTING_ATTRIBUTES = ["commits", "stars"] # The attribute to sort the repositories by

RUN_FUNCTIONS = { # Dictionary with the functions to run and their respective booleans
   "CSV Files": True, # Create CSV files for the repositories
	"Histograms": True, # Create histograms for the repositories
	"Save to PDF": True, # Save the repositories to a PDF file
	"Save to JSON": True, # Save the repositories to a JSON file
	"Scatter Plot": True, # Generate a scatter plot for the code churn
	"Show Candidate Repositories": False, # Randomly select repositories and print them
   "Reprocess Processed Repositories": False, # Reprocess the processed repositories
}

# Default paths:
START_PATH = os.getcwd() # Get the current working directory

# .Env Constants:
ENV_PATH = START_PATH.replace("PyDriller", ".env") # The path to the .env file
ENV_VARIABLE = "GITHUB_TOKEN" # The environment variable to load

# File Extensions Constants:
CSV_FILE_EXTENSION = ".csv" # The CSV file extension
PDF_FILE_EXTENSION = ".pdf" # The PDF file extension
PNG_FILE_EXTENSION = ".png" # The PNG file extension
JSON_FILE_EXTENSION = ".json" # The JSON file extension

# Global Set for the Processed Repositories:
PROCESSED_REPOSITORIES = set() # The set of processed repositories

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# Relative File Path Constants:
RELATIVE_REPOSITORIES_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories
RELATIVE_REPOSITORIES_HISTOGRAM_PNG_FILEPATH = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/repositories_histogram_DATA_TYPE{PNG_FILE_EXTENSION}" # The relative path of the directory that contains the histograms
RELATIVE_REPOSITORIES_LIST_PDF_FILEPATH = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/repositories_sorted_by_SORTING_ATTRIBUTE{PDF_FILE_EXTENSION}" # The relative path to the repositories PDF file
RELATIVE_REPOSITORIES_LIST_JSON_FILEPATH = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/repositories_sorted_by_SORTING_ATTRIBUTE{JSON_FILE_EXTENSION}" # The relative path to the repositories JSON file
RELATIVE_REPOSITORIES_CSV_FILEPATH = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/repositories_FIELD_NAME{CSV_FILE_EXTENSION}" # The relative path to the repositories CSV file
RELATIVE_REPOSITORIES_PNG_SCATTER_FILEPATH = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/respositories_FIELD_NAME_scatter_plot{PNG_FILE_EXTENSION}" # The relative path to the scatter plot file

# Full File Path Constants:
FULL_REPOSITORIES_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_REPOSITORIES_DIRECTORY_PATH}" # The full path of the directory that contains the repositories
FULL_REPOSITORIES_HISTOGRAM_PNG_FILEPATH = f"{START_PATH}{RELATIVE_REPOSITORIES_HISTOGRAM_PNG_FILEPATH}" # The full path of the directory that contains the histograms
FULL_REPOSITORIES_LIST_PDF_FILEPATH = f"{START_PATH}{RELATIVE_REPOSITORIES_LIST_PDF_FILEPATH}" # The full path to the repositories PDF file
FULL_REPOSITORIES_LIST_JSON_FILEPATH = f"{START_PATH}{RELATIVE_REPOSITORIES_LIST_JSON_FILEPATH}" # The full path to the repositories JSON file
FULL_REPOSITORIES_CSV_FILEPATH = f"{START_PATH}{RELATIVE_REPOSITORIES_CSV_FILEPATH}" # The full path to the repositories topics file
FULL_REPOSITORIES_PNG_SCATTER_FILEPATH = f"{START_PATH}{RELATIVE_REPOSITORIES_PNG_SCATTER_FILEPATH}" # The full path to the scatter plot file

# Color Constants:
class BackgroundColors: # Colors for the terminal
   CYAN = "\033[96m" # Cyan
   GREEN = "\033[92m" # Green
   YELLOW = "\033[93m" # Yellow
   RED = "\033[91m" # Red
   BOLD = "\033[1m" # Bold
   UNDERLINE = "\033[4m" # Underline
   CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Sound Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The commands to play a sound for each operating system
SOUND_FILE_PATH = ".assets/Sounds/NotificationSound.wav" # The path to the sound file

def verify_filepath_exists(filepath):
   """
   Verify if a file or folder exists at the specified path.

   :param filepath: Path to the file or folder
   :return: True if the file or folder exists, False otherwise
   """

   return os.path.exists(filepath) # Return True if the file or folder exists, False otherwise

def play_sound():
   """
   Plays a sound when the program finishes.

   :return: None
   """

   if verify_filepath_exists(SOUND_FILE_PATH): # If the sound file exists
      if platform.system() in SOUND_COMMANDS: # If the platform.system() is in the SOUND_COMMANDS dictionary
         os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE_PATH}") # Play the sound
      else: # If the platform.system() is not in the SOUND_COMMANDS dictionary
         print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
   else: # If the sound file does not exist
      print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE_PATH}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

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
   Verifies if the PATH constant contains whitespaces.

   :return: True if the PATH constant contains whitespaces, False otherwise.
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if the {BackgroundColors.CYAN}PATH{BackgroundColors.GREEN} constant contains whitespaces...{Style.RESET_ALL}")
   
   if " " in START_PATH: # Verify if the PATH constant contains whitespaces
      print(f"{BackgroundColors.RED}The {BackgroundColors.GREEN}{START_PATH}{BackgroundColors.RED} constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return True # Return True if the PATH constant contains whitespaces
   
   return False # Return False if the PATH constant does not contain whitespaces

def update_sound_file_path():
   """
   Updates the SOUND_FILE_PATH constant based on the current directory.
   If the current directory ends in "PyDriller", the prefix is "../",
   if it ends in "Scripts", the prefix is "../../", otherwise "./".
   """

   global SOUND_FILE_PATH # Declare SOUND_FILE_PATH as global to modify its value

   # Determine the appropriate prefix based on the current directory name
   if START_PATH.endswith("PyDriller"): # If the current directory is "PyDriller"
      prefix = "../" # Go up one directory
   elif START_PATH.endswith("Scripts"): # If the current directory is "Scripts"
      prefix = "../../" # Go up two directories
   else: # The current directory is not "PyDriller" or "Scripts", so it must be the root dir ("Worked-Example-Miner")
      prefix = "./" # Stay in the same directory

   SOUND_FILE_PATH = f"{prefix}{SOUND_FILE_PATH}" # Update the SOUND_FILE_PATH constant

   verbose_output(true_string=f"{BackgroundColors.GREEN}Updated the {BackgroundColors.CYAN}SOUND_FILE{BackgroundColors.GREEN} path to {BackgroundColors.CYAN}{SOUND_FILE_PATH}{Style.RESET_ALL}")

   return SOUND_FILE_PATH # Return the updated sound file path

def verify_git():
   """
   Verify if Git is installed.

   :return: True if Git is installed, False otherwise.
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if Git is installed...{Style.RESET_ALL}")

   try: # Try to run the git --version command
      subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Run the git --version command
   except subprocess.CalledProcessError as e: # Handle the exception if Git is not installed
      print(f"{BackgroundColors.RED}An error occurred while verifying if Git is installed: {BackgroundColors.YELLOW}{e}{BackgroundColors.RED}. Please install Git!{Style.RESET_ALL}")
      return False # Return False if Git is not installed
   return True # Return True if Git is installed

def get_directory_file_list(dir_path):
   """
   Get the list of files in a directory.

   :param dir_path: str - The path to the directory.
   :return: list - The list of files in the directory.
   """

   return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))] # Return the list of files in the directory

def is_directory_empty(path):
   """
   Checks if a directory is empty.

   :param path: str - The path to the directory.
   :return: bool - True if the directory is empty, False otherwise.
   """

   dir_files = get_directory_file_list(path) # Get the list of files in the directory

   return not dir_files # Return True if the directory is empty, False otherwise

def init_submodule(repo_path):
   """
   Initializes the submodule for a given repository.

   :param repo_path: str
   :return: True if the submodule was initialized successfully, False otherwise.
   """

   try: # Try to run the git submodule update --init --recursive command
      subprocess.run(["git", "-C", repo_path, "submodule", "update", "--init", "--recursive"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True) # Run the git submodule update --init --recursive command
      verbose_output(true_string=f"{BackgroundColors.GREEN}Submodule initialized successfully.{Style.RESET_ALL}")
      return True # Return True if the submodule was initialized successfully
   except subprocess.CalledProcessError as e: # Handle the exception if the command fails
      print(f"{BackgroundColors.RED}Error while initializing the submodule: {e}{Style.RESET_ALL}")
      return False # Return False if the submodule was not initialized successfully

def update_submodule(repo_path):
   """
   Updates the submodule for a given repository.

   :param repo_path: str
   :return: True if the submodule was updated successfully, False otherwise.
   """

   try: # Try to run the git submodule update --recursive command
      subprocess.run(["git", "-C", repo_path, "submodule", "update", "--recursive"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True) # Run the git submodule update --recursive command
      verbose_output(true_string=f"{BackgroundColors.GREEN}Submodule updated successfully.{Style.RESET_ALL}")
      return True # Return True if the submodule was updated successfully
   except subprocess.CalledProcessError as e: # Handle the exception if the command fails
      print(f"{BackgroundColors.RED}Error while updating the submodule: {e}{Style.RESET_ALL}")
      return False # Return False if the submodule was not updated successfully

def setup_submodule(repo_path):
   """
   Sets up the submodule for a given repository.

   :param repo_path: str
   :return: True if the submodule was set up successfully, False otherwise.
   """

   if not verify_filepath_exists(repo_path) or is_directory_empty(repo_path): # Verify if the repository path exists or is empty
      verbose_output(true_string=f"{BackgroundColors.GREEN}The repository path does not exist. Cloning the submodule repository...{Style.RESET_ALL}")
      return init_submodule(repo_path) # Initialize the submodule
   else: # The repository path exists, update the submodule
      verbose_output(true_string=f"{BackgroundColors.GREEN}The repository path exists. Updating the submodule repository...{Style.RESET_ALL}")
      return update_submodule(repo_path) # Update the submodule

def get_env_token(env_path=ENV_PATH, key=ENV_VARIABLE):
   """
   Verify if the .env file exists and if the desired key is present.

   :param env_path: Path to the .env file.
   :param key: The key to get in the .env file.
   :return: The value of the key if it exists.
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying the .env file...{Style.RESET_ALL}")

   # Verify if the .env file exists
   if not verify_filepath_exists(env_path):
      print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}.env file{BackgroundColors.RED} not found at {BackgroundColors.CYAN}{env_path}{Style.RESET_ALL}")
      sys.exit(1) # Exit the program

   load_dotenv(env_path) # Load the .env file
   api_key = os.getenv(key) # Get the value of the key

   # Verify if the key exists
   if not api_key:
      print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}{key}{BackgroundColors.RED} key was not found in the .env file located at {BackgroundColors.CYAN}{env_path}{Style.RESET_ALL}")
      sys.exit(1) # Exit the program

   return api_key # Return the value of the key

def build_headers(token):
   """
   Builds the headers for the GitHub API request.

   :param token: str
   :return: dict
   """

   return {
      "Authorization": f"token {token}", # Add the token to the headers
      "Accept": "application/vnd.github.v3+json" # Add the accept header
   }

def build_url(query, updated_after=None):
   """
   Builds the GitHub API request URL.

   :param query: str
   :param updated_after: str for filtering repositories updated after a certain time, this way we create a new query and bypass the 1000 results limit
   :return: str
   """

   updated_filter = f"+pushed:>{updated_after}" if updated_after else ""
   return f"https://api.github.com/search/repositories?q={query}{updated_filter}&sort=updated&order=asc&per_page=100"

def fetch_single_page(url, headers, page):
   """
   Fetches a single page of repositories from GitHub API.

   :param url: str
   :param headers: dict
   :param page: int
   :return: dict or None
   """

   response = requests.get(f"{url}&page={page}", headers=headers) # Make a GET request to the URL
   if response.status_code == 200:
      return response.json() # Get the JSON data from the response
   else:
      verbose_output(true_string=f"{BackgroundColors.RED}Failed to fetch page {page}: {response.status_code}{Style.RESET_ALL}")
      return None

def fetch_all_pages(url, headers):
   """
   Fetches all pages of repositories from GitHub API.

   :param url: str
   :param headers: dict
   :return: list
   """

   repositories = [] # The list of repositories
   page = 1 # The page number

   while True:
      response_data = fetch_single_page(url, headers, page) # Fetch a single page of data
      if not response_data or "items" not in response_data or not response_data["items"]:
         break # Break the loop if there are no items in the response

      repositories.extend(response_data["items"]) # Add the fetched repositories to the list
      page += 1 # Increment the page number

   return repositories # Return the list of repositories

def fetch_repositories(token):
   """
   Fetches the list of repositories from GitHub API.

   :param token: str
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Fetching the repositories...{Style.RESET_ALL}")

   headers = build_headers(token) # Build the request headers
   query = "topic:distributed-systems language:java" # The query to search for repositories

   all_repositories = [] # The list of all repositories
   updated_after = None # Start without a time filter

   while True: # Infinite loop to fetch all repositories
      url = build_url(query, updated_after) # Build the request URL with updated_after for pagination beyond 1000 results
      repositories = fetch_all_pages(url, headers) # Fetch repositories from all pages

      if not repositories: # If no repositories are returned
         break # Exit loop if no more repositories are returned

      all_repositories.extend(repositories) # Append fetched repositories to the complete list

      updated_after = repositories[-1]["updated_at"] # Get the timestamp of the last fetched repository to continue fetching from there

      if len(repositories) < 100: # Break if the number of repositories fetched is less than 100 (no more pages)
         break # Exit the loop

   return all_repositories

def get_threads():
   """
   Get the number of available cpu cores.

   return: The number of cpu cores.
   """
   
   cpu_cores = os.cpu_count() # Get the number of CPU cores

   return cpu_cores # Return the number of CPU cores

def get_adjusted_number_of_threads(cpu_count):
   """
   Get the adjusted number of threads to use based on the available CPU cores, following these rules:

   - Ensure at least 1 thread is used.
   - Always try leave at least 1 thread free.
   - If there are 8 or more cores, leave 2 threads free, so the system can still be usable in terms of cpu usage, but memory wise it will also be very high.

   :param cpu_count: int
   :return: tuple (int, int)
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Adjusting the number of threads to use...{Style.RESET_ALL}")

   if cpu_count <= 2: # If there are 2 or fewer CPU cores
      usable_threads = 1 # Use 1 thread
   elif 3 <= cpu_count <= 7: # If there are between 3 and 7 CPU cores
      usable_threads = cpu_count - 1 # Leave 1 thread free
   else: # If there are 8 or more CPU cores
      usable_threads = cpu_count - 2 # Leave 2 threads free

   usable_threads = max(1, usable_threads) # Ensure at least 1 thread is used

   return usable_threads, cpu_count # Return the number of threads to use and the maximum number of threads available

def get_datetime_filter(days=DATETIME_FILTER):
   """
   Calculates the date filter for the repositories.

   :param days: Number of days to go back from today. If None, return the earliest possible datetime.
   :return: datetime
   """

   if days is None:
      return datetime.min # Return the earliest possible datetime (since "forever")
   else:
      return datetime.now() - timedelta(days=days) # Return datetime "days" ago

def get_processed_repositories_names():
   """
   Get the processed repositories names from the Worked-Example-Miner-Candidates directory.

   :return: set - Unique names from both candidates and worked examples directories.
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Fetching processed repository names from the Worked-Example-Miner-Candidates Submodule directory...{Style.RESET_ALL}")

   # Get first-level subdirectories inside candidates/*/
   candidates_dirs = glob("../Worked-Example-Miner-Candidates/candidates/*/") # Candidate category directories
   candidates_names = [] # Initialize the list of candidate names
   
   for dir_path in candidates_dirs: # Iterate over the candidate directories
      # Fetch second-level directory names within each candidate subdirectory
      subdir_paths = glob(os.path.join(dir_path, "*/")) # Second-level directories
      candidates_names.extend([os.path.basename(os.path.normpath(subdir).lower()) for subdir in subdir_paths]) # Add the second-level directory names to the list

   # Get the worked_examples/*/ directory names directly
   worked_examples_dirs = glob("./Worked-Example-Miner-Candidates/worked_examples/*/") # Worked examples directories
   worked_examples_names = [os.path.basename(os.path.normpath(path).lower()) for path in worked_examples_dirs] # Get the worked examples directory names

   return set(candidates_names + worked_examples_names) # Combine and return unique names from both candidates and worked examples

def contains_excluded_keywords(repo, ignore_keywords):
   """
   Verifies if the repository's name or description contains any excluded keywords.

   :param repo: dict
   :param ignore_keywords: list
   :return: bool
   """

   repo_name = repo["name"].lower() # Get the name of the repository
   repo_description = (repo["description"] or "").lower() # Get the description of the repository

   return any(
      keyword.lower() in repo_name or keyword.lower() in repo_description # Verify if the keyword is in the name or description
      for keyword in ignore_keywords # Iterate over the ignore keywords
   )

def is_repository_valid(repo, updated_date, date_filter, ignore_keywords):
   """
   Verifies if the repository is valid based on the update date, star count, and keywords.

   :param repo: dict
   :param updated_date: datetime
   :param date_filter: datetime to filter the repositories
   :param ignore_keywords: list
   :return: bool
   """

   return (
      updated_date > date_filter # Verify if the repository was updated after the date filter
      and repo["stargazers_count"] >= MINIMUM_STARS # Verify if the repository has the minimum number of stars
      and not contains_excluded_keywords(repo, ignore_keywords) # Verify if the repository has the excluded keywords
   )

def parse_repo_updated_date(repo):
   """
   Parses the repository's last updated date from its string format.

   :param repo: dict
   :return: datetime
   """

   return datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ") # Parse the date string to a datetime object

def extract_author_name(repo):
   """
   Extracts the author's name from the repository's URL.

   :param repo: dict
   :return: str
   """

   return repo["html_url"].split("/")[-2] # Get the author's name from the URL

def run_git_log_numstat(repo_path):
   """
   Runs the 'git log --numstat' command for a given repository.

   :param repo_path: str
   :return: list of lines from the git numstat output or an empty list in case of an error.
   """

   try:
      # Run the git command to get the numstat output
      result = subprocess.run(
         ["git", "-C", repo_path, "log", "--pretty=tformat:", "--numstat"], # The git command to run
         capture_output=True, # Capture the output
         text=True, # Get the output as text
         check=True # Check if the command was successful
      )

      lines = result.stdout.strip().splitlines() # Get the lines from the output
      return lines # Return the lines
   except subprocess.CalledProcessError as e: # Handle the exception if the command fails
      print(f"{BackgroundColors.RED}Error while running git log --numstat: {e}{Style.RESET_ALL}")
      return [] # Return an empty list in case of an error

def is_within_limit(value, limit, check_upper=True):
   """
   Generic function to check if the value is within the limit.

   :param value: The value to check.
   :param limit: The limit (can be upper or lower limit).
   :param check_upper: If True, checks for upper limit; if False, checks for lower limit.
   :return: True if value is within the limit or if the limit is None, False otherwise.
   """

   if limit is None: # If the limit is None
      return True # Return True
   return value < limit if check_upper else value > limit # Return True if the value is within the limit (upper or lower)

def process_numstat_metrics(lines):
   """
   Processes git numstat lines to calculate total added, removed, code churn, and files modified.

   :param lines: list of numstat output lines
   :return: list containing:
      - total added lines
      - total removed lines
      - total code churn (added - removed)
      - total files modified
   """

   metrics = [0, 0, 0, 0] # Initialize the metrics list: [total_added, total_removed, total_code_churn, total_files_modified]

   for line in lines: # Iterate over the lines
      if line: # If the line is not empty
         parts = line.split() # Split the line by whitespace
         if len(parts) == 3: # Ensure the line has the expected format (added, removed, file path)
            try: # Try to parse the added and removed lines
               added = int(parts[0]) if parts[0] != "-" else 0 # Get the added lines
               removed = int(parts[1]) if parts[1] != "-" else 0 # Get the removed lines
               metrics[0] += added # Total Lines Added
               metrics[1] += removed # Total Lines Removed
               metrics[2] += (added - removed) # Total Code Churn
               metrics[3] += 1 # Total Files Modified
            except ValueError as e: # Handle the exception if there's an error parsing the numstat output
               print(f"{BackgroundColors.RED}Error while parsing numstat output: {e}{Style.RESET_ALL}")

   return metrics # Return the list of metrics

def calculate_average_metrics(repo_path, repo_name, total_commits, lines=None):
   """
   Calculates the average code churn and average files modified for all commits in a repository.

   :param repo_path: str
   :param repo_name: str
   :param total_commits: int
   :param lines: list of numstat output lines (optional)
   :return: tuple containing:
      - average code churn (float)
      - average files modified per commit (float)
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating average metrics for the {BackgroundColors.CYAN}{repo_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

   lines = run_git_log_numstat(repo_path) if not lines else lines # Get the numstat output if not provided

   if not lines: # If there are no lines
      return 0, 0 # Return 0 for both if there's an error

   metrics = process_numstat_metrics(lines) # Process the numstat metrics

   avg_code_churn = metrics[2] / total_commits if total_commits > 0 else 0 # Calculate the average code churn
   avg_files_modified = metrics[3] / total_commits if total_commits > 0 else 0 # Calculate the average files modified

   return avg_code_churn, avg_files_modified # Return the average code churn and files modified

def get_autometric_dir():
   """
   Returns the path to the AutoMetric directory.

   :return: str - The path to the AutoMetric directory.
   """

   return START_PATH.replace("PyDriller", "AutoMetric")

def build_command(repo_url, autometric_dir, github_token):
   """
   Builds the command to execute the AutoMetric script.

   :param repo_url: str - The URL of the repository.
   :param autometric_dir: str - The path to the AutoMetric directory.
   :param github_token: str - The GitHub token.
   :return: list - The command to execute.
   """

   return ["make", "-C", autometric_dir, f"args=--repo_urls {repo_url} --github_token {github_token}"]

def execute_subprocess(cmd):
   """
   Executes the given command and returns the result.

   :param cmd: list - The command to execute.
   :return: CompletedProcess - The result of the command execution.
   """

   return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def get_repo_owner_and_name(repo_url):
   """
   Gets the repository owner and name from the repository URL.

   :param repo_url: str - The URL of the repository.
   :return: tuple - The repository owner and name.
   """

   return repo_url.split("/")[-2:] # Get the repository owner and name

def get_output_file(repo_owner, repo_name, autometric_dir):
   """
   Gets the output file path based on the repository URL.

   :param repo_owner: str - The owner of the repository.
   :param repo_name: str - The name of the repository.
   :param autometric_dir: str - The path to the AutoMetric directory.
   :return: str - The output file path.
   """

   output_file = os.path.join(autometric_dir, f"output/{repo_owner}-{repo_name}.json") # Get the output file path
   return output_file # Return the output file path

def wait_until_file_is_created(file_path, timeout=60):
   """
   Waits until the file is created or until a timeout occurs.

   :param file_path: str - The path to the file.
   :param timeout: int - Maximum time to wait for the file to be created (in seconds).
   :return: bool - True if the file was created, False otherwise.
   """

   start_time = time.time() # Record the start time
   while not verify_filepath_exists(file_path): # While the file does not exist
      if time.time() - start_time > timeout: # If the timeout is reached
         print(f"{BackgroundColors.RED}Timeout: The file {file_path} was not created in time.{Style.RESET_ALL}")
         return False # Return False if the file was not created in time
      time.sleep(1) # Wait for 1 second
   return True # Return True if the file was created

def load_metrics(output_file):
   """
   Loads metrics from the output JSON file.

   :param output_file: str - The path to the output JSON file.
   :return: dict - The metrics loaded from the file.
   """

   try: # Try to load the metrics from the JSON file
      with open(output_file, "r") as file: # Open the JSON file
         metrics = json.load(file) # Load the metrics from the JSON file
      return metrics[0] if metrics else {} # Return the metrics if they exist
   except (FileNotFoundError, json.JSONDecodeError) as e: # Handle the exception if the file is not found or there's an error decoding the JSON file
      print(f"{BackgroundColors.RED}Error loading metrics from {output_file}: {e}{Style.RESET_ALL}")
      return {} # Return an empty dictionary

def get_autometric_metrics(repo_url, github_token=None):
   """
   Executes the AutoMetric script to gather metrics for a given repository URL.

   :param repo_url: str - The URL of the repository.
   :param github_token: str - The GitHub token.
   :return: dict - The metrics gathered by the AutoMetric script.
   """

   github_token = get_env_token() if not github_token else github_token # Get the GitHub token
   autometric_dir = get_autometric_dir() # Get the path to the AutoMetric directory
   cmd = build_command(repo_url, autometric_dir, github_token) # Build the command

   result = execute_subprocess(cmd) # Run the command in a subprocess
   
   repo_metrics = {} # Initialize the AutoMetric metrics dictionary for the repository

   if result.returncode == 0: # If the script ran successfully
      repo_owner, repo_name = get_repo_owner_and_name(repo_url) # Get the repository owner and name
      output_file = get_output_file(repo_owner, repo_name, autometric_dir) # Get the output file path      
      repo_metrics = load_metrics(output_file) if wait_until_file_is_created(output_file) else {} # Load the metrics from the output file
   else: # If the script did not run successfully
      print(f"{BackgroundColors.RED}Error while running AutoMetric script: {result.stderr}{Style.RESET_ALL}")

   return repo_metrics # Return the AutoMetric metrics for the repository

def fill_repository_dict_fields(repo, autometric_metrics, avg_code_churn, avg_files_modified, commits_count):
   """
   Fills the repository dictionary with relevant metrics and information.

   :param repo: dict - The repository information.
   :param autometric_metrics: dict - Metrics gathered from AutoMetric.
   :param avg_code_churn: float - The average code churn.
   :param avg_files_modified: float - The average number of modified files.
   :param commits_count: int - The total number of commits in the repository.
   :return: dict - The filled repository dictionary.
   """

   return { # Return the filled repository dictionary
      "name": repo["name"].encode("utf-8").decode("utf-8"), # Encode and decode the name to handle special characters
      "author": extract_author_name(repo).encode("utf-8").decode("utf-8"), # Encode and decode the author's name to handle special characters
      "url": repo["html_url"], # Get the URL of the repository
      "description": repo["description"].encode("utf-8").decode("utf-8"), # Encode and decode the description to handle special characters
      "topics": ", ".join(repo["topics"]), # Get the topics of the repository
      "commits": commits_count, # Get the number of commits
      "stars": repo["stargazers_count"], # Get the number of stars
      "forks_counter": repo["forks_count"], # Get the number of forks
      "open_issues_counter": repo["open_issues_count"], # Get the number of open issues
      "avg_code_churn": int(avg_code_churn), # Get the average code churn
      "avg_modified_files": int(avg_files_modified), # Get the average files modified
      "number_of_contributors": autometric_metrics.get("Number of Contributors", "n/a"), # Get the number of contributors
      "inactive_period": autometric_metrics.get("Inactive Period", "n/a"), # Get the inactive period
      "mttu": autometric_metrics.get("MTTU", "n/a"), # Get the Mean Time to Update (MTTU)
      "mttc": autometric_metrics.get("MTTC", "n/a"), # Get the Mean Time to Close (MTTC)
      "branch_protection": autometric_metrics.get("Branch Protection", "n/a"), # Get the branch protection status
      "updated_at": repo["updated_at"], # Get the last update date
      # "pull_requests": repo.get("pulls_count", 0), # Get the number of pull requests (Apparently this endpoint aint working)
      "license": repo["license"]["name"] if repo.get("license") else "No license specified", # Get the license name or specify if there is no license
      "are_candidates_generated": repo["name"].lower() in PROCESSED_REPOSITORIES # Boolean to indicate if the repository's candidates have been generated
   }

def process_repository(repo, token, date_filter=None, ignore_keywords=None):
   """
   Processes a single repository, filtering by date, keywords, and ensuring a unique name.

   :param repo: dict
   :param token: str
   :param date_filter: datetime to filter the repositories
   :param ignore_keywords: list
   :return: dict or None
   """

   updated_date = parse_repo_updated_date(repo) # Get the last update date of the repository

   if is_repository_valid(repo, updated_date, date_filter, ignore_keywords): # Validate the repository based on the update date, star count, and keywords
      setup_repository(repo["name"], repo["html_url"]) # Setup the repository: Clone or update it so we can calculate the code churn and commit count
      repo_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repo['name']}/" # The path to the repository directory
      commits_count = count_commits(repo_path) # Count the number of commits in the repository
      numstat_lines = run_git_log_numstat(repo_path) # Get numstat output

      if is_within_limit(commits_count, MINIMUM_COMMITS, False): # If the number of commits is greater than the minimum
         avg_code_churn, avg_files_modified = calculate_average_metrics(repo_path, repo["name"], commits_count, numstat_lines) # Calculate the average code churn and files modified
         if is_within_limit(avg_code_churn, MAXIMUM_AVG_CODE_CHURN, True) and is_within_limit(avg_files_modified, MAXIMUM_AVG_FILES_MODIFIED, True): # If the average code churn and files modified are within the limits
            autometric_metrics = get_autometric_metrics(repo["html_url"], token) # Get metrics from AutoMetric and integrate into repo_dict
            filled_repo_dict = fill_repository_dict_fields(repo, autometric_metrics, avg_code_churn, avg_files_modified, commits_count) # Fill the repository dictionary with relevant metrics and information
            return filled_repo_dict # Return the filled repository dictionary

   return None # Return None if the repository is not valid

def update_repository(repository_directory_path):
   """
   Update the repository using "git pull".

   :param repository_directory_path: The path to the repository directory
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Updating the {BackgroundColors.CYAN}{repository_directory_path.split('/')[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   os.chdir(repository_directory_path) # Change the current working directory to the repository directory
   
   update_thread = subprocess.Popen(["git", "pull", "--force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Create a thread to update the repository
   update_thread.wait() # Wait for the thread to finish

   os.chdir(START_PATH) # Change the current working directory to the default one

def get_default_branch_name(repository_directory_path):
   """
   Get the default branch name of the repository.

   :param repository_directory_path: The path to the repository directory
   :return: str
   """

   branch_thread = subprocess.Popen(["git", "-C", repository_directory_path, "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Create a thread to get the default branch name
   branch_name, _ = branch_thread.communicate() # Get the current branch name
   return branch_name.decode("utf-8").strip() # Decode and strip whitespace

def checkout_latest_commit(repository_directory_path):
   """
   Check out the latest commit (HEAD) of the repository.

   :param repository_directory_path: The path to the repository directory
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Checking out the latest commit of the {BackgroundColors.CYAN}{repository_directory_path.split('/')[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

   os.chdir(repository_directory_path) # Change to the repository directory

   # Pull the latest changes from the default branch and force checkout to HEAD
   checkout_thread = subprocess.Popen(["git", "pull", "origin", get_default_branch_name(repository_directory_path), "--force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   checkout_thread.wait() # Wait for the checkout command to finish

   os.chdir(START_PATH) # Change back to the original directory

def clone_repository(repository_directory_path, repository_url):
   """
   Clone the repository to the repository directory.

   :param repository_directory_path: The path to the repository directory
   :param repository_url: URL of the repository to be analyzed
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Cloning the {BackgroundColors.CYAN}{repository_directory_path.split('/')[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   try: # Try to clone the repository
      thread = subprocess.Popen(["git", "clone", repository_url, repository_directory_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Create a thread to clone the repository
      stdout, stderr = thread.communicate() # Wait for the thread to finish and capture output
      
      if thread.returncode != 0: # Check for errors during cloning
         print(f"{BackgroundColors.RED}Error cloning repository: {BackgroundColors.GREEN}{stderr.decode().strip()}{Style.RESET_ALL}") # Print error message if cloning fails
   except Exception as e:
      print(f"{BackgroundColors.RED}An error occurred while cloning the repository: {BackgroundColors.GREEN}{e}{Style.RESET_ALL}")

def setup_repository(repository_name, repository_url):
   """"
   Setup the repository by cloning it or updating it if it already exists.

   :param repository_name: Name of the repository to be analyzed
   :param repository_url: URL of the repository to be analyzed
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Setting up the {BackgroundColors.CYAN}{repository_name}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   repository_directory_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}" # The path to the repository directory
   
   if os.path.isdir(repository_directory_path) and os.listdir(repository_directory_path): # Verify if the repository directory already exists and if it is not empty
      update_repository(repository_directory_path) # Update the repository
      checkout_latest_commit(repository_directory_path) # Check out to the latest commit
   else: # If the repository directory does not exist or is empty
      clone_repository(repository_directory_path, repository_url) # Clone the repository

def count_commits(repo_path):
   """
   Counts the number of commits in a repository using the git command.

   :param repo_path: str
   :return: int
   """

   try:
      # Run the git command to count commits
      result = subprocess.run(
         ["git", "-C", repo_path, "rev-list", "--count", "HEAD"], # The git command to run
         capture_output=True, # Capture the output
         text=True, # Get the output as text
         check=True # Check if the command was successful
      )
      return int(result.stdout.strip()) # Return the commit count as an integer
   except subprocess.CalledProcessError as e: # Handle the exception if the command fails
      print(f"Error while counting commits: {e}")
      return 0 # Return 0 or handle the error as needed

def process_repository_task(repo, token, datetime_filter, ignore_keywords):
   """
   Processes and filters a single repository.

   :param repo: dict
   :param token: str
   :param datetime_filter: datetime to filter the repositories
   :param ignore_keywords: list
   :return: dict or None
   """

   filtered_repo = process_repository(repo, token, datetime_filter, ignore_keywords) # Process the repository
   return filtered_repo if filtered_repo else None # Return the repository if it is valid, otherwise return None

def filter_repositories(repositories, token, ignore_keywords=EXCLUDE_REPOSITORIES_KEYWORDS):
   """
   Filters the list of repositories based on the update date, ignore keywords, and ensures unique names.
   This function uses concurrent processing to speed up the filtering process based on the number of available CPU cores.

   :param repositories: list
   :param token: str
   :param ignore_keywords: list
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Applying repository filtering criteria...{Style.RESET_ALL}")

   usable_threads, max_threads = get_adjusted_number_of_threads(get_threads()) # Get the adjusted number of threads to use
   
   verbose_output(true_string=f"{BackgroundColors.GREEN}Using {BackgroundColors.CYAN}{usable_threads}{BackgroundColors.GREEN} of {BackgroundColors.CYAN}{max_threads}{BackgroundColors.GREEN} threads available...{Style.RESET_ALL}")

   datetime_filter = get_datetime_filter() # Get the datetime filter for the repositories

   filtered_repositories = [] # The list of filtered repositories. Each repository is a dict

   global PROCESSED_REPOSITORIES # Global variable to store the processed repositories
   PROCESSED_REPOSITORIES = get_processed_repositories_names() # Get the processed repositories names

   with concurrent.futures.ThreadPoolExecutor(max_workers=usable_threads) as executor: # Create a ThreadPoolExecutor with the number of threads to use
      futures = [executor.submit(process_repository_task, repo, token, datetime_filter, ignore_keywords) for repo in repositories] # Submit the process_repository_task function to the executor for each repository

      for future in concurrent.futures.as_completed(futures): # Iterate over the futures as they are completed
         try: # Try to get the result of the future
            result = future.result() # Raises exception if any occurred during execution
            if result: # If the result is not None
               filtered_repositories.append(result) # Append the repository to the list
         except Exception as exc: # Handle the exception if any occurred during execution
               print(f"{BackgroundColors.RED}Error occurred: {BackgroundColors.GREEN}{exc}{Style.RESET_ALL}")

   return filtered_repositories # Return the list of filtered repositories

def create_directory(full_directory_name, relative_directory_name):
   """
   Creates a directory.

   :param full_directory_name: Name of the directory to be created.
   :param relative_directory_name: Relative name of the directory to be created that will be shown in the terminal.
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Creating the {BackgroundColors.CYAN}{relative_directory_name}{BackgroundColors.GREEN} directory...{Style.RESET_ALL}")

   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      return # Return if the directory already exists
   try: # Try to create the directory
      os.makedirs(full_directory_name) # Create the directory
   except OSError: # If the directory cannot be created
      print(f"{BackgroundColors.GREEN}The creation of the {BackgroundColors.CYAN}{relative_directory_name}{BackgroundColors.GREEN} directory failed.{Style.RESET_ALL}")

def save_to_json(data, filename=FULL_REPOSITORIES_LIST_JSON_FILEPATH):
   """
   Saves the data to a JSON file.

   :param data: dict
   :param filename: str
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Saving the data to {BackgroundColors.CYAN}{filename}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

   create_directory(FULL_REPOSITORIES_DIRECTORY_PATH, RELATIVE_REPOSITORIES_DIRECTORY_PATH) # Create the output directory

   with open(filename, "w") as json_file: # Open the JSON file
      json.dump(data, json_file, ensure_ascii=False, indent=3) # Dump the data to the JSON file

def add_pdf_header(pdf, num_candidates, sorting_attribute):
   """
   Adds a header to the PDF.

   :param pdf: FPDF object
   :param num_candidates: int, number of repositories
   :param sorting_attribute: str, the attribute to sort the repositories by
   :return: None
   """

   pdf.set_font("Helvetica", size=12) # Set the font to Helvetica with size 12

   # Header
   pdf.set_font("Helvetica", "B", 12) # Set font to bold
   pdf.set_text_color(0, 102, 204) # Set font color to a sky blue shade

   # Format the current date
   current_date = datetime.now().strftime("%d %B %Y") # Format: 01 January 2022
   current_time = datetime.now().strftime("%Hh %Mm %Ss") # Format: 12h 34m 56s

   header_text = ( # Header text
      f"Repositories List Sorted by {sorting_attribute.capitalize()}\n" # Title
      f"Number of Candidates: {num_candidates}\n" # Number of repositories
      f"Generated on: {current_date} at {current_time}" # Current date and time of generation
   )

   pdf.set_y(10) # Set vertical position
   pdf.multi_cell(0, 8, header_text, align="C") # Reduced line height
   pdf.ln(5) # Reduced line break after header

def add_pdf_column_headers(pdf):
   """
   Adds column headers to the PDF.

   :param pdf: FPDF object
   :return: None
   """

   pdf.set_font("Helvetica", "B", 10) # Bold font
   pdf.set_fill_color(200, 220, 255) # Light blue color for headers
   pdf.set_text_color(0, 0, 0) # Reset font color to black
   pdf.set_x(10) # Set the start x position
   pdf.cell(120, 10, "Name (Hyperlink)", border=1, fill=True) # Name column
   pdf.cell(20, 10, "Commits", border=1, fill=True) # Commits column
   pdf.cell(15, 10, "Stars", border=1, fill=True) # Stars column
   pdf.cell(35, 10, "Last Update", border=1, fill=True) # Last Update column
   pdf.ln() # Line break

def format_last_update_date(last_update):
   """
   Formats the last update date of the repository.

   :param last_update: str, the ISO date string from the repository data
   :return: str, formatted date or "Unknown" if parsing fails
   """

   try: # Try to parse the date
      last_update_date = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%SZ") # Parse the date
      return last_update_date.strftime("%d %B %Y") # Format: 01 January 2022
   except ValueError: # Handle the exception if the date parsing fails
      return "Unknown" # Fallback if date parsing fails

def add_pdf_data_rows(pdf, data):
   """
   Adds repository data rows to the PDF.

   :param pdf: FPDF object
   :param data: list of dict
   :return: None
   """

   pdf.set_font("Helvetica", size=10) # Set the font to Helvetica with size 10

   for repo in data: # Iterate over the repositories
      name = repo.get("name", "") # Get the name of the repository
      author = repo.get("author", "") # Get the author of the repository
      url = repo.get("url", "") # Get the URL of the repository
      commits = str(repo.get("commits", "")) # Get the number of commits
      stars = str(repo.get("stars", "")) # Get the number of stars
      last_update = repo.get("updated_at", "") # Get the last update date of the repository
      last_update = format_last_update_date(last_update) # Parse and format last update date

      pdf.set_x(10) # Set the start x position

      # Name (Hyperlink)
      pdf.set_text_color(0, 0, 255) # Set color to blue for hyperlinks
      pdf.cell(120, 10, f"{author}/{name}", border=1, link=url) # Name (Hyperlink) is the "author/repository_name" of the repository
      pdf.set_text_color(0, 0, 0) # Reset text color to black
      pdf.cell(20, 10, commits, border=1) # Commits
      pdf.cell(15, 10, stars, border=1) # Stars
      pdf.cell(35, 10, last_update, border=1) # Last Update
      pdf.ln() # Line break

def save_to_pdf(data, sorting_attribute, filename=FULL_REPOSITORIES_LIST_PDF_FILEPATH):
   """
   Saves the data to a PDF file.

   :param data: list of dict
   :param sorting_attribute: str, the attribute to sort the data by
   :param filename: str
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Saving the data to {BackgroundColors.CYAN}{filename}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

   pdf = FPDF() # Create a PDF object
   pdf.add_page() # Add a page to the PDF

   add_pdf_header(pdf, len(data), sorting_attribute) # Add header section
   add_pdf_column_headers(pdf) # Add column headers
   add_pdf_data_rows(pdf, data) # Add data rows

   pdf.output(filename) # Save the PDF file

def extract_repositories_field(repositories, repository_field):
   """
   Extract the number of commits from repositories.

   :param repositories: list of repositories (dicts)
   :param repository_field: the name of the field containing the desired data
   :return: list of data from the repositories of the repository field
   """

   return [repo[repository_field] for repo in repositories] # Return the data for each repository

def calculate_statistics(data):
   """
   Calculate and print the statistics (min_value, max_value, average, median, and standard deviation) for a given dataset.

   :param data: list of integers
   :return: tuple of floats (min_value, max_value, average, median, std_dev)
   """

   min_value = min(data) # Get the minimum value
   max_value = max(data) # Get the maximum value
   average = np.mean(data) # Calculate the average
   median = np.median(data) # Calculate the median
   std_dev = np.std(data) # Calculate the standard deviation

   return min_value, max_value, average, median, std_dev # Return the calculated statistics

def create_basic_histogram(data, title, xlabel, ylabel, filename):
   """
   Create a histogram for the given data.

   :param data: list of integers to plot
   :param title: title of the histogram
   :param xlabel: label for the x-axis
   :param ylabel: label for the y-axis
   :param filename: name of the file to save the histogram
   :return: None
   """

   plt.figure(figsize=(10, 6)) # Set the figure size
   counts, bins, patches = plt.hist(data, bins=20, color="skyblue", edgecolor="black") # Create the histogram
   plt.title(title) # Set the title of the histogram
   plt.xlabel(xlabel) # Set the x-axis label
   plt.ylabel(ylabel) # Set the y-axis label
   plt.grid(True) # Enable the grid
   plt.tight_layout() # Adjust the layout
   
   # Annotate each bar with its height
   for count, x in zip(counts, bins[:-1]):
      if count > 0: # Verify if the count is greater than 0 (Bar Exists)
         plt.annotate(f"{int(count)}", 
                        xy=(x + (bins[1] - bins[0]) / 2, count), # Center of the bar
                        xytext=(0, 5), # Offset the text a little above the bar
                        textcoords="offset points", # Offset the text
                        ha="center") # Center the text horizontally
   
   plt.savefig(filename) # Save the histogram to a file
   plt.close() # Close the plot

def create_repository_field_histogram(repositories, repository_field):
   """
   Create a histogram for the specified repository field.

   :param repositories: list of repositories (dicts)
   :param repository_field: the name of the field containing the desired data
   :return: None
   """

   repositories_data = extract_repositories_field(repositories, repository_field) # Extract the data for the repository field

   min_value, max_value, average, median, std_dev = calculate_statistics(repositories_data) # Calculate and display statistics for the repository field
   histogram_title = f"Histogram of {repository_field.capitalize()}\nMin: {int(min_value)}, Max: {int(max_value)}, Average: {int(average)}, Median: {int(median)}, Standard Deviation: {int(std_dev)}" # Title of the histogram
   commits_histogram_filepath = FULL_REPOSITORIES_HISTOGRAM_PNG_FILEPATH.replace("DATA_TYPE", repository_field) # Replace "DATA_TYPE" with the repository field in the histogram file path
   create_basic_histogram(repositories_data, histogram_title, f"Number of {repository_field}", f"Number of Repositories (Total {len(repositories_data)})", commits_histogram_filepath) # Create a histogram for the repository field in the repositories

def create_histograms(repositories):
   """
   Create histograms for the repository fields in the HISTORY_REPOSITORY_FIELDS list.

   :param repositories: list of repositories (dicts)
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Creating histograms for the repositories...{Style.RESET_ALL}")

   for repository_field in HISTOGRAM_REPOSITORY_FIELDS: # Iterate over the repository fields
      create_repository_field_histogram(repositories, repository_field) # Create a histogram for the repository field

def collect_field_values_from_list(data_list, field_name):
   """
   Collect the values from the specified field in the list of repositories and track where they appeared.

   :param data_list: list containing the data values
   :param field_name: the field name to collect and sort
   :return: dictionary with field values as keys and lists of repository names as values
   """

   value_to_repos = defaultdict(list) # Dictionary to store values and corresponding repository names

   def add_values(values, repo_name): # Helper function to handle adding values to the dictionary
      for value in values: # Iterate over the values
         value_to_repos[value].append(repo_name) # Add the value and repository name to the dictionary

   for data in data_list: # Iterate over the repositories, in order to collect the field values
      if field_name in data: # If the field is present in the data
         repo_name = f"{data.get('author', 'Unknown Author')}/{data.get('name', 'Unknown Repo')}".capitalize() # Get the repository name with the author
         field_data = data[field_name] # Get the data for the field

         # Handle the field data based on its type
         if isinstance(field_data, str): # If the field is a string
            values_list = field_data.split(", ") if ", " in field_data else [field_data] # Split by comma and space or treat as a single value
            add_values(values_list, repo_name) # Add the values and repo name
         elif isinstance(field_data, (int, float)): # If the field is an integer or float
            add_values([field_data], repo_name) # Add the value and repo name
         elif isinstance(field_data, list): # If the field is a list
            add_values(field_data, repo_name) # Add the values from the list
         elif isinstance(field_data, dict): # If the field is a dictionary
            add_values(field_data.values(), repo_name) # Add the values from the dictionary
      else:
         print(f"{BackgroundColors.RED}Field {field_name} not found in the data.{Style.RESET_ALL}")

   return value_to_repos # Return the dictionary of values and repository names

def sort_values_by_occurrences(values):
   """
   Sort the values by occurrences (number of repositories they appeared in) and return a list of tuples with the value, 
   its occurrences count, and the repositories list (as a comma-separated string).

   :param values: dictionary with values as keys and lists of repository names as values
   :return: list of tuples with value, occurrences, and repositories (as a comma-separated string)
   """

   sorted_values = sorted(values.items(), key=lambda x: len(x[1]), reverse=True) # Sort by occurrences (number of repositories)
   formatted_values = [(value, len(repos), ", ".join(repos)) for value, repos in sorted_values] # Transform the sorted values into a list of tuples (value, occurrences count, comma-separated repositories)
   return formatted_values # Return the formatted list

def write_to_csv(header, data, filename):
   """
   Write data to a CSV file with a given header.

   :param header: list of column names for the CSV file
   :param data: list of tuples or lists to write as rows in the CSV file
   :param filename: name of the CSV file to save the data
   :return: None
   """

   with open(filename, mode="w", newline="", encoding="utf-8") as csvfile: # Open the CSV file for writing
      writer = csv.writer(csvfile) # Create a CSV writer
      writer.writerow(header) # Write the header
      writer.writerows(data) # Write the rows of data

def calculate_percentile_intervals(data, percentiles):
   """
   Calculate the intervals between specified percentiles for a list of numerical values.

   :param data: List of numerical values
   :param percentiles: List of percentiles to calculate (0-100)
   :return: List of tuples containing percentile ranges (percentile_start, percentile_end, interval_start, interval_end)
   """

   sorted_data = np.sort(data) # Sort the data
   percentile_values = [round(np.percentile(sorted_data, p), 2) for p in percentiles] # Calculate and round the percentile values
   intervals = [] # List to store the calculated intervals

   for i in range(1, len(percentile_values)): # Iterate over the percentiles to calculate the intervals
      intervals.append((percentiles[i-1], percentiles[i], percentile_values[i-1], percentile_values[i])) # Append the interval to the list

   return intervals # Return the calculated intervals

def create_csv_files(repositories):
   """"
   Create a CSV files containing the repositories data.

   :param repositories: list of repositories (dicts)
   return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Creating CSV files and plots for the repositories...{Style.RESET_ALL}")

   # Topics Occurrences CSV
   topics = sort_values_by_occurrences(collect_field_values_from_list(repositories, "topics")) # Collect and sort the topics from the repositories
   write_to_csv(["Topic", "Occurrences Count", "Occurrences Location"], topics, FULL_REPOSITORIES_CSV_FILEPATH.replace("FIELD_NAME", "topics_occurrences")) # Write the topics to a CSV file
 
   # Code Churn Occurrences CSV
   code_churns = sort_values_by_occurrences(collect_field_values_from_list(repositories, "avg_code_churn")) # Collect and sort the code churns from the repositories
   write_to_csv(["Code Churn", "Occurrences Count", "Occurrences Location"], code_churns, FULL_REPOSITORIES_CSV_FILEPATH.replace("FIELD_NAME", "code_churn_occurrences")) # Write the code churns to a CSV file

   # Number of Modified Files Occurrences CSV
   avg_modified_files = sort_values_by_occurrences(collect_field_values_from_list(repositories, "avg_modified_files")) # Collect and sort the average modified files from the repositories
   write_to_csv(["Average Modified Files", "Occurrences Count", "Occurrences Location"], avg_modified_files, FULL_REPOSITORIES_CSV_FILEPATH.replace("FIELD_NAME", "avg_modified_files_occurrences")) # Write the average modified files to a CSV file

   # Number of Modified Files Percentile Intervals CSV
   modified_files_values = [int(avg_modified_file) for avg_modified_file, _, _ in avg_modified_files] # Extract the average modified files values for percentile calculations
   percentile_intervals = calculate_percentile_intervals(modified_files_values, [5, 10, 25, 50, 75, 90, 95, 99]) # Calculate the percentile intervals
   write_to_csv(["Percentile Start", "Percentile End", "Interval Start", "Interval End"], percentile_intervals, FULL_REPOSITORIES_CSV_FILEPATH.replace("FIELD_NAME", "avg_modified_files_percentile_intervals")) # Write the percentile intervals to a CSV file

   # Code Churn Percentile Intervals CSV
   churn_values = [float(code_churn) for code_churn, _, _ in code_churns] # Extract the code churn values for percentile calculations
   percentile_intervals = calculate_percentile_intervals(churn_values, [5, 10, 25, 50, 75, 90, 95, 99]) # Calculate the percentile intervals
   write_to_csv(["Percentile Start", "Percentile End", "Interval Start", "Interval End"], percentile_intervals, FULL_REPOSITORIES_CSV_FILEPATH.replace("FIELD_NAME", "code_churn_percentile_intervals")) # Write the percentile intervals to a CSV file

def calculate_percentiles(data, percentiles):
   """
   Calculate specified percentiles for a list of numerical values.

   :param data: List of numerical values
   :param percentiles: List of percentiles to calculate (0-100)
   :return: Dictionary with percentile values
   """

   return {p: np.percentile(data, p) for p in percentiles} # Calculate the percentiles and return them

def filter_data_by_iqr(data, lower_percentile=25, upper_percentile=75):
   """
   Filter data by focusing on the interquartile range (IQR) between specified percentiles.

   :param data: List of numerical values
   :param lower_percentile: The lower bound percentile (default 25th)
   :param upper_percentile: The upper bound percentile (default 75th)
   :return: Filtered list of data within the specified IQR
   """

   lower_bound = np.percentile(data, lower_percentile) # Calculate the lower bound
   upper_bound = np.percentile(data, upper_percentile) # Calculate the upper bound
   
   filtered_data = [value for value in data if lower_bound <= value <= upper_bound] # Filter the data to only include values within the 25th to 75th percentile range (IQR)
   
   return filtered_data, lower_bound, upper_bound # Return the filtered data and bounds

def generate_scatter_plot(data, percentiles_dict=None, iqr_range=(25, 75)):
   """
   Generate a scatter plot to visualize code churn values within a specific interquartile range.

   :param data: List of numerical values representing code churns
   :param percentiles_dict: Optional dictionary with percentiles and values for visualization
   :param iqr_range: Tuple indicating the percentiles to focus on (default is 25th to 75th)
   :return: None
   """

   filtered_data, lower_bound, upper_bound = filter_data_by_iqr(data, *iqr_range) # Filter data by interquartile range (IQR)

   plt.figure(figsize=(10, 6)) # Create a figure and axis

   sns.scatterplot(x=range(len(filtered_data)), y=filtered_data, color="blue", alpha=0.6) # Scatter plot of filtered code churn values (focused on IQR)

   # Optionally, add lines for key percentiles (25%, 50%, etc.) if provided
   if percentiles_dict: # If the percentiles dictionary is provided
      for p, value in percentiles_dict.items(): # Iterate over the percentiles
         if iqr_range[0] <= p <= iqr_range[1]: # If the percentile is within the IQR range
            plt.axhline(y=value, color="red", linestyle="--", label=f"{p}th Percentile: {value:.2f}") # Add a horizontal line for the percentile

   plt.xlabel("Index of Code Churn Value") # X-axis is just the index (no names needed)
   plt.ylabel("Code Churn Value") # Y-axis is the code churn value
   plt.title(f"Scatter Plot of Code Churn Values (Filtered to {iqr_range[0]}th - {iqr_range[1]}th Percentiles)") # Set the title of the plot
   plt.legend(loc="upper right") # Show legend with percentile lines

   plt.tight_layout() # Adjust the layout
   plt.savefig(FULL_REPOSITORIES_PNG_SCATTER_FILEPATH.replace("FIELD_NAME", f"code_churn_iqr_{iqr_range[0]}_{iqr_range[1]}")) # Save the scatter plot to a file

def generate_code_churn_scatter_plot(repositories):
   """
   Generate a scatter plot for the code churn values of the repositories.

   :param repositories: list of repositories (dicts)
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Generating a scatter plot for the code churn values...{Style.RESET_ALL}")

   code_churns = sort_values_by_occurrences(collect_field_values_from_list(repositories, "avg_code_churn")) # Collect and sort the code churns from the repositories
   
   churn_values = [float(code_churn) for code_churn, _, _ in code_churns] # Extract churn values for percentile calculations and scatter plot

   percentiles_to_calculate = [25, 50, 75] # Percentiles to calculate for visualization
   percentiles_dict = calculate_percentiles(churn_values, percentiles_to_calculate) # Calculate the percentiles for visualization

   generate_scatter_plot(churn_values, percentiles_dict, iqr_range=(25, 75)) # Generate a scatter plot for the code churn values

def randomly_select_repositories(repositories, num_repos):
   """
   Selects a number of repositories randomly.

   :param repositories: list
   :param num_repos: int
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Selecting {BackgroundColors.CYAN}{num_repos}{BackgroundColors.GREEN} repositories randomly...{Style.RESET_ALL}")

   return random.sample(repositories, num_repos) # Return a random sample of repositories

def print_repositories_summary(total_repo_count, total_candidates, candidates):
   """
   Prints the total number of repositories and the selected repositories to the console.

   :param total_repo_count: int
   :param total_candidates: int
   :param candidates: list
   :return: None
   """

   print(f"{BackgroundColors.GREEN}Total repositories according to the criteria: {BackgroundColors.CYAN}{total_candidates}{BackgroundColors.GREEN} out of {BackgroundColors.CYAN}{total_repo_count}{Style.RESET_ALL}\n")
   print(f"{BackgroundColors.CYAN}Selected repositories:{Style.RESET_ALL}")
   for i, repo in enumerate(candidates, start=1): # Iterate over the selected repositories
      print(f"{BackgroundColors.CYAN}{i}. {repo['author']}/{repo['name']}{Style.RESET_ALL}: {BackgroundColors.GREEN}{repo['url']} - {repo['description']} "
            f"{BackgroundColors.CYAN}(⭐ {repo['stars']}{BackgroundColors.GREEN}, {BackgroundColors.CYAN}📝 {repo['commits']} commits{BackgroundColors.GREEN}){Style.RESET_ALL}")

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

atexit.register(play_sound) # Register the function to play a sound when the program finishes

def main():
   """
   Main function.

   :return: None
   """

   start_time = datetime.now() # Get the start time

   print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Repositories Picker{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the welcome message
   print(f"{BackgroundColors.GREEN}This script will generate the list of GitHub Repositories based on the provided criteria.{Style.RESET_ALL}", end="\n\n") # Output the script description

   if path_contains_whitespaces(): # Verify if the path constants contains whitespaces
      return # Return if the path constants contains whitespaces

   update_sound_file_path() # Update the sound file path

   if not verify_git(): # Verify if Git is installed
      return # Return if Git is not installed

   if not setup_submodule(f"{START_PATH[:START_PATH.rfind('/')]}/"): # Setup the submodule
      return # Return if the submodule setup fails

   token = get_env_token() # Verify the .env file and get the token

   repositories = fetch_repositories(token) # Fetch the repositories
   total_repo_count = len(repositories) # Get the total number of repositories
   filtered_repositories = filter_repositories(repositories, token) # Filter the repositories

   if filtered_repositories: # If there are repositories after filtering and sorting
      for repository_attribute in REPOSITORIES_SORTING_ATTRIBUTES: # Iterate over the REPOSITORIES_SORTING_ATTRIBUTES
         sorted_repositories = sorted(filtered_repositories, key=lambda x: x[repository_attribute], reverse=True) # Sort the repositories by the repository_attribute value
         save_to_json(sorted_repositories, FULL_REPOSITORIES_LIST_JSON_FILEPATH.replace("SORTING_ATTRIBUTE", repository_attribute)) if RUN_FUNCTIONS["Save to JSON"] else None # Save the filtered and sorted repositories to a JSON file
         save_to_pdf(sorted_repositories, repository_attribute, FULL_REPOSITORIES_LIST_PDF_FILEPATH.replace("SORTING_ATTRIBUTE", repository_attribute)) if RUN_FUNCTIONS["Save to PDF"] else None # Save the filtered and sorted repositories to a PDF file

      create_histograms(sorted_repositories) if RUN_FUNCTIONS["Histograms"] else None # Create histograms for the HISTORY_REPOSITORY_FIELDS in the repositories
      create_csv_files(sorted_repositories) if RUN_FUNCTIONS["CSV Files"] else None # Create CSV files for the code churn and topics occurrences in the repositories

      generate_code_churn_scatter_plot(sorted_repositories) if RUN_FUNCTIONS["Scatter Plot"] else None # Generate a scatter plot for the code churn values in the repositories

      candidates = randomly_select_repositories(sorted_repositories, CANDIDATES) if RUN_FUNCTIONS["Show Candidate Repositories"] else None # Select a number of repositories randomly
      candidates = sorted(candidates, key=lambda x: x["commits"], reverse=True) if RUN_FUNCTIONS["Show Candidate Repositories"] else None # Sort the candidates by the number of commits
      print_repositories_summary(total_repo_count, len(sorted_repositories), candidates) if RUN_FUNCTIONS["Show Candidate Repositories"] else None # Print the summary of the repositories
   else: # If there are no repositories after filtering and sorting
      print(f"{BackgroundColors.RED}No repositories found.{Style.RESET_ALL}")

   end_time = datetime.now() # Get the end time
   output_time(f"\n{BackgroundColors.GREEN}Total execution time: ", (end_time - start_time).total_seconds()) # Output the total execution time

   print(f"\n{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """

   main() # Call the main function
