import atexit # For playing a sound when the program finishes
import concurrent.futures # For running tasks concurrently
import json # For creating JSON output
import matplotlib.pyplot as plt # For creating plots, such as histograms
import numpy as np # For numerical operations
import os # For running a command in the terminal
import platform # For getting the operating system name
import random # For selecting random items
import requests # For making HTTP requests
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import sys # For exiting the program
from colorama import Style # For coloring the terminal
from datetime import datetime, timedelta # For date manipulation
from dotenv import load_dotenv # For loading environment variables from .env file
from fpdf import FPDF # For creating PDFs

# Default values that can be changed:
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function
DATETIME_FILTER = None # The datetime filter for the repositories
HISTOGRAM_REPOSITORY_FIELDS = ["commits", "stars"] # The repository fields to create histograms for
CANDIDATES = 3 # The number of repositories to select
EXCLUDE_REPOSITORIES_KEYWORDS = [] # Keywords to ignore in repository names
MINIMUM_COMMITS = 0 # The minimum number of commits a repository must have
MINIMUM_STARS = 50 # The minimum number of stars a repository must have
PROCESS_JSON_REPOSITORIES = True # Process the JSON repositories. If set to True, it will process the JSON repositories, otherwise it will pick the ones defined in the DEFAULT_REPOSITORIES dictionary.
REPOSITORIES_SORTING_ATTRIBUTES = ["commits", "stars"] # The attribute to sort the repositories by

DEFAULT_REPOSITORIES = { # The default repositories to be analyzed in the format: "repository_name": "repository_url"
   "CorfuDB": "https://github.com/CorfuDB/CorfuDB",
   "kafka": "https://github.com/apache/kafka",
   "moleculer-java": "https://github.com/moleculer-java/moleculer-java",
   "scalecube-services": "https://github.com/scalecube/scalecube-services",
   "zookeeper": "https://github.com/apache/zookeeper"
}

# .Env Constants:
ENV_PATH = "../.env" # The path to the .env file
ENV_VARIABLE = "GITHUB_TOKEN" # The environment variable to load

# File Extensions Constants:
PDF_FILE_EXTENSION = ".pdf" # The PDF file extension
PNG_FILE_EXTENSION = ".png" # The PNG file extension
JSON_FILE_EXTENSION = ".json" # The JSON file extension

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# Default paths:
START_PATH = os.getcwd() # Get the current working directory

# Relative File Path Constants:
RELATIVE_REPOSITORIES_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories
RELATIVE_REPOSITORIES_HISTOGRAM_FILEPATH = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/histogram_DATA_TYPE{PNG_FILE_EXTENSION}" # The relative path of the directory that contains the histograms
RELATIVE_REPOSITORIES_LIST_FILEPATH_PDF = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/repositories_sorted_by_SORTING_ATTRIBUTE{PDF_FILE_EXTENSION}" # The relative path to the repositories PDF file
RELATIVE_REPOSITORIES_LIST_FILEPATH_JSON = f"{RELATIVE_REPOSITORIES_DIRECTORY_PATH}/repositories_sorted_by_SORTING_ATTRIBUTE{JSON_FILE_EXTENSION}" # The relative path to the repositories JSON file

# Full File Path Constants:
FULL_REPOSITORIES_DIRECTORY_PATH = f"{START_PATH}{RELATIVE_REPOSITORIES_DIRECTORY_PATH}" # The full path of the directory that contains the repositories
FULL_REPOSITORIES_HISTOGRAM_FILEPATH = f"{START_PATH}{RELATIVE_REPOSITORIES_HISTOGRAM_FILEPATH}" # The full path of the directory that contains the histograms
FULL_REPOSITORIES_LIST_FILEPATH_PDF = f"{START_PATH}{RELATIVE_REPOSITORIES_LIST_FILEPATH_PDF}" # The full path to the repositories PDF file
FULL_REPOSITORIES_LIST_FILEPATH_JSON = f"{START_PATH}{RELATIVE_REPOSITORIES_LIST_FILEPATH_JSON}" # The full path to the repositories JSON file

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

def play_sound():
   """
   Plays a sound when the program finishes.

   :return: None
   """

   if os.path.exists(SOUND_FILE_PATH):
      if platform.system() in SOUND_COMMANDS: # If the platform.system() is in the SOUND_COMMANDS dictionary
         os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE_PATH}")
      else: # If the platform.system() is not in the SOUND_COMMANDS dictionary
         print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
   else: # If the sound file does not exist
      print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE_PATH}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

