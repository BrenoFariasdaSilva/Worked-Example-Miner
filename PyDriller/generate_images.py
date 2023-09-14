import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
import matplotlib.pyplot as plt # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
import atexit # For playing a sound when the program finishes
import platform # For getting the operating system name
import time # For displaying the execution time 
from colorama import Style # For coloring the terminal

# Import from the main.py file
from ck_metrics import backgroundColors
        
# Constants:
PATH = os.getcwd() # Get the current working directory
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The sound commands for each operating system
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# Changable constants:
CLASS_CSV_FILE = "class.csv" # The name of the csv generated file from ck.
METHOD_CSV_FILE = "method.csv" # The name of the csv generated file from ck.
PROCESS_CLASSES = input(f"{backgroundColors.GREEN}Do you want to process the {backgroundColors.CYAN}class.csv{backgroundColors.GREEN} file {backgroundColors.RED}(True/False){backgroundColors.GREEN}? {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
CK_CSV_FILE = CLASS_CSV_FILE if PROCESS_CLASSES else METHOD_CSV_FILE # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
OPPOSITE_CK_CSV_FILE = METHOD_CSV_FILE if PROCESS_CLASSES else CLASS_CSV_FILE # The name of the csv generated file from ck.
DEFAULT_REPOSITORY_NAMES = ["commons-lang", "jabref", "kafka", "zookeeper"] # The default repository names
CURRENT_REPOSITORY_NAME = DEFAULT_REPOSITORY_NAMES[0] # The current repository name
DEFAULT_CLASS_IDS = {"org.apache.commons.lang.StringUtils": ["class"]} # The default ids to be analyzed. It stores the class:type
DEFAULT_METHOD_IDS = { # The default ids to be analyzed. It stores the method:class
   "org.apache.commons.lang3.AnnotationUtilsTest": ["testBothArgsNull/0"],
   "org.apache.commons.lang.LangTestSuite": ["suite/0"]}
DEFAULT_IDS = DEFAULT_CLASS_IDS if PROCESS_CLASSES else DEFAULT_METHOD_IDS # The default ids to be analyzed. It stores the class:type or method:class
IMAGE_LABELS = [True, True]
REPOSITORY_LABELS_TYPE = {"commons-lang": ["y*", 1], "jabref": ["y*", 1], "kafka": ["y*", 1], "zookeeper": ["y*", 1]} # The labels type for each repository
SORTED_CHANGES_CSV_FILENAME = f"sorted_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the sorted top changes
 
# Relative paths:
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution" # The relative path of the metrics_evolution directory
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics" # The relative path of the metrics_statistics directory
RELATIVE_GRAPHICS_DIRECTORY_PATH = "/graphics" # The relative path of the graphics directory

# Default values:
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH # The full path of the metrics_evolution directory
FULL_GRAPHICS_DIRECTORY_PATH = PATH + RELATIVE_GRAPHICS_DIRECTORY_PATH # The full path of the graphics directory

# @brief: This function is used to verify if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Verify if the PATH constant contains whitespaces
   if " " in PATH:
      return True # Return True if the PATH constant contains whitespaces
   return False # Return False if the PATH constant does not contain whitespaces

# @brief: This function loops through the DEFAULT_REPOSITORY_NAME list
# @param: None
# @return: None
def loop_through_default_repository_names():
   loop_start_time = time.time() # Start the timer
   for repository_name in DEFAULT_REPOSITORY_NAMES: # Loop through the DEFAULT_REPOSITORY_NAME list
      process_repository(repository_name) # Process the current repository
      print(f"")
      print(f"------------------------------------------------------------")
      print(f"")
   print(f"")
   elapsed_time = time.time() - loop_start_time
   elapsed_time_string = f"Time taken to generate the {backgroundColors.CYAN}metrics changes{backgroundColors.GREEN} for the {backgroundColors.CYAN}{DEFAULT_REPOSITORY_NAMES} {CLASSES_OR_METHODS}{backgroundColors.GREEN}: "
   output_time(elapsed_time_string, round(elapsed_time, 2))

# @brief: This function call the procedures to process the specified repository
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def process_repository(repository_name):
   start_time = time.time(repository_name) # Start the timer

   # Get the ids from the user
   ids = get_user_ids_input(repository_name)

   # Validate the ids, if is related to a class or method
   if not validate_ids(ids, repository_name):
      print(f"{backgroundColors.RED}The {backgroundColors.CYAN}{', '.join(ids.keys())}{backgroundColors.RED} are {OPPOSITE_CK_CSV_FILE.replace('.csv', '')} instead of {CK_CSV_FILE.replace('.csv', '')} names. Please change them!{Style.RESET_ALL}")
      return

   # Verify if the metrics evolution were already calculated
   if not check_metrics_files(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, repository_name, ids):
      print(f"{backgroundColors.RED}The metrics evolution for {backgroundColors.CYAN}{', '.join(ids.keys())}{backgroundColors.RED} in {backgroundColors.CYAN}{repository_name}{backgroundColors.RED} were not created. Please run the {backgroundColors.CYAN}metrics_changes.py{backgroundColors.RED} file first.{Style.RESET_ALL}")
      return

   # Get the number of ids to be analyzed
   number_of_ids = sum(len(attributes) for attributes in ids.values())
   current_id = 1

   # Iterate through each class and its variable attributes
   for index, (class_name, variable_attributes) in enumerate(ids.items()):
      for attribute_index, attribute in enumerate(variable_attributes): # Iterate through each variable attribute of the class
         print(f"{backgroundColors.GREEN}Generating Image {backgroundColors.CYAN}{current_id} of {number_of_ids}{backgroundColors.GREEN} for the {backgroundColors.CYAN}{attribute} {CK_CSV_FILE.replace('.csv', '')}{backgroundColors.GREEN} inside the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository.{Style.RESET_ALL}")
         create_metrics_evolution_graphic(repository_name, class_name, get_clean_id(attribute)) # Create the metrics evolution graphs
         current_id += 1

   print(f"{backgroundColors.CYAN}Successfully created the metrics evolution graphics{backgroundColors.GREEN} for the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository inside the {backgroundColors.CYAN}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:]}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")

   elapsed_time = time.time() - start_time
   elapsed_time_string = f"Time taken to generate the {backgroundColors.CYAN}images{backgroundColors.GREEN} for the {backgroundColors.CYAN}{CLASSES_OR_METHODS}{backgroundColors.GREEN} in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
   output_time(elapsed_time_string, round(elapsed_time, 2))

# @brief: Create a directory if it does not exist
# @param: full_directory_path: Name of the directory to be created
# @param: relative_directory_path: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_path, relative_directory_path):
   if os.path.isdir(full_directory_path): # Verify if the directory already exists
      print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}{relative_directory_path}{backgroundColors.GREEN} directory already exists.{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_path)
      print(f"{backgroundColors.GREEN}Successfully created the {backgroundColors.CYAN}{relative_directory_path}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print(f"{backgroundColors.GREEN}The creation of the {backgroundColors.CYAN}{relative_directory_path}{backgroundColors.GREEN} directory failed.{Style.RESET_ALL}")

# @brief: Get user input of the name of the class or method to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: id: Name of the class or method to be analyzed
def get_user_ids_input(repository_name):
   ids = {} # Dictionary that stores the ids to be analyzed
   input_source = input(f"{backgroundColors.GREEN}Enter the {backgroundColors.CYAN}source of input{backgroundColors.GREEN} to get {backgroundColors.CYAN}IDS{backgroundColors.GREEN} {backgroundColors.RED}(default/all){backgroundColors.GREEN}: {Style.RESET_ALL}")

   while input_source.lower() != "default" and input_source.lower() != "all": # While the input_source is not "default" or "all"
      print(f"{backgroundColors.RED}Invalid input source!{Style.RESET_ALL}")
      input_source = input(f"{backgroundColors.GREEN}Enter the {backgroundColors.CYAN}source of input{backgroundColors.GREEN} to get {backgroundColors.CYAN}IDS{backgroundColors.GREEN} {backgroundColors.RED}(default/all){backgroundColors.GREEN}: {Style.RESET_ALL}")

   # If the input_source is "all", them get every variable_attribute of each class.
   if input_source.lower() == "all":
      variable_attribute = "Type" if PROCESS_CLASSES else "Method"
      top_changes_csv_path = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "/" + CK_CSV_FILE.replace('.csv', '') + "-" + SORTED_CHANGES_CSV_FILENAME
      # Open the top changes csv file and get the class/method and variable attribute data
      with open(top_changes_csv_path, "r") as file: 
         csv_reader = csv.DictReader(file) # Read the csv file
         for row in csv_reader: # Loop trough the csv file
            if int(row["Changed"]) > MINIMUM_CHANGES: # If the number of changes is greater than the minimum number of changes
               class_name = row["Class"] # Get the class name
               variable_attribute_value = row[variable_attribute] # Get the variable attribute
                
               if class_name not in ids: # If the class is not in the dictionary
                  ids[class_name] = [variable_attribute_value] # Initialize list for variable attributes
               else: # If the class is in the dictionary
                  ids[class_name].append(variable_attribute_value) # Append variable attribute to the existing list

   # If the input_source is "default", them get the ids from the DEFAULT_IDS dictionary.
   if input_source.lower() == "default":
      ids = DEFAULT_IDS
      print(f"{backgroundColors.GREEN}Using the default stored {CK_CSV_FILE.replace('.csv', '')} names: {backgroundColors.CYAN}{', '.join(ids.keys())}{backgroundColors.GREEN}.{Style.RESET_ALL}")

   return ids # Return the IDs to be analyzed

# @brief: This function validates if the ids are as the same type as the files to be analyzed defined in CK_CSV_FILE according to PROCESS_CLASSES
# @param: ids: Dictionary containing the ids to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: True if the ids are valid, False otherwise
def validate_ids(ids, repository_name):
   # Get the path of the file containing the top changes of the classes
   repo_top_changes_file_path = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "/" + CK_CSV_FILE.replace('.csv', '') + "-" + SORTED_CHANGES_CSV_FILENAME

   df = pd.read_csv(repo_top_changes_file_path)
   variable_attribute = "Type" if PROCESS_CLASSES else "Method"

   # Verify if the ids are as the same type as the files to be analyzed defined in CK_CSV_FILE according to PROCESS_CLASSES
   for key, values in ids.items():
      for value in values:
         matching_row = df[(df["Class"] == key) & (df[variable_attribute] == value)] # Get the row that matches the class and variable attribute
         if matching_row.empty:
            return False # Return False if the id is not found in the CSV file
   return True # Return True if all ids are valid (found in the CSV file)

# @brief: This function receives an id and verify if it contains slashes, if so, it returns the id without the slashes
# @param: id: ID of the class or method to be analyzed
# @return: ID of the class or method to be analyzed without the slashes
def get_clean_id(id):
   if "/" in id: # If the id contains slashes, remove them
      return str(id.split("/")[0:-1])[2:-2]
   else:
      return id

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: folder_path: The path of the folder to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @param: ids: The ids to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_metrics_files(folder_path, repository_name, ids):
   print(f"{backgroundColors.GREEN}Checking if all the {backgroundColors.CYAN}{folder_path.rsplit('/', 1)[-1]}{backgroundColors.GREEN} are already created.{Style.RESET_ALL}")
   original_path = os.getcwd() # Store the original working directory
   try:
      os.chdir(folder_path) # Change the current working directory to the repository folder
      for id, values in ids.items(): # Iterate through each class and its variable attributes
         for value in values: # Iterate through each variable attribute of the class
            file_name = f"{id} {value}" if PROCESS_CLASSES else f"{id} {get_clean_id(value)}"
            evolution_file = os.path.join(repository_name, CLASSES_OR_METHODS, f"{file_name}.csv")
            if not os.path.isfile(evolution_file):
               print(f"{backgroundColors.YELLOW}The {backgroundColors.CYAN}{file_name}.csv{backgroundColors.YELLOW} file does not exist.{Style.RESET_ALL}")
               return False
   finally:
      os.chdir(original_path) # Change the current working directory back to the original path

   return True

# @brief: Add the desired label type to the data points of the graphic image
# @param: df: DataFrame containing the metrics data
# @param: label_type: Type of label to be added to the data points of the graphic image
# @param: commit_hashes: List containing the commit hashes
# @param: metric_values: List containing the metric values
# @return: None
def add_labels_to_plot(plt, label_type, commit_hashes, metric_values):
   # Add the desired label type to the data points of the graphic image
   if label_type == "1":
      # Add labels to each data point
      for j, value in enumerate(metric_values):
         plt.text(commit_hashes[j], value, f"{j+1}º", ha="center", va="bottom", fontsize=12)
   elif label_type == "2":
      # Add labels to each data point
      for j, value in enumerate(metric_values):
         plt.text(commit_hashes[j], value, f"{value}", ha="center", va="bottom", fontsize=12)

# @brief: This function gets the plt object and add each metric first and last value to the plot
# @param: plt: plt object
# @param: df: DataFrame containing the metrics data
# @return: None
def add_first_and_last_values_to_plot(plt, df):
   # Add the first and last values of each metric (CBO, CBO Modified, WMC, RFC) to the graphic image
   plt.text(0.20, 0.97, f"CBO {df['CBO'].iloc[0]} -> {df['CBO'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.20, 0.92, f"CBOModified {df['CBO Modified'].iloc[0]} -> {df['CBO Modified'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.70, 0.97, f"WMC {df['WMC'].iloc[0]} -> {df['WMC'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.70, 0.92, f"RFC {df['RFC'].iloc[0]} -> {df['RFC'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)

# @brief: This function creates the metrics evolution graphs fronm the RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH folder
# @param: repository_name: Name of the repository to be analyzed
# @param: id: ID of the class or method to be analyzed
# @param: clean_id_key: Clean ID of the class or method to be analyzed
# @return: None
def create_metrics_evolution_graphic(repository_name, id, clean_id_key):
   # Load the generated CSV files into a dataframe and save a plot of the evolution of the CBO, CBO Modified, WMC and RFC metrics
   df = pd.read_csv(PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id + " " + clean_id_key + ".csv")

   # Extract the metrics and commit hashes from the DataFrame
   commit_hashes = df["Commit Hash"]
   metrics = ["CBO", "CBO Modified", "WMC", "RFC"]

   # Set the attributes of the graph: colors, line styles and marker sizes
   colors = ["blue", "pink", "green", "orange"]
   line_styles = ["-", "--", "-.", ":"]
   marker_sizes = [5, 5, 5, 5] if PROCESS_CLASSES else [6, 10, 6, 10]

   # Plotting the graph
   plt.figure(figsize=(38.4, 21.6))

   # Iterate over each metric and plot its evolution with a different color
   for i, metric in enumerate(metrics):
      metric_values = df[metric]
      plt.plot(commit_hashes, df[metric], marker="o", label=metric, linestyle=line_styles[i], markersize=marker_sizes[i], color=colors[i])

      if REPOSITORY_LABELS_TYPE[repository_name][0] == "y*":
         add_labels_to_plot(plt, REPOSITORY_LABELS_TYPE[repository_name][1], commit_hashes, metric_values)

   # Set the graph title and labels according to the type of analysis (class or method)
   if PROCESS_CLASSES:
      plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {id} {clean_id_key} in {repository_name} repository", color="red")
   else:
      plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {clean_id_key} {id} in {repository_name} repository", color="red")
   plt.xlabel("Commit Hash")
   plt.ylabel("Metric Value")

   add_first_and_last_values_to_plot(plt, df)

   # Rotate the x-axis labels for better readability
   plt.xticks(rotation=0)
   plt.xticks([commit_hashes[0], commit_hashes.iloc[-1]], visible=True, rotation="horizontal")

   # Set the color of x-values (commit hashes) and y-values (metric values)
   plt.tick_params(axis="x", colors="red")
   plt.tick_params(axis="y", colors="red")

   # Add a legend
   plt.legend()

   # Add a grid
   plt.tight_layout()

   # create the graphics directory if it doesn't exist
   create_directory(FULL_GRAPHICS_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id, RELATIVE_GRAPHICS_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id)

   # Save the graph
   plt.savefig(FULL_GRAPHICS_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id + "/" + clean_id_key + ".png")

   # Close the plot
   plt.close()

   object_reference = f"{clean_id_key}" if PROCESS_CLASSES else f"{clean_id_key} {CK_CSV_FILE.replace('.csv', '')}"
   print(f"{backgroundColors.CYAN}Successfully{backgroundColors.GREEN} created the {backgroundColors.CYAN}metrics evolution graphic {backgroundColors.GREEN}for {backgroundColors.CYAN}{id} {object_reference}{backgroundColors.GREEN} from the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository.{Style.RESET_ALL}")
   print()

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

# @brief: Main function
# @param: None
# @return: None
def main():
   # Verify if the path constant contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   print(f"{backgroundColors.GREEN}This script {backgroundColors.CYAN}generates the images{backgroundColors.GREEN} from the {backgroundColors.CYAN}metrics evolution{backgroundColors.GREEN} of the {CK_CSV_FILE.replace('.csv', '')} of a {backgroundColors.CYAN}specific repository{backgroundColors.GREEN}.{Style.RESET_ALL}")
   print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}source of the data{backgroundColors.GREEN} used to {backgroundColors.CYAN}generate the images{backgroundColors.GREEN} is the {backgroundColors.CYAN}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")

   # Asks for user input if wants to process all the repositories or just one
   process_all_repositories = input(f"{backgroundColors.GREEN}Do you want to process all the repositories? {backgroundColors.CYAN}(y/n){backgroundColors.GREEN}: {Style.RESET_ALL}")
   # Verify if the user wants to process all the repositories
   if process_all_repositories.lower() == "y" or process_all_repositories.lower() == "":
      print(f"{backgroundColors.GREEN}Processing all the repositories: {backgroundColors.CYAN}{DEFAULT_REPOSITORY_NAMES}{Style.RESET_ALL}")
      loop_through_default_repository_names() # Process all the repositories
   else:
      print(f"{backgroundColors.GREEN}Processing a single repository: {backgroundColors.CYAN}{CURRENT_REPOSITORY_NAME}{Style.RESET_ALL}")
      process_repository(CURRENT_REPOSITORY_NAME) # Process a single repository, that is, the CURRENT_REPOSITORY_NAME.

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function