import atexit # For playing a sound when the program finishes
import os # For running a command in the terminal
import platform # For getting the operating system name
import sys # For exiting the program
from colorama import Style # For coloring the terminal
import requests # For making HTTP requests
import json # For creating JSON output
import random # For selecting random items
from datetime import datetime, timedelta # For date manipulation
from dotenv import load_dotenv # For loading environment variables from .env file

# Macros:
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
SOUND_FILE = "./.assets/Sounds/NotificationSound.wav" # The path to the sound file

# .Env Constants:
ENV_PATH = "../.env" # The path to the .env file
ENV_VARIABLE = "GITHUB_TOKEN" # The environment variable to load

# Execution Constants:
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function
CANDIDATES = 3 # The number of repositories to select
EXCLUDE_REPOSITORIES_KEYWORDS = ["awesome", "interview", "question"] # Keywords to ignore in repository names
MINIMUM_STARS = 50 # The minimum number of stars a repository must have

# File Path Constants:
OUTPUT_DIRECTORY = "./Repositories/" # The path to the output directory
OUTPUT_FILE = f"{OUTPUT_DIRECTORY}repositories.json" # The path to the output file

def play_sound():
   """
   Plays a sound when the program finishes.

   :return: None
   """

   if os.path.exists(SOUND_FILE):
      if platform.system() in SOUND_COMMANDS: # If the platform.system() is in the SOUND_COMMANDS dictionary
         os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
      else: # If the platform.system() is not in the SOUND_COMMANDS dictionary
         print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
   else: # If the sound file does not exist
      print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

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

def main():
   """
   Main function.

   :return: None
   """

   print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Repositories Selector{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the welcome message

   token = verify_env_file() # Verify the .env file and get the token

   repositories = fetch_repositories(token) # Fetch the repositories

   filtered_repositories = filter_repositories(repositories) # Filter the repositories

   if filtered_repositories: # If there are repositories after filtering
      save_to_json(filtered_repositories) # Save the filtered repositories to a JSON file

      # Randomly select an specific number of repositories
      candidates = select_repositories(filtered_repositories, CANDIDATES)

      print(f"{BackgroundColors.GREEN}Selected repositories:{Style.RESET_ALL}")
      for repo in candidates: # Iterate over the selected repositories
         print(f"{BackgroundColors.CYAN}{repo['name'].title()}{Style.RESET_ALL}: {BackgroundColors.GREEN}{repo['url']} - {repo['description']} (⭐ {repo['stars']}){Style.RESET_ALL}")
   else:
      print(f"{BackgroundColors.RED}No repositories found.{Style.RESET_ALL}")

   print(f"\n{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """

   main() # Call the main function