atexit.register(play_sound) # Register the function to play a sound when the program finishes

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
   
   # Verify if the PATH constant contains whitespaces
   if " " in START_PATH: # If the PATH constant contains whitespaces
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
   if START_PATH.endswith("PyDriller"):
      prefix = "../" # Go up one directory
   elif START_PATH.endswith("Scripts"):
      prefix = "../../" # Go up two directories
   else: # The current directory is not "PyDriller" or "Scripts", so it must be the root dir ("Worked-Example-Miner")
      prefix = "./" # Stay in the same directory

   # Update the SOUND_FILE_PATH constant
   SOUND_FILE_PATH = f"{prefix}{SOUND_FILE_PATH}"

   verbose_output(true_string=f"{BackgroundColors.GREEN}Updated the {BackgroundColors.CYAN}SOUND_FILE{BackgroundColors.GREEN} path to {BackgroundColors.CYAN}{SOUND_FILE_PATH}{Style.RESET_ALL}")

   return SOUND_FILE_PATH # Return the updated sound file path

def verify_json_file(file_path):
   """
   Verify if the JSON file exists and is not empty.

   :param file_path: The path to the JSON file.
   :return: True if the JSON file exists and is not empty, False otherwise.
   """

   if not os.path.exists(file_path):
      print(f"{BackgroundColors.RED}The repositories JSON file does not exist.{Style.RESET_ALL}")
      return False # Return False if the JSON file does not exist
   if os.path.getsize(file_path) == 0:
      print(f"{BackgroundColors.RED}The repositories JSON file is empty.{Style.RESET_ALL}")
      return False # Return False if the JSON file is empty
   return True # Return True if the JSON file exists and is not empty

def load_repositories_from_json(file_path):
   """
   Load repositories from a JSON file.

   :param file_path: The path to the JSON file.
   :return: A dictionary containing the repositories if the JSON file is valid, None otherwise.   
   """

   try:
      with open(file_path, "r", encoding="utf-8") as json_file: # Open the JSON file
         repositories_list = json.load(json_file) # Load the JSON file

      # Ensure the data is a list and contains repositories
      if isinstance(repositories_list, list) and repositories_list:
         return {repo["name"]: repo["url"] for repo in repositories_list} # Return the dictionary containing the repositories
      else:
         print(f"{BackgroundColors.RED}The repositories JSON file is not in the correct format.{Style.RESET_ALL}")
         return None # Return None if the JSON file is not in the correct format
   except (json.JSONDecodeError, KeyError) as e:
      verbose_output(true_string=f"{BackgroundColors.RED}Error parsing the repositories JSON file: {e}{Style.RESET_ALL}", is_error=True)
      return None # Return None if there is an error parsing the JSON file

def update_repositories_dictionary():
   """
   Update the repositories list in the DEFAULT_REPOSITORIES dictionary.
   
   :return: True if the DEFAULT_REPOSITORIES dictionary was successfully updated with values from the JSON file, False otherwise.
   """
   
   verbose_output(true_string=f"{BackgroundColors.GREEN}Updating the repositories list file with the DEFAULT_REPOSITORIES dictionary...{Style.RESET_ALL}")

   global DEFAULT_REPOSITORIES # Use the global DEFAULT_REPOSITORIES variable

   # Iterate through all REPOSITORIES_SORTING_ATTRIBUTES to find a valid file
   for sorting_attribute in REPOSITORIES_SORTING_ATTRIBUTES:
      filename = FULL_REPOSITORIES_LIST_FILEPATH_JSON.replace("SORTING_ATTRIBUTE", sorting_attribute) # Get the filename for the current attribute
      
      # Verify if the JSON file exists
      if not os.path.exists(filename): # If file doesn't exist, skip to the next attribute
         verbose_output(true_string=f"{BackgroundColors.YELLOW}File {filename} not found, checking next...{Style.RESET_ALL}")
         continue
      
      # Validate the JSON file
      if not verify_json_file(filename): # If the JSON file is not valid, skip to the next
         verbose_output(true_string=f"{BackgroundColors.RED}Invalid JSON file: {filename}, checking next...{Style.RESET_ALL}")
         continue
      
      # Load repositories from the valid JSON file
      json_repositories = load_repositories_from_json(filename)
      if not json_repositories: # If loading the JSON file fails, skip to the next
         verbose_output(true_string=f"{BackgroundColors.RED}Failed to load JSON data from {filename}, checking next...{Style.RESET_ALL}")
         continue

      # Update DEFAULT_REPOSITORIES and return True if successful
      DEFAULT_REPOSITORIES = json_repositories
      verbose_output(true_string=f"{BackgroundColors.GREEN}The {BackgroundColors.CLEAR_TERMINAL}DEFAULT_REPOSITORIES{BackgroundColors.GREEN} dictionary was successfully updated from {BackgroundColors.CYAN}{filename}{BackgroundColors.GREEN}.{Style.RESET_ALL}")
      return True # Return True if the DEFAULT_REPOSITORIES dictionary was successfully updated with values from the JSON file
   
   # If no valid files were found
   print(f"{BackgroundColors.RED}No valid JSON files found for any of the sorting attributes.{Style.RESET_ALL}")
   return False # Return False if no valid JSON files were found

def verify_repositories_execution_constants():
   """
   Verify the constants used in the execution of the repositories.
   It will process the JSON repositories, if the PROCESS_JSON_REPOSITORIES constant is set to True or if the DEFAULT_REPOSITORIES dictionary is empty.
   
   :return: None
   """

   # Verify if PROCESS_REPOSITORIES_LIST is set to True or if the DEFAULT_REPOSITORIES dictionary is empty
   if PROCESS_JSON_REPOSITORIES or not DEFAULT_REPOSITORIES:
      if not update_repositories_dictionary(): # Update the repositories list
         print(f"{BackgroundColors.RED}The repositories list could not be updated. Please execute the {BackgroundColors.CYAN}repositories_picker.py{BackgroundColors.RED} script with the {BackgroundColors.CYAN}PROCESS_JSON_REPOSITORIES{BackgroundColors.RED} set to {BackgroundColors.CYAN}False{BackgroundColors.RED} or manually fill the {BackgroundColors.CYAN}DEFAULT_REPOSITORIES{BackgroundColors.RED} dictionary.{Style.RESET_ALL}")
         exit() # Exit the program if the repositories list could not be updated

def verify_git():
   """
   Verify if Git is installed.

   :return: True if Git is installed, False otherwise.
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying if Git is installed...{Style.RESET_ALL}")

   try:
      subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
   except subprocess.CalledProcessError as e:
      print(f"{BackgroundColors.RED}An error occurred while verifying if Git is installed: {BackgroundColors.YELLOW}{e}{BackgroundColors.RED}. Please install Git!{Style.RESET_ALL}")
      return False # Return False if Git is not installed
   return True # Return True if Git is installed

def verify_env_file(env_path=ENV_PATH, key=ENV_VARIABLE):
   """
   Verify if the .env file exists and if the desired key is present.

   :param env_path: Path to the .env file.
   :param key: The key to get in the .env file.
   :return: The value of the key if it exists.
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Verifying the .env file...{Style.RESET_ALL}")

   # Verify if the .env file exists
   if not os.path.exists(env_path):
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

def calculate_average_code_churn(repo_path, total_commits):
   """
   Calculates the average code churn for all commits in a repository.

   :param repo_path: str
   :param total_commits: int
   :return: float representing the average code churn (lines added and removed).
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating average code churn for the {BackgroundColors.CYAN}{repo_path.split("/")[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")

   try:
      # Run the git command to get the numstat output
      result = subprocess.run(
         ["git", "-C", repo_path, "log", "--pretty=tformat:", "--numstat"], # Get the numstat output
         capture_output=True, # Capture the output
         text=True, # Get the output as text
         check=True # Check for errors
      )
      
      lines = result.stdout.strip().splitlines() # Split the output into lines

      code_churn_metrics = (0, 0, 0) # Initialize the code churn metrics (code churn, total added, total removed)

      for line in lines: # Process each line
         if line: # If the line is not empty
            parts = line.split() # Split the line into parts
            if len(parts) == 3: # If there are 3 parts
               # Use try-except to handle conversion errors
               try:
                  added = int(parts[0]) if parts[0] != "-" else 0 # Get the number of lines added
                  removed = int(parts[1]) if parts[1] != "-" else 0 # Get the number of lines removed
                  total_added = code_churn_metrics[1] + added # Update total added
                  total_removed = code_churn_metrics[2] + removed # Update total removed
                  code_churn = added - removed # Calculate code churn
                  code_churn_metrics = (code_churn_metrics[0] + code_churn, total_added, total_removed) # Update the code churn metrics
               except ValueError as e:
                  print(f"{BackgroundColors.RED}Error while parsing numstat output: {e}{Style.RESET_ALL}")

      avg_code_churn = code_churn_metrics[0] / total_commits if total_commits > 0 else 0 # Calculate average code churn
      return avg_code_churn # Return the average code churn

   except subprocess.CalledProcessError as e:
      print(f"{BackgroundColors.RED}Error while calculating average code churn: {e}{Style.RESET_ALL}")
      return 0 # Return 0 or handle the error as needed

def process_repository(repo, date_filter=None, ignore_keywords=None):
   """
   Processes a single repository, filtering by date, keywords, and ensuring a unique name.

   :param repo: dict
   :param date_filter: datetime to filter the repositories
   :param ignore_keywords: list
   :return: dict or None
   """

   updated_date = parse_repo_updated_date(repo) # Get the last update date of the repository

   # Validate the repository based on the update date, star count, and keywords
   if is_repository_valid(repo, updated_date, date_filter, ignore_keywords):
      setup_repository(repo["name"], repo["html_url"]) # Setup the repository: Clone or update it so we can calculate the code churn and commit count
      repo_path = f"{FULL_REPOSITORIES_DIRECTORY_PATH}/{repo['name']}/" # The path to the repository directory
      commits_count = count_commits(repo_path) # Count the number of commits in the repository
      if commits_count > MINIMUM_COMMITS: # If the number of commits is greater than the minimum
         return {
            "name": repo["name"].encode("utf-8").decode("utf-8"),
            "author": extract_author_name(repo).encode("utf-8").decode("utf-8"),
            "url": repo["html_url"],
            "description": repo["description"].encode("utf-8").decode("utf-8"),
            "topics": ", ".join(repo["topics"]),
            "commits": commits_count,
            "stars": repo["stargazers_count"],
            "forks counter": repo["forks_count"],
            "open issues counter": repo["open_issues_count"],
            "avg_code_churn": int(calculate_average_code_churn(repo_path, commits_count)),
            "avg_modified_files_count": "To be calculated",
            "updated_at": repo["updated_at"],
            # "pull_requests": repo.get("pulls_count", 0), # Apparently this endpoint aint working
            "license": repo["license"]["name"] if repo.get("license") else "No license specified",
         }

   return None # Return None if the repository is not valid

def update_repository(repository_directory_path):
   """
   Update the repository using "git pull".

   :param repository_directory_path: The path to the repository directory
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Updating the {BackgroundColors.CYAN}{repository_directory_path.split('/')[-1]}{BackgroundColors.GREEN} repository...{Style.RESET_ALL}")
   
   os.chdir(repository_directory_path) # Change the current working directory to the repository directory
   
   # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + "/" + repository_name
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
   thread.wait() # Wait for the thread to finish

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

def count_commits(repo_path):
   """
   Counts the number of commits in a repository using the git command.

   :param repo_path: str
   :return: int
   """

   try:
      # Run the git command to count commits
      result = subprocess.run(
         ["git", "-C", repo_path, "rev-list", "--count", "HEAD"],
         capture_output=True,
         text=True,
         check=True
      )
      # Return the commit count as an integer
      return int(result.stdout.strip())
   except subprocess.CalledProcessError as e:
      print(f"Error while counting commits: {e}")
      return 0 # Return 0 or handle the error as needed

def process_repository_task(repo, datetime_filter, ignore_keywords):
   """
   Processes and filters a single repository.

   :param repo: dict
   :param datetime_filter: datetime to filter the repositories
   :param ignore_keywords: list
   :return: dict or None
   """

   filtered_repo = process_repository(repo, datetime_filter, ignore_keywords) # Process the repository
   return filtered_repo if filtered_repo else None # Return the repository if it is valid, otherwise return None

def filter_repositories(repositories, ignore_keywords=EXCLUDE_REPOSITORIES_KEYWORDS):
   """
   Filters the list of repositories based on the update date, ignore keywords, and ensures unique names.
   This function uses concurrent processing to speed up the filtering process based on the number of available CPU cores.

   :param repositories: list
   :param ignore_keywords: list
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Applying repository filtering criteria...{Style.RESET_ALL}")

   usable_threads, max_threads = get_adjusted_number_of_threads(get_threads()) # Get the adjusted number of threads to use
   
   verbose_output(true_string=f"{BackgroundColors.GREEN}Using {BackgroundColors.CYAN}{usable_threads}{BackgroundColors.GREEN} of {BackgroundColors.CYAN}{max_threads}{BackgroundColors.GREEN} threads available...{Style.RESET_ALL}")

   datetime_filter = get_datetime_filter() # Get the datetime filter for the repositories

   filtered_repositories = [] # The list of filtered repositories. Each repository is a dict

   with concurrent.futures.ThreadPoolExecutor(max_workers=usable_threads) as executor:
      # Submit the process_repository_task function to the executor for each repository
      futures = [executor.submit(process_repository_task, repo, datetime_filter, ignore_keywords) for repo in repositories]

      for future in concurrent.futures.as_completed(futures): # Iterate over the futures as they are completed
         try:
            result = future.result() # Raises exception if any occurred during execution
            if result: # If the result is not None
               filtered_repositories.append(result) # Append the repository to the list
         except Exception as exc:
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

def save_to_json(data, filename=FULL_REPOSITORIES_LIST_FILEPATH_JSON):
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
   except ValueError:
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
      # Handle content in English
      name = repo.get("name", "") # Get the name of the repository
      author = repo.get("author", "") # Get the author of the repository
      url = repo.get("url", "") # Get the URL of the repository
      commits = str(repo.get("commits", "")) # Get the number of commits
      stars = str(repo.get("stars", "")) # Get the number of stars

      # Handle last_update
      last_update = repo.get("updated_at", "") # Get the last update date of the repository
      last_update = format_last_update_date(last_update) # Parse and format last update date

      # Add the encoded content to the PDF
      pdf.set_x(10) # Set the start x position

      # Name (make it a hyperlink)
      pdf.set_text_color(0, 0, 255) # Set color to blue for hyperlinks
      pdf.cell(120, 10, f"{author}/{name}", border=1, link=url) # Name (Hyperlink) is the "author/repository_name" of the repository
      pdf.set_text_color(0, 0, 0) # Reset text color to black
      pdf.cell(20, 10, commits, border=1) # Commits
      pdf.cell(15, 10, stars, border=1) # Stars
      pdf.cell(35, 10, last_update, border=1) # Last Update
      pdf.ln() # Line break

def save_to_pdf(data, sorting_attribute, filename=FULL_REPOSITORIES_LIST_FILEPATH_PDF):
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
   commits_histogram_filepath = FULL_REPOSITORIES_HISTOGRAM_FILEPATH.replace("DATA_TYPE", repository_field) # Replace "DATA_TYPE" with the repository field in the histogram file path
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
   for i, repo in enumerate(candidates, start=1):
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

def main():
   """
   Main function.

   :return: None
   """

   start_time = datetime.now() # Get the start time

   print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Repositories Picker{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the welcome message

   if path_contains_whitespaces(): # Verify if the path constants contains whitespaces
      return # Return if the path constants contains whitespaces

   update_sound_file_path() # Update the sound file path

   verify_repositories_execution_constants() # Verify the DEFAULT_REPOSITORIES constant

   if not verify_git(): # Verify if Git is installed
      return # Return if Git is not installed

   token = verify_env_file() # Verify the .env file and get the token

   repositories = fetch_repositories(token) # Fetch the repositories
   total_repo_count = len(repositories) # Get the total number of repositories
   filtered_repositories = filter_repositories(repositories) # Filter the repositories

   if filtered_repositories: # If there are repositories after filtering and sorting
      for repository_attribute in REPOSITORIES_SORTING_ATTRIBUTES: # Iterate over the REPOSITORIES_SORTING_ATTRIBUTES
         sorted_repositories = sorted(filtered_repositories, key=lambda x: x[repository_attribute], reverse=True) # Sort the repositories by the repository_attribute value
         save_to_json(sorted_repositories, FULL_REPOSITORIES_LIST_FILEPATH_JSON.replace("SORTING_ATTRIBUTE", repository_attribute)) # Save the filtered and sorted repositories to a JSON file
         save_to_pdf(sorted_repositories, repository_attribute, FULL_REPOSITORIES_LIST_FILEPATH_PDF.replace("SORTING_ATTRIBUTE", repository_attribute)) # Save the filtered and sorted repositories to a PDF file

      create_histograms(sorted_repositories) # Create histograms for the HISTORY_REPOSITORY_FIELDS in the repositories
      candidates = randomly_select_repositories(sorted_repositories, CANDIDATES) # Randomly select an specific number of repositories
      candidates = sorted(candidates, key=lambda x: x["commits"], reverse=True) # Sort the candidates by the number of commits
      print_repositories_summary(total_repo_count, len(sorted_repositories), candidates) # Print the summary of the repositories
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
