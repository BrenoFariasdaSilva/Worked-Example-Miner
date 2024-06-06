import atexit # For playing a sound when the program finishes
import google.generativeai as genai # Import the Google AI Python SDK
import numpy as np # For handling numerical data
import os # For running a command in the terminal
import pandas as pd # For handling CSV files
import platform # For getting the operating system name
import sys # For exiting the program
from collections import Counter # For counting frequencies
from colorama import Style # For coloring the terminal
from concurrent.futures import ThreadPoolExecutor, as_completed # For parallel execution
from dotenv import load_dotenv # For loading .env files
from sklearn.feature_extraction.text import TfidfVectorizer # For text similarity
from sklearn.metrics.pairwise import cosine_similarity # For text similarity

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
SOUND_FILE = "../.assets/Sounds/NotificationSound.wav" # The path to the sound file

# Execution Constants:
VERBOSE = False # Verbose mode. If set to True, it will output messages at the start/call of each function (Note: It will output a lot of messages).
RUNS = 10 # Number of runs to perform

# .Env Constants:
ENV_PATH = "../.env" # The path to the .env file
ENV_VARIABLE = "GEMINI_API_KEY" # The environment variable to load

# File Path Constants:
CSV_INPUT_FILE = "../PyDriller/metrics_statistics/zookeeper/substantial_CBO_classes_changes.csv" # The path to the input JSON file
OUTPUT_DIRECTORY = "./Outputs/" # The path to the output directory
OUTPUT_FILE = f"{OUTPUT_DIRECTORY}output.txt" # The path to the output file
MOST_COMMON_OUTPUT_FILE = f"{OUTPUT_DIRECTORY}most_common_output.txt" # The path to the most common output file

# Header Constants:
DESIRED_HEADER = ["Class", "Method Invocations"] # The desired header of the CSV file

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

def configure_model(api_key):
	"""
	Configure the generative AI model.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Configuring the Gemini Model...{Style.RESET_ALL}")

	genai.configure(api_key=api_key) # Configure the Google AI Python SDK

	# Generation configuration
	generation_config = {
		"temperature": 1, # Controls the randomness of the output. Values can range from [0.0, 2.0].
		"top_p": 0.95, # Optional. The maximum cumulative probability of tokens to consider when sampling.
		"top_k": 64, # Optional. The maximum number of tokens to consider when sampling.
		"max_output_tokens": 8192, # Set the maximum number of output tokens
	}

	# Create the model
	model = genai.GenerativeModel(
		model_name="gemini-1.5-flash", # Set the model name
		generation_config=generation_config, # Set the generation configuration
	)

	return model # Return the model

def load_csv_file(file_path):
	"""
	Load and filter the CSV file by "Class" and "Method Invocations" fields.
	:param file_path: Path to the CSV file.
	:return: Filtered data as a string.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Loading the CSV file...{Style.RESET_ALL}")

	if not os.path.exists(file_path):
		print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}CSV file{BackgroundColors.RED} not found at {BackgroundColors.CYAN}{file_path}{Style.RESET_ALL}")
		sys.exit(1) # Exit the program

	df = pd.read_csv(file_path) # Load the CSV file

	missing_columns = [col for col in DESIRED_HEADER if col not in df.columns] # Get the missing columns
	if missing_columns: # If there are missing columns
		print(f"{BackgroundColors.RED}The CSV file must contain {BackgroundColors.CYAN}{', '.join(missing_columns)}{BackgroundColors.RED} columns.{Style.RESET_ALL}")
		sys.exit(1) # Exit the program

	# Filter the data
	filtered_data = df[DESIRED_HEADER].to_string(index=False) # Filter the data and convert it to a string
	return filtered_data # Return the filtered data

def start_chat_session(model, initial_user_message):
	"""
	Start a chat session with the model.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Starting the chat session...{Style.RESET_ALL}")

	chat_session = model.start_chat(
		history=[
			{
				"role": "user",
				"parts": [
					initial_user_message,
				],
			}
		]
	)

	return chat_session # Return the chat session

def send_message(chat_session, user_message):
	"""
	Send a message in the chat session and get the output.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sending the message...{Style.RESET_ALL}")

	output = chat_session.send_message(user_message) # Send the message
	return output # Return the output

def print_output(output):
	"""
	Print the output text.
	"""
	
	print(f"{BackgroundColors.BOLD}{BackgroundColors.CYAN}Output:{BackgroundColors.GREEN}\n{output}{Style.RESET_ALL}", end="\n") # Output the output

def write_output_to_file(output, file_path=OUTPUT_FILE):
	"""
	Writes the chat output to a specified file.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the output to the file...{Style.RESET_ALL}")

	with open(file_path, "w") as file:
		file.write(output) # Write the output to the file

def calculate_similarity(outputs):
	"""
	Calculate the average similarity between multiple outputs.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating the similarity between the outputs...{Style.RESET_ALL}")

	# If there are no outputs or only one output, return 0 similarity
	if not outputs or len(outputs) == 1:
		return 0.0 # No similarity

	vectorizer = TfidfVectorizer().fit_transform(outputs) # Get the vectorizer
	vectors = vectorizer.toarray() # Get the vectors
	cosine_matrix = cosine_similarity(vectors) # Get the cosine matrix
	np.fill_diagonal(cosine_matrix, 0) # Ignore self-similarity
	avg_similarity = cosine_matrix.mean() # Get the average similarity

	return avg_similarity # Return the average similarity

def perform_run(model, start_message):
	"""
	Perform a single run of starting a chat session and sending a message.
	"""

	chat_session = start_chat_session(model, start_message)
	output = send_message(chat_session, "Please analyze the provided data.")
	return output.text

def main():
	"""
	Main function.
	:return: None
	"""

	print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Google Gemini API Integration{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the Welcome message

	# Verify .env file and load API key
	api_key = verify_env_file(ENV_PATH, ENV_VARIABLE)

	# OUTPUT_DIRECTORY.replace(".", "").replace("/", "")
	create_directory(os.path.abspath(OUTPUT_DIRECTORY), OUTPUT_DIRECTORY.replace(".", "")) # Create the output directory

	# Configure the model
	model = configure_model(api_key)

	# Load and filter the CSV file
	csv_data = load_csv_file(CSV_INPUT_FILE)

	# Start chat session and send message
	start_message = f"""
	Hi, Gemini. I will provide you a CSV file containing the following header:
	'Class' field, which is the name of the corresponding class;
	'Method Invocations' field, which is a list following the format: 'method_name of the current class[ invoked_method_name():number_of_invocations ... ]';
	
	With that in mind, i want you to analyze each line of the CSV and try to relate the terms of the method invocations with topics of Distributed Systems education.
	Here is the CSV data:
	{csv_data}
	"""

	outputs = [] # List to store the outputs generated

	with ThreadPoolExecutor() as executor:
		future_to_run = {executor.submit(perform_run, model, start_message): run for run in range(RUNS)}
		for future in as_completed(future_to_run):
			run = future_to_run[future]
			try:
				output = future.result() # Get the output from the future
				if RUNS > 1: # If the number of runs is greater than 1
					print(f"{BackgroundColors.GREEN}Thread of Run {BackgroundColors.CYAN}{run + 1}/{RUNS}{BackgroundColors.GREEN} Finished.{Style.RESET_ALL}")

				if VERBOSE: # If the VERBOSE constant is set to True
					print_output(output) # Print the output

				write_output_to_file(output, f"{OUTPUT_FILE.split('.')[0]}.{OUTPUT_FILE.split('.')[1]}_{run+1}.{OUTPUT_FILE.split('.')[2]}") # Write the output to a file
				outputs.append(output) # Add the output
			except Exception as exc:
				print(f"{BackgroundColors.RED}Run {run} generated an exception: {exc}{Style.RESET_ALL}")

	# Count the frequency of each output
	output_counts = Counter(outputs)
	most_frequent_output = output_counts.most_common(1)[0][0]

	# Write the most frequent output to a file
	write_output_to_file(most_frequent_output, MOST_COMMON_OUTPUT_FILE) # Write the output to a file

	if RUNS > 1: # If the number of runs is greater than 1
		avg_similarity = calculate_similarity(outputs) # Calculate the average similarity between the outputs
		print(f"\n{BackgroundColors.BOLD}{BackgroundColors.CYAN}Average Similarity between Runs: {avg_similarity:.2f}{Style.RESET_ALL}", end="\n\n")

	print(f"{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
	"""
	This is the standard boilerplate that calls the main() function.
	:return: None
	"""

	main() # Call the main function
