import os
import pandas as pd
import git
import subprocess
from colorama import Style # For coloring the terminal

# Import from the main.py file
from ck_metrics import backgroundColors

# Current working directory
cwd = os.getcwd()

# Define the repository name and CSV file path
DEFAULT_REPOSITORY_NAME = ["commons-lang", "jabref", "kafka", "zookeeper"] # The default repository names
repository_name = DEFAULT_REPOSITORY_NAME[-1] # The repository name
repository_path = os.path.join(cwd, "repositories", repository_name) # The repository path
csv_file_path = f"/ck_metrics/{repository_name}-commit_hashes.csv" # The CSV file path

# Read the CSV file into a DataFrame
df = pd.read_csv(f"{cwd}{csv_file_path}")

# Get the first two commit hashes
if len(df) < 2:
	print(f"{backgroundColors.RED}There are not enough commits in the CSV file to generate a diff.{Style.RESET_ALL}")
else:
	for i in range(len(df) - 1):
		commit_hash1 = df.iloc[i]["commit hash"]
		commit_hash2 = df.iloc[i+1]["commit hash"]

		# Create the diff folder if it doesn"t exist
		diff_folder_path = f"/diffs/{repository_name}/{commit_hash1}_{commit_hash2}/"
		os.makedirs(f"{cwd}{diff_folder_path}", exist_ok=True)

		# Initialize a Git repository object
		git_repository = git.Repo(repository_path)
		print(f"Git Repository: {git_repository}")

		# Get the list of modified files between the two commits
		diff_index = git_repository.index.diff(commit_hash1, commit_hash2)

		# If the diff index is empty, skip the commit
		if len(diff_index) == 0:
			continue

		print(f"Diff index: {diff_index}")

		# Run the git diff command in the terminal
		diff_command = ["git", "diff", commit_hash1, commit_hash2]
		diff_output = subprocess.check_output(diff_command, cwd=repository_path, universal_newlines=True)

		# Generate a .diff file and save the diff output
		file_path = os.path.join(diff_folder_path, f"{commit_hash1}_{commit_hash2}.diff")
		with open(file_path, "w") as diff_file:
			diff_file.write(diff_output)

		# # Generate a .diff file for each modified file
		# for diff_entry in diff_index:
		# 	file_path = os.path.join(diff_folder_path, diff_entry.a_path + ".diff")
		# 	print(f"File path: {file_path}")
		# 	with open(file_path, "w") as diff_file:
		# 		diff_file.write(diff_entry.diff.decode("utf-8"))
		# 		print(f"{backgroundColors.GREEN}Diff for {backgroundColors.CYAN}{diff_entry.a_path}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}")

		i += 1
		print(f"{backgroundColors.GREEN}Diff {backgroundColors.CYAN}{i} of {len(df)-1}{backgroundColors.GREEN} for {backgroundColors.CYAN}{commit_hash1}{backgroundColors.GREEN} and {backgroundColors.CYAN}{commit_hash2}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}")