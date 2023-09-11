import os
import pandas as pd
import subprocess
from colorama import Style
from ck_metrics import backgroundColors

# Current working directory
cwd = os.getcwd()

# Define the repository name and CSV file path
DEFAULT_REPOSITORY_NAME = ["commons-lang", "jabref", "kafka", "zookeeper"]

for i in range(len(DEFAULT_REPOSITORY_NAME)):
	repository_name = DEFAULT_REPOSITORY_NAME[i]
	repository_path = os.path.join(cwd, "repositories", repository_name)
	csv_file_path = os.path.join(cwd, "ck_metrics", f"{repository_name}-commit_hashes.csv")

	# Read the CSV file into a DataFrame
	df = pd.read_csv(f"{csv_file_path}")

	# Get the first two commit hashes
	if len(df) < 2:
		print(f"{backgroundColors.RED}There are not enough commits in the CSV file to generate a diff.{Style.RESET_ALL}")
	else:
		for i in range(len(df) - 1):
			commit_hash1 = df.iloc[i]["commit hash"]
			commit_hash2 = df.iloc[i + 1]["commit hash"]

			# Create the diff folder if it doesn't exist
			diff_folder_path = os.path.join(cwd, "diffs", repository_name, f"{commit_hash1}_{commit_hash2}")
			os.makedirs(diff_folder_path, exist_ok=True)

			# Run the git diff command in the terminal
			diff_command = ["git", "diff", commit_hash1, commit_hash2]
			try:
				diff_output = subprocess.check_output(diff_command, cwd=repository_path, stderr=subprocess.STDOUT, universal_newlines=True)
			except subprocess.CalledProcessError as e:
				diff_output = e.output

			# Split the diff into individual file diffs
			diff_parts = diff_output.split("diff --git")

			for j, diff_part in enumerate(diff_parts):
				if j == 0:
					continue # Skip the first empty part

				print(f"j: {j} of {len(diff_parts)-1}")
				# print(f"diff_part: {diff_part}")

				file_diff = "diff --git" + diff_part  # Re-add the "diff --git" part

				# Extract the file path from the diff
				file_path_start = file_diff.find(" a/") + 3
				file_path_end = file_diff.find(" b/")
				file_path = file_diff[file_path_start:file_path_end]

				# Generate a .diff file for each modified file
				file_path = os.path.join(diff_folder_path, f"{file_path.replace('/', '_')}.diff")
				with open(file_path, "w", encoding="utf-8", errors="ignore") as diff_file:
					diff_file.write(file_diff)

				print(f"{Style.RESET_ALL}{backgroundColors.GREEN}Diff {backgroundColors.CYAN}{i+1} of {len(df)-1}{backgroundColors.GREEN} for {backgroundColors.CYAN}{commit_hash1}{backgroundColors.GREEN} and {backgroundColors.CYAN}{commit_hash2}{backgroundColors.GREEN} saved successfully.{Style.RESET_ALL}")

	print(f"{backgroundColors.GREEN}All diffs generated and saved.{Style.RESET_ALL}")
