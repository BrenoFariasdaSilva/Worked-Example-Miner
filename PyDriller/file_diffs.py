import os # The OS module in Python provides functions for interacting with the operating system.
import atexit # For playing a sound when the program finishes
import platform # For getting the operating system name
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
from colorama import Style # Colorama is a Python library for printing colored text and stylizing terminal output.
from ck_metrics import backgroundColors # Import the background colors from the ck_metrics module

SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The sound commands for each operating system
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file

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

# Current working directory
cwd = os.getcwd()

# Define the default repository names and URLs
DEFAULT_REPOSITORY_NAMES = {"commons-lang":"https://github.com/apache/commons-lang", "jabref": "https://github.com/JabRef/jabref", "kafka": "https://github.com/apache/kafka", "zookeeper": "https://github.com/apache/zookeeper"}

# Generate the diffs for each repository
for repository_name, repository_url in DEFAULT_REPOSITORY_NAMES.items():
	# Get the commits generator and list for the repository
	commits_generator = (commit for commit in Repository(repository_url).traverse_commits())
	commits = list(commit for commit in Repository(repository_url).traverse_commits())

	# Validate if there are enough commits to generate a diff
	if len(commits) < 2:
		print(f"{backgroundColors.RED}There are not enough commits in the {repository_name} repository to generate a diff.{Style.RESET_ALL}")
		continue

	# Loop through the commits of the repository and generate the diffs files
	for i, commit in enumerate(tqdm(commits_generator, desc=f"{backgroundColors.GREEN}Processing {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} commits{Style.RESET_ALL}")):
		# Loop through the modified files of the commit
		for modified_file in commit.modified_files:
			file_diff = modified_file.diff # Get the diff of the modified file
			diff_file_directory = f"{cwd}/diffs/{repository_name}/{i} - {commit.hash}/" # Define the directory to save the diff file

			# Validate if the directory exists, if not, create it
			if not os.path.exists(diff_file_directory):
				os.makedirs(diff_file_directory, exist_ok=True) # Create the directory
			# Save the diff file
			with open(f"{diff_file_directory}{modified_file.filename}.diff", "w", encoding="utf-8", errors="ignore") as diff_file:
				diff_file.write(file_diff) # Write the diff to the file

	print(f"{backgroundColors.GREEN}All diffs for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}\n")
print(f"{backgroundColors.GREEN}All diffs for {backgroundColors.CYAN}{list(DEFAULT_REPOSITORY_NAMES.keys())}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}")