import os # OS module in Python provides functions for interacting with the operating system
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
from colorama import Style # For coloring the terminal

# Macros:
class backgroundColors: # Colors for the terminal
	OKCYAN = "\033[96m" # Cyan
	OKGREEN = "\033[92m" # Green
	WARNING = "\033[93m" # Yellow
	FAIL = "\033[91m" # Red
        
# Default paths:
PATH = os.getcwd() # Get the current working directory
DEFAULT_FOLDER = PATH # Get the current working directory
 
# Relative paths:
RELATIVE_CK_METRICS_DIRECTORY_PATH = "/ck_metrics"
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution"
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics"
RELATIVE_REPOSITORY_DIRECTORY_PATH = "/repositories"
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

# Default values:
DEFAULT_REPOSITORY_URL = "https://github.com/apache/commons-lang"
FULL_CK_METRICS_DIRECTORY_PATH = PATH + RELATIVE_CK_METRICS_DIRECTORY_PATH
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH
FULL_METRICS_STATISTICS_DIRECTORY_PATH = PATH + RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH
FULL_REPOSITORY_DIRECTORY_PATH = PATH + RELATIVE_REPOSITORY_DIRECTORY_PATH
FULL_CK_JAR_PATH = PATH + RELATIVE_CK_JAR_PATH

# @brief: This function is used to check if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Check if the PATH constant contains whitespaces
   if " " in PATH:
      return True
   return False

# @brief: Verifiy if the attribute is empty. If so, set it to the default value
# @param: attribute: The attribute to be checked
# @param: default_attribute_value: The default value of the attribute
# @return: The repository URL and the output directory
def validate_attribute(attribute, default_attribute_value):
   if not attribute:
      print(f"{backgroundColors.WARNING}The attribute is empty! Using the default value: {backgroundColors.OKCYAN}{default_attribute_value}{Style.RESET_ALL}")
      attribute = default_attribute_value
   return attribute

# @brief: Get the user input of the repository URL
# @param: None
# @return: repository_url: URL of the repository to be analyzed
def get_user_repository_url():
   # Ask for user input of the repository URL
   repository_url = input(f"{backgroundColors.OKGREEN}Enter the repository URL{backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   # Return the repository URL
   return validate_attribute(repository_url, DEFAULT_REPOSITORY_URL)

# @brief: Get the string after the last slash
# @param: url: URL of the repository to be analyzed
# @return: The name of the repository
def get_repository_name(url):
   return url.split("/")[-1]

# @brief: Update the repository using "git pull"
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def update_repository(repository_name):
   print(f"Updating the {backgroundColors.OKGREEN}{repository_name}{Style.RESET_ALL} repository using {backgroundColors.OKGREEN}git pull{Style.RESET_ALL}.")
   os.chdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name)
   # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + '/' + repository_name
   update_thread = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   # Wait for the thread to finish
   update_thread.wait()
   os.chdir(DEFAULT_FOLDER)

# @brief: Clone the repository to the repository directory
# @param: repository_url: URL of the repository to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def clone_repository(repository_url, repository_name):
   # Check if the repository directory already exists and if it is not empty
   if os.path.isdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name) and os.listdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name):
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository is already cloned!{Style.RESET_ALL}")
      update_repository(repository_name)
      return
   else:
      print(f"{backgroundColors.OKGREEN}Cloning the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
      # Create a thread to clone the repository
      thread = subprocess.Popen(["git", "clone", repository_url, FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # Wait for the thread to finish
      thread.wait()
      print(f"{backgroundColors.OKGREEN}Successfully cloned the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository{Style.RESET_ALL}")

# @brief: Create a subdirectory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
   if os.path.isdir(full_directory_name): # Check if the directory already exists
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory already exists{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_name)
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print (f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory failed{Style.RESET_ALL}")

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_metrics_folders(repository_name):
   print(f"{backgroundColors.OKGREEN}Checking if all the {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} are already calculated for the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
   current_path = PATH
   data_path = os.path.join(current_path, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]) # Join the current path with the relative path of the ck metrics directory
   repo_path = os.path.join(data_path, repository_name) # Join the data path with the repository name
   commit_file = f"commit_hashes-{repository_name}.txt" # The name of the commit hashes file
   commit_file_path = os.path.join(data_path, commit_file) # Join the data path with the commit hashes file

   # Check if the repository exists
   if not os.path.exists(commit_file_path):
      print(f"{backgroundColors.FAIL}File {backgroundColors.OKCYAN}{commit_file}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{data_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
      return False

   # Read the commit hashes file
   with open(commit_file_path, "r") as file:
      lines = file.readlines() # Read all the lines of the file and store them in a list

   # Check if the repository exists
   for line in lines:
      # Get the commit hash
      folder_name = line.strip() # Remove the \n from the line
      folder_path = os.path.join(repo_path, folder_name) # Join the repo path with the folder name

      if not os.path.exists(folder_path): # Check if the folder exists
         print(f"{backgroundColors.FAIL}Folder {backgroundColors.OKCYAN}{folder_name}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{repo_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
         return False
   return True

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
   thread = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = thread.communicate()
   print(thread.decode())

# @brief: This function generates the output directory path for the CK metrics generator
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hash: Commit hash of the commit to be analyzed
# @return: The output_directory and relative_output_directory paths
def generate_output_directory_paths(repository_name, commit_hash):
   output_directory = FULL_CK_METRICS_DIRECTORY_PATH + "/" + repository_name + "/" + commit_hash + "/"
   relative_output_directory = RELATIVE_CK_METRICS_DIRECTORY_PATH + "/" + repository_name + "/" + commit_hash + "/"
   return output_directory, relative_output_directory

# @brief: This function outputs the progress of the analyzed commit
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hash: Commit hash of the commit to be analyzed
# @param: commit_number: Number of the commit to be analyzed
# @param: number_of_commits: Number of commits to be analyzed
# @return: None
def output_commit_progress(repository_name, commit_hash, commit_number, number_of_commits):
   relative_cmd = f"{backgroundColors.OKGREEN}java -jar {backgroundColors.OKCYAN}{RELATIVE_CK_JAR_PATH} {RELATIVE_REPOSITORY_DIRECTORY_PATH}/{repository_name}{backgroundColors.OKGREEN} false 0 false {backgroundColors.OKCYAN}{RELATIVE_CK_METRICS_DIRECTORY_PATH}/{repository_name}/{commit_hash}/"
   print(f"{backgroundColors.OKCYAN}{commit_number} of {number_of_commits}{Style.RESET_ALL} - Running CK: {relative_cmd}{Style.RESET_ALL}")

# @brief: This function traverses the repository
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @param: number_of_commits: Number of commits to be analyzed
# @return: The commit hashes of the repository
def traverse_repository(repository_name, repository_url, number_of_commits):
   i = 1
   commit_hashes = ""
   for commit in Repository(repository_url).traverse_commits():
      commit_hashes += f"{commit.hash}\n"

      workdir_directory = FULL_REPOSITORY_DIRECTORY_PATH + "/" + repository_name
      os.chdir(workdir_directory)        
      checkout_branch(commit.hash)

      # Create the output directory paths
      output_directory, relative_output_directory = generate_output_directory_paths(repository_name, commit.hash)
      # Create the output directory
      create_directory(output_directory, relative_output_directory)

      # change working directory to the repository directory
      os.chdir(output_directory)

      # Output the progress of the analyzed commit
      output_commit_progress(repository_name, commit.hash, i, number_of_commits)

      # Run ck metrics for every commit hash
      cmd = f"java -jar {FULL_CK_JAR_PATH} {workdir_directory} false 0 false {output_directory}"
      run_ck_metrics_generator(cmd)
      
      i += 1
   return commit_hashes

# @brief: Main function
# @param: None
# @return: None
def main():
   # check if the path constants contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.FAIL}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   # Get the user input
   repository_url = get_user_repository_url()

   # Get the name of the repository
   repository_name = get_repository_name(repository_url)

   # create the metrics_evolution directory
   create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH)
   # create the metrics_statistics directory
   create_directory(FULL_METRICS_STATISTICS_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH)

   # Check if the metrics were already calculated
   if check_metrics_folders(repository_name):
      print(f"{backgroundColors.OKGREEN}The metrics for {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} were already calculated{Style.RESET_ALL}")
      return
   
   # Create the repositories directory
   create_directory(FULL_REPOSITORY_DIRECTORY_PATH, RELATIVE_REPOSITORY_DIRECTORY_PATH)

   # Clone the repository
   clone_repository(repository_url, repository_name)
   
   number_of_commits = len(list(Repository(repository_url).traverse_commits()))

   commit_hashes = traverse_repository(repository_name, repository_url, number_of_commits)

   with open(FULL_CK_METRICS_DIRECTORY_PATH + "/" + "commit_hashes-" + repository_name + ".txt", "w") as file:
      file.write(commit_hashes)

   checkout_branch("main")

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function