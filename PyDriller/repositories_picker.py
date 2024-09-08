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
from fpdf import FPDF # For creating PDFs

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
EXCLUDE_REPOSITORIES_KEYWORDS = [] # Keywords to ignore in repository names
MINIMUM_STARS = 50 # The minimum number of stars a repository must have

# File Path Constants:
OUTPUT_DIRECTORY = "./repositories/" # The path to the output directory
OUTPUT_FILE_JSON = f"{OUTPUT_DIRECTORY}repositories.json" # The path to the JSON output file
OUTPUT_FILE_PDF = f"{OUTPUT_DIRECTORY}repositories.pdf" # The path to the PDF output file

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

def build_url(query):
   """
   Builds the GitHub API request URL.
   :param query: str
   :return: str
   """

   return f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page=100"

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
   url = build_url(query) # Build the request URL

   repositories = fetch_all_pages(url, headers) # Fetch repositories from all pages
   return repositories # Return the list of repositories

def filter_repositories(repositories, ignore_keywords=EXCLUDE_REPOSITORIES_KEYWORDS):
   """
   Filters the list of repositories based on the update date and ignore keywords.

   :param repositories: list
   :param ignore_keywords: list
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Filtering the repositories...{Style.RESET_ALL}")

   filtered_repositories = [] # The list of filtered repositories
   six_months_ago = datetime.now() - timedelta(days=180) # The date six months ago

   for repo in repositories: # Iterate over the repositories
      updated_date = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ") # Get the updated date of the repository
      if updated_date > six_months_ago and repo["stargazers_count"] >= MINIMUM_STARS and not any(keyword.lower() in repo["name"].lower() or keyword.lower() in repo["description"].lower() for keyword in ignore_keywords):
         filtered_repositories.append({ # Append the repository to the list
            "name": repo["name"], # Get the name of the repository
            "url": repo["html_url"], # Get the URL of the repository
            "description": repo["description"], # Get the description of the repository
            "stars": repo["stargazers_count"], # Get the number of stars of the repository
            "updated_at": repo["updated_at"] # Get the updated date of the repository
         })

   return filtered_repositories # Return the filtered list of repositories

def capitalize_repositories(repositories):
   """
   Capitalizes the first letter of each word in the repository name.

   :param repositories: list
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Capitalizing the repository names...{Style.RESET_ALL}")

   for repo in repositories: # Iterate over the repositories
      repo["name"] = repo["name"].title() # Capitalize the first letter of each word in the repository name

   return repositories # Return the list of repositories

def save_to_json(data, filename=OUTPUT_FILE_JSON):
   """
   Saves the data to a JSON file.

   :param data: dict
   :param filename: str
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Saving the data to {BackgroundColors.CYAN}{filename}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

   create_directory(OUTPUT_DIRECTORY, "output") # Create the output directory

   with open(filename, "w") as json_file: # Open the JSON file
      json.dump(data, json_file, indent=3) # Dump the data to the JSON file

def add_pdf_header(pdf, num_candidates):
   """
   Adds a header to the PDF.
   :param pdf: FPDF object
   :param num_candidates: int, number of repositories
   :return: None
   """

   pdf.set_font("Helvetica", size=12) # Set the font to Helvetica with size 12

   # Header
   pdf.set_font("Helvetica", "B", 12) # Set font to bold
   pdf.set_text_color(0, 102, 204) # Set font color to a sky blue shade

   # Format the current date
   current_date = datetime.now().strftime("%d %B %Y") # Format: 01 January 2022
   current_time = datetime.now().strftime("%Hh %Mm %Ss") # Format: 12h 34m 56s

   header_text = (
      f"Repositories List\n" # Title
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
   pdf.cell(135, 10, "Name (Hyperlink)", border=1, fill=True) # Name column
   pdf.cell(20, 10, "Stars", border=1, fill=True) # Stars column
   pdf.cell(35, 10, "Last Update", border=1, fill=True) # Last Update column
   pdf.ln() # Line break

def format_last_update_date(last_update):
   """
   Formats the last update date of the repository.
   :param last_update: str, the ISO date string from the repository data
   :return: str, formatted date or 'Unknown' if parsing fails
   """

   try:
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

   pdf.set_font("Helvetica", size=10)

   for repo in data:
      # Handle content in English
      name = repo.get("name", "") # Get the name of the repository
      url = repo.get("url", "") # Get the URL of the repository
      stars = str(repo.get("stars", "")) # Get the number of stars

      # Handle last_update
      last_update = repo.get("updated_at", "")
      last_update = format_last_update_date(last_update) # Parse and format last update date

      # Add the encoded content to the PDF
      pdf.set_x(10) # Set the start x position

      # Name (make it a hyperlink)
      pdf.set_text_color(0, 0, 255) # Set color to blue for hyperlinks
      pdf.cell(135, 10, name, border=1, link=url) # Name should be clickable
      pdf.set_text_color(0, 0, 0) # Reset text color to black

      pdf.cell(20, 10, stars, border=1) # Stars
      pdf.cell(35, 10, last_update, border=1) # Last Update
      pdf.ln() # Line break

def save_to_pdf(data, filename=OUTPUT_FILE_PDF):
   """
   Saves the data to a PDF file.
   :param data: list of dict
   :param filename: str
   :return: None
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Saving the data to {BackgroundColors.CYAN}{filename}{BackgroundColors.GREEN}...{Style.RESET_ALL}")

   pdf = FPDF() # Create a PDF object
   pdf.add_page() # Add a page to the PDF

   add_pdf_header(pdf, len(data)) # Add header section
   add_pdf_column_headers(pdf) # Add column headers
   add_pdf_data_rows(pdf, data) # Add data rows

   pdf.output(filename) # Save the PDF file

def randomly_select_repositories(repositories, num_repos):
   """
   Selects a number of repositories randomly.

   :param repositories: list
   :param num_repos: int
   :return: list
   """

   verbose_output(true_string=f"{BackgroundColors.GREEN}Selecting {BackgroundColors.CYAN}{num_repos}{BackgroundColors.GREEN} repositories randomly...{Style.RESET_ALL}")

   return random.sample(repositories, num_repos)

def main():
   """
   Main function.

   :return: None
   """

   print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Repositories Picker{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the welcome message

   token = verify_env_file() # Verify the .env file and get the token

   repositories = fetch_repositories(token) # Fetch the repositories

   filtered_repositories = filter_repositories(repositories) # Filter the repositories

   capitalized_repositories = capitalize_repositories(filtered_repositories)

   sorted_by_stars = sorted(capitalized_repositories, key=lambda x: x["stars"], reverse=True) # Sort the repositories by stars

   if sorted_by_stars: # If there are repositories after filtering and sorting
      save_to_json(sorted_by_stars) # Save the filtered and sorted repositories to a JSON file
      save_to_pdf(sorted_by_stars) # Save the filtered and sorted repositories to a PDF file

      # Randomly select an specific number of repositories
      candidates = randomly_select_repositories(sorted_by_stars, CANDIDATES)

      print(f"{BackgroundColors.CYAN}Selected repositories:{Style.RESET_ALL}")
      for i, repo in enumerate(candidates, start=1): # Iterate over the selected repositories with index starting from 1
         print(f"{BackgroundColors.CYAN}{i}. {repo['name'].title()}{Style.RESET_ALL}: {BackgroundColors.GREEN}{repo['url']} - {repo['description']} (⭐ {repo['stars']}){Style.RESET_ALL}")

   else:
      print(f"{BackgroundColors.RED}No repositories found.{Style.RESET_ALL}")

   print(f"\n{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
   """
   This is the standard boilerplate that calls the main() function.

   :return: None
   """

   main() # Call the main function
