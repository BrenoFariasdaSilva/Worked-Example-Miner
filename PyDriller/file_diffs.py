import os # The OS module in Python provides functions for interacting with the operating system.
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
from colorama import Style # Colorama is a Python library for printing colored text and stylizing terminal output.
from ck_metrics import backgroundColors # Import the background colors from the ck_metrics module

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
			with open(f"{diff_file_directory}{modified_file.filename}", "w", encoding="utf-8", errors="ignore") as diff_file:
				diff_file.write(file_diff) # Write the diff to the file

	print(f"{backgroundColors.GREEN}All diffs for {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}\n")
print(f"{backgroundColors.GREEN}All diffs for {backgroundColors.CYAN}{list(DEFAULT_REPOSITORY_NAMES.keys())}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}")