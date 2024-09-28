import atexit # For playing a sound when the program finishes
import google.generativeai as genai # Import the Google AI Python SDK
import numpy as np # For handling numerical data
import os # For running a command in the terminal
import pandas as pd # For handling CSV files
import platform # For getting the operating system name
import sys # For exiting the program
import time # For sleeping the program
from collections import Counter # For counting frequencies
from colorama import Style # For coloring the terminal
from concurrent.futures import ThreadPoolExecutor, as_completed # For parallel execution
from dotenv import load_dotenv # For loading .env files
from scipy import stats # For calculating statistics
from sklearn.feature_extraction.text import TfidfVectorizer # For text similarity
from sklearn.metrics.pairwise import cosine_similarity # For text similarity
from threading import Semaphore # For limiting the number of threads

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
RUNS = 5 # Number of runs to perform
MAX_THREADS = 2 # Maximum number of threads to run concurrently

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

def get_env_token(env_path=ENV_PATH, key=ENV_VARIABLE):
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
	:param api_key: The API key to configure the model.
	:return: The configured model.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Configuring the Gemini Model...{Style.RESET_ALL}")

	genai.configure(api_key=api_key) # Configure the Google AI Python SDK

	# Generation configuration
	generation_config = {
		"temperature": 0.1, # Controls the randomness of the output. Values can range from [0.0, 2.0].
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

def prepare_context_message(csv_data):
	"""
	Prepare the context message for the chat session.
	:param csv_data: The CSV data to be included in the message.
	:return: The context message.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Preparing the context message...{Style.RESET_ALL}")

	return f"""
	Hi, Gemini. I will provide you a CSV file containing the following header:
	'Class' field, which is the name of the corresponding class;
	'Method Invocations' field, which is a list following the format: 'method_name of the current class[ invoked_method_name():number_of_invocations ... ]';

	With that in mind, i want you to analyze each line of the CSV and try to relate the terms of the method invocations with topics of Distributed Systems education.
	Here is the CSV data:
	{csv_data}
	"""

def write_output_to_file(output, file_path=OUTPUT_FILE):
	"""
	Writes the chat output to a specified file.
	:param output: The output to write.
	:param file_path: The path to the file.
	:return: None
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Writing the output to the file...{Style.RESET_ALL}")

	with open(file_path, "w") as file:
		file.write(output) # Write the output to the file

def print_output(output):
	"""
	Print the output text.
	:param output: The output text.
	"""
	
	print(f"{BackgroundColors.BOLD}{BackgroundColors.CYAN}Output:{BackgroundColors.GREEN}\n{output}{Style.RESET_ALL}", end="\n") # Output the output

def handle_output(run, output):
	"""
	Handle the output of a run.
	:param run: The run number.
	:param output: The output text.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Handling the output of Run {BackgroundColors.CYAN}{run + 1}/{RUNS}...{Style.RESET_ALL}")

	if RUNS > 1: # If the number of runs is greater than 1
		print(f"{BackgroundColors.GREEN}Thread of Run {BackgroundColors.CYAN}{run + 1}/{RUNS}{BackgroundColors.GREEN} Finished.{Style.RESET_ALL}")
	if VERBOSE: # If the VERBOSE constant is set to True
		print_output(output) # Print the output
	
	# Write the output to a file
	filename = f"{OUTPUT_FILE.split('.')[0]}.{OUTPUT_FILE.split('.')[1]}_{run+1}.{OUTPUT_FILE.split('.')[2]}"
	write_output_to_file(output, filename) # Write the output to a file

def process_future_output(future, run, outputs):
	"""
	Process the output of a future.
	:param future: The future to process.
	:param run: The run number.
	:param outputs: The outputs list.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Thread of Run {BackgroundColors.CYAN}{run + 1}/{RUNS}{BackgroundColors.GREEN} Finished.{Style.RESET_ALL}")

	try: # Try to get the result of the future
		output = future.result() # Get the output from the future
		outputs.append(output) # Add the output
		handle_output(run, output) # Handle the output
	except Exception as exc: # If an exception occurs
		print(f"{BackgroundColors.RED}Run {run} generated an exception: {exc}{Style.RESET_ALL}")

def start_chat_session(model, initial_user_message):
	"""
	Start a chat session with the model.
	:param model: The generative AI model.
	:param initial_user_message: The initial user message.
	:return: The chat session.
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
	:param chat_session: The chat session.
	:param user_message: The user message to send.
	:return: The output.
	"""
 
	verbose_output(true_string=f"{BackgroundColors.GREEN}Sending the message...{Style.RESET_ALL}")

	output = chat_session.send_message(user_message) # Send the message
	return output # Return the output

def perform_run(model, context_message, run_number, retries=3, backoff_factor=0.5):
	"""
	Perform a single run of starting a chat session and sending a message.
	Implements a retry mechanism with exponential backoff in case of server errors.
	:param model: The generative AI model.
	:param context_message: The context message to be sent.
	:param run_number: The run number.
	:param retries: The number of retries.
	:param backoff_factor: The backoff factor.
	:return: The output text.
	"""

	attempt = 0 # Set the attempt to 0
	while attempt <= retries: # While the attempt is less than or equal to the number of retries
		try:
			chat_session = start_chat_session(model, context_message) # Start the chat session
			output = send_message(chat_session, "Please analyze the provided data.") # Send the message
			return output.text # Return the output text
		except Exception as exc: # If an exception occurs
			attempt += 1 # Increment the attempt
			if attempt > retries: # If the attempt is greater than the number of retries
				raise exc # Raise the exception
			wait_time = backoff_factor * (2 ** (attempt - 1)) # Calculate the wait time
			verbose_output(true_string=f"{BackgroundColors.YELLOW}Run {run_number} generated an exception: {exc}. Retrying in {wait_time:.2f} seconds...{Style.RESET_ALL}")
			time.sleep(wait_time) # Sleep the program

	raise Exception(f"{BackgroundColors.RED}Failed to perform run after {BackgroundColors.CYAN}{retries}{BackgroundColors.GREEN} retries.{Style.RESET_ALL}") # Raise an exception

def limited_thread_function(model, semaphore, message, run):
	"""
	Perform a single run of starting a chat session and sending a message with a semaphore.
	:param model: The generative AI model.
	:param semaphore: The semaphore to limit the number of threads.
	:param message: The message to be sent.
	:param run: The run number.
	:return: The output text.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Thread of Run {BackgroundColors.CYAN}{run + 1}/{RUNS}{BackgroundColors.GREEN} Started.{Style.RESET_ALL}")

	with semaphore: # Use the semaphore
		return perform_run(model, message, run) # Perform the run

def perform_runs_with_threading(model, context_message):
	"""
	Perform multiple runs of starting a chat session and sending a message with threading.
	:param model: The generative AI model.
	:param context_message: The context message to be sent.
	:return: The outputs of the runs.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Performing the runs with threading...{Style.RESET_ALL}")

	outputs = [] # Initialize the outputs list
	semaphore = Semaphore(MAX_THREADS) # Create a semaphore to limit the number of threads

	with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
		future_to_run = {executor.submit(limited_thread_function, model, semaphore, context_message, run): run for run in range(RUNS)} # Create a future to run dictionary
		for future in as_completed(future_to_run): # For each future in the completed futures
			run = future_to_run[future] # Get the run from the future
			process_future_output(future, run, outputs) # Process the future output

	return outputs # Return the outputs

def analyze_outputs(outputs):
	"""
	Analyze the outputs and return the most frequent output.
	:param outputs: The outputs to analyze.
	:return: The most frequent output.
	"""
	
	output_counts = Counter(outputs) # Count the frequencies of the outputs
	most_frequent_output = output_counts.most_common(1)[0][0] # Get the most frequent output
	write_output_to_file(most_frequent_output, MOST_COMMON_OUTPUT_FILE) # Write the most frequent output to a file
	return most_frequent_output # Return the most frequent output

def calculate_similarity_and_confidence(outputs, confidence=0.95):
	"""
	Calculate the average similarity between multiple outputs and the confidence interval.
	:param outputs: The outputs to calculate the similarity.
	:param confidence: The confidence level.
	:return: The average similarity and confidence interval.
	"""

	verbose_output(true_string=f"{BackgroundColors.GREEN}Calculating the similarity between the outputs...{Style.RESET_ALL}")

	if not outputs or len(outputs) == 1: # If there are no outputs or only one output
		return 0.0, (0.0, 0.0) # No similarity or undefined confidence interval

	vectorizer = TfidfVectorizer().fit_transform(outputs) # Fit the vectorizer and transform the outputs
	vectors = vectorizer.toarray() # Convert the vectors to an array
	cosine_matrix = cosine_similarity(vectors) # Calculate the cosine similarity matrix
	np.fill_diagonal(cosine_matrix, 0) # Ignore self-similarity

	# Get upper triangle of the matrix, ignoring the diagonal
	upper_tri_indices = np.triu_indices_from(cosine_matrix, k=1)
	similarities = cosine_matrix[upper_tri_indices]

	avg_similarity = similarities.mean() # Calculate the average similarity
	sem = stats.sem(similarities) # Calculate the standard error of the mean
	ci = stats.t.interval(confidence, len(similarities)-1, loc=avg_similarity, scale=sem) # Calculate the confidence interval

	return avg_similarity, ci # Return the average similarity and confidence interval

def report_run_statistics(outputs):
	"""
	Report the run statistics.
	:param outputs: The outputs to analyze.
	"""

	avg_similarity, confidence_interval = calculate_similarity_and_confidence(outputs, 0.95) # Calculate the average similarity and confidence interval

	print(f"\n{BackgroundColors.BOLD}{BackgroundColors.GREEN}Average Similarity between {BackgroundColors.CYAN}{RUNS}{BackgroundColors.GREEN} Runs: {BackgroundColors.CYAN}{avg_similarity:.2f}{Style.RESET_ALL}")
	print(f"{BackgroundColors.BOLD}{BackgroundColors.GREEN}95% Confidence Interval for the Gemini's Output Similarity: {BackgroundColors.CYAN}({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}){Style.RESET_ALL}", end="\n\n")

def main():
	"""
	Main function.
	:return: None
	"""

	print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Welcome to the {BackgroundColors.CYAN}Google Gemini API Integration{BackgroundColors.GREEN}!{Style.RESET_ALL}", end="\n\n") # Output the Welcome message

	# Verify .env file and load API key
	api_key = get_env_token(ENV_PATH, ENV_VARIABLE)

	create_directory(os.path.abspath(OUTPUT_DIRECTORY), OUTPUT_DIRECTORY.replace(".", "")) # Create the output directory

	# Configure the model
	model = configure_model(api_key)

	# Load and filter the CSV file
	csv_data = load_csv_file(CSV_INPUT_FILE)

	context_message = prepare_context_message(csv_data) # Start chat session and send message
	outputs = perform_runs_with_threading(model, context_message) # Perform the runs with threading
	most_frequent_output = analyze_outputs(outputs) # Analyze the outputs

	if RUNS > 1: # If the number of runs is greater than 1
		report_run_statistics(outputs) # Report the run statistics

	print(f"{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

if __name__ == "__main__":
	"""
	This is the standard boilerplate that calls the main() function.
	:return: None
	"""

	main() # Call the main function
