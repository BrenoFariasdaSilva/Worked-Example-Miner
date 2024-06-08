<div align="center">

# [Google Gemini.](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/tree/main/Gemini)  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the Google Gemini API integration directory, in which you will find the script used to interact with the Google Gemini API in order to help analyze the good candidates in order to generate a worked example for the classes of Software Engineering courses, as this is the main goals of this project. The scripts that are located in this directory are part of the [Worked-Example-Miner (WEM)](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) Tool.

---

</div>

- [Google Gemini.  ](#google-gemini--)
  - [Important Notes](#important-notes)
  - [Setup](#setup)
    - [Python and Pip](#python-and-pip)
      - [Linux](#linux)
      - [MacOS](#macos)
      - [Windows](#windows)
    - [Requirements](#requirements)
    - [Cleaning Up](#cleaning-up)
  - [How to use](#how-to-use)
    - [gemini\_script](#gemini_script)
      - [Configuration](#configuration)
      - [Run](#run)
      - [Workflow](#workflow)
  - [Generated Data](#generated-data)
    - [Output](#output)
    - [Results and Discussion](#results-and-discussion)
  - [Contributing](#contributing)
  - [License](#license)

## Important Notes

- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- To enhance the readability of the code, please note that the files adhere to a Bottom-Up approach in function ordering. This means that each function is defined above the function that calls it.
- All of the Scripts have a `Makefile`that handles virtual environment creation, dependencies installation and script execution. You can run the scripts by using the `make` command, as shown in the `How to use` section.

## Setup

This section provides instructions for installing the Python Language and Pip Python package manager, as well as the project's dependencies. It also explains how to run the scripts using the provided `makefile`. The `makefile` automates the process of creating a virtual environment, installing dependencies, and running the scripts.

### Python and Pip

In order to run the scripts, you must have python3 and pip installed in your machine. If you don't have it installed, you can use the following commands to install it:

#### Linux

In order to install python3 and pip in Linux, you can use the following commands:

```
sudo apt install python3 -y
sudo apt install python3-pip -y
```

#### MacOS

In order to install python3 and pip in MacOS, you can use the following commands:

```
brew install python3
```

#### Windows

In order to install python3 and pip in Windows, you can use the following commands in case you have `choco` installed:

```
choco install python3
```

Or just download the installer from the [official website](https://www.python.org/downloads/).

Great, you now have python3 and pip installed. Now, we need to install the project requirements/dependencies.

### Requirements

This project depends on the following libraries:

- [Gemini GenAI](https://pypi.org/project/google-generativeai/) -> Gemini, now called Google GenerativeAI, is the core of this project. It analyzes candidates to generate worked examples for Software Engineering course classes.
- [Pandas](https://pandas.pydata.org/) -> Used primarily to read and write CSV files.
- [NumPy](https://numpy.org/) -> For handling numerical data efficiently.
- [Python dotenv Module](https://pypi.org/project/python-dotenv/) -> Used for loading environment variables from `.env` files, crucial for reading the Google GenerativeAI API Key.
- [Colorama](https://pypi.org/project/colorama/) -> For adding color and style to terminal outputs, enhancing the readability of command-line feedback.
- [Scikit-learn](https://scikit-learn.org/stable/) -> Utilized for text similarity assessments using TfidfVectorizer and cosine similarity metrics.
- [SciPy](https://scipy.org) -> For calculating statistics, particularly useful for generating confidence intervals.
- [Concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) -> For parallel execution of the Runs, improving the efficiency of processing tasks.
- [Threading](https://docs.python.org/3/library/threading.html) -> Used for concurrency control, particularly with the `Semaphore` object for limiting the number of threads.
- Standard Libraries:
    - [atexit](https://docs.python.org/3/library/atexit.html) -> For executing cleanup functions when the program terminates.
    - [os](https://docs.python.org/3/library/os.html) -> For interacting with the operating system, like running terminal commands.
    - [sys](https://docs.python.org/3/library/sys.html) -> For accessing system-specific parameters and functions, such as exiting the program.
    - [platform](https://docs.python.org/3/library/platform.html) -> For obtaining the name of the operating system.
    - [time](https://docs.python.org/3/library/time.html) -> For handling time-related tasks, like sleeping the program to implement the retry mechanism with exponential backoff.
    - [collections.Counter](https://docs.python.org/3/library/collections.html#collections.Counter) -> For counting hashable objects in an efficient way.

Futhermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** 
   
   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `Gemini`, `Numpy`, `Pandas`, and `Scikit-learn` will be installed.
This will also be handled by the `Makefile` during the dependencies installation process, so no command must be executed in order to create the virtual environment.

1. **Install Dependencies:** 
   
   Run the following command to set up the virtual environment and install all necessary dependencies on it:

    ```
    make dependencies
    ```

   This command performs the following actions:
  - Creates a new virtual environment by running `python3 -m venv venv`.
  - Installs the project's dependencies within the virtual environment using `pip` based on the `requirements.txt` file. The `requirements.txt` file contains a list of all required packages and their versions. This is the recommended way to manage dependencies in Python projects, as it allows for consistent and reproducible installations across different environments.

      If you need to manually activate the virtual environment, you can do so by running the following command:

      ```
      source venv/bin/activate
      ```

2. **Running Scripts:**
   
   The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `gemini.py` file, use:

   ```
   make gemini_script
   ```

   This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

3. **Generate the requirements.txt file:**

   If you changed the project dependencies and want to update the `requirements.txt` file, you can run the following command:

   ```
   make generate_requirements
   ```

   This command will generate the `requirements.txt` file in the root of the tool directory (`Gemini/`), which will contain all the dependencies used in the virtual environment of the project.

### Cleaning Up

To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:

```
make clean
```

This command removes the `venv` directory and deletes any cached Python files in the project directory, helping maintain a clean workspace.

By following these instructions, you'll ensure that all project dependencies are correctly managed and isolated, leading to a more stable and consistent development environment.
	
## How to use

In order to use the makefile rules, you must be in the `Gemini/` directory.

### gemini_script

This script is used to interact with the Google Gemini API in order to help analyze the good candidates in order to generate a worked example for the classes of Software Engineering courses. The input of this script are the ones generated by `PyDriller/code_metrics.py` and `PyDriller/metrics_changes.py`

#### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE` If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `RUNS` constant refers to the number of runs that the script will execute. This is set to 5 by default, and you are able to change it to any number you want, but be aware that the more runs you set, the more likely is for you to get blocked by the Google Generative AI API.
3. `CSV_INPUT_FILE` constant refers to the path of the CSV file that contains the data generated by the `PyDriller/code_metrics.py` and `PyDriller/metrics_changes.py` scripts. The data from that CSV will be passed at the end of the `start_message`, which gives the context for Gemini on what to do.
4. `DESIRED_HEADER` list constant refers to the desired header of the `CSV_INPUT_FILE` file that will be passed to the `start_message` at the end of the script, so Gemini ain't flooded with unnecessary data.
5. `start_message` string contains the message that will be passed to the Gemini API in order to analyze the good candidates to generate a worked example for the classes of Software Engineering courses.

#### Run

Now that you have set the constants, you can run the following command to execute the `gemini.py` file:

```
make gemini_script
```

#### Workflow

1. **Check for Whitespaces in Project Path:**
   - The script first verifies if there are any whitespaces in the project path. If there are, it will not proceed.

2. **Verify .env File:**
   - Calls `verify_env_file()` to ensure that the `.env` file exists and contains the `GEMINI_API_KEY`.
   - If the `.env` file or the key is missing, the script exits.

3. **Configure the Generative AI Model:**
   - Calls `configure_model()` to set up the Google Generative AI model using the API key obtained from the `.env` file.
   - Configures the model with specified parameters such as temperature, top_p, top_k, and max_output_tokens.

4. **Load and Filter CSV File:**
   - Calls `load_csv_file()` to read the CSV file located at `CSV_INPUT_FILE`.
   - Verifies the presence of required columns ("Class" and "Method Invocations") in the CSV file.
   - If the file or required columns are missing, the script exits.
   - Filters and converts the data to a string for further processing.

5. **Start Chat Session with Model:**
   - Prepares an initial message for the chat session explaining the format and content of the CSV data.
   - Calls `start_chat_session()` with the initial message to begin a chat session with the AI model.

6. **Perform Multiple Runs:**
   - Executes the process `RUNS` times to engage with the model using parallel execution, where each run starts a chat session and sends a message requesting the analysis of the provided CSV data.
   - Implements a retry mechanism with exponential backoff in case of server errors.
   - Each response is collected and the similarity between all responses is computed to assess consistency.

7. **Print and Save Outputs:**
   - Calls `print_output()` to print the AI model's response to the terminal.
   - Calls `write_output_to_file()` to save the AI model's response to the specified output file (`OUTPUT_FILE`).

8. **Compute Similarity Between Runs:**
   - After collecting outputs from multiple runs, calculates the similarity of outputs to assess the consistency using cosine similarity metrics.
   - Computes the average similarity and a 95% confidence interval for the similarity to provide a measure of the reliability of the responses.

9. **Play Sound on Completion:**
   - When the script finishes, it plays a notification sound to indicate completion, using the `play_sound()` function registered with `atexit`.

## Generated Data

The outputs of the scripts are stored in the `Gemini/Outputs/` directory, which are the following:

### Output  

The output of this Python script consists of multiple files according to the number of runs set in the `RUNS` constant. The `OUTPUT_FILE` contains the analysis generated by the Google Generative AI model based on the input data for the respective run. The `MOST_COMMON_OUTPUT_FILE` contains the most common output between the multiple runs. The content saved in the `OUTPUT_FILE` is also shown in the terminal if the `VERBOSE` constant is set to `True`.

Additionally, the script calculates the average similarity between the outputs of multiple runs and provides a 95% confidence interval for the similarity of the outputs generated by the Gemini model.

### Results and Discussion

The integration with Google Gemini API yielded consistent results across multiple runs. The program's execution with 5 runs generated outputs for each run, demonstrating the stability and reliability of the implemented solution.

| Metric                                            | Value     |
|---------------------------------------------------|-----------|
| Average Similarity between 5 Runs                | 0.83      |
| 95% Confidence Interval for the Gemini's Output  | (0.78, 0.88) |

Upon analyzing the outputs, the average similarity between the results of the five runs was found to be 0.83. This suggests a high level of consistency in the responses generated by the Gemini model across different iterations of the script. Additionally, a 95% confidence interval for the similarity of the outputs was calculated to be [0.78, 0.88], indicating a relatively narrow range and a high degree of confidence in the observed similarity.

The Gemini model was configured with specific parameters to control the output generation process. These parameters include:
- **Temperature:** Controls the randomness of the output, with values ranging from 0.0 to 1.0. A lower temperature results in more deterministic output, while a higher temperature introduces more randomness. We used a value of 0.1 to ensure coherent and contextually relevant responses, but improving this value actually didnt make any major difference in the similarity and confidence interval of the similarity.
- **Top P:** An optional parameter that sets the maximum cumulative probability of tokens to consider when sampling. This parameter helps in generating diverse and contextually relevant responses. We set the value to 0.95.
- **Top K:** Another optional parameter that limits the number of tokens to consider when sampling. It helps in constraining the model's output and avoiding overly repetitive or verbose responses. We set the value to 64.
- **Max Output Tokens:** Specifies the maximum number of tokens in the generated output, ensuring that the responses remain within a manageable length. We set the value to 8192 tokens, which is the maximum allowed by the Gemini API.

The input message provided to the Gemini model prompted it to analyze a CSV file located in `../PyDriller/metrics_statistics/zookeeper/substantial_CBO_classes_changes.csv` containing a list of good class candidates in terms of SE metrics (CBO, mainly) and Refactoring pPtterns detected overtime in the ZooKeeper repository. So, we filter this CSV to read the class name and terms extraded in the method invocations of the methods from that class (which is a feature added by me in the [CK repository](https://github.com/mauricioaniche/ck/pull/120)). So, Gemini is instructed to read those informations about class and method invocations in the context of Distributed Systems education to filter the good candidates to select the ones which are relevant to the educional topics of DS in order to create a worked example. The CSV was generated by `PyDriller/metrics_changes.py` and this message guided the model in understanding the task and generating relevant responses based on the provided data.

It's important to note that the outputs themselves are relatively large, averaging around 40 lines with approximately 500 words in total. So, a high similarity in a large output indicates that the model is consistently generating coherent and contextually relevant responses across multiple runs. The narrow confidence interval further strengthens the reliability of the observed similarity, suggesting that the outputs are highly consistent and reliable.

Overall, the consistency and high similarity observed in the outputs generated by the Gemini model reinforce its effectiveness in analyzing the provided data and generating coherent responses.

## Contributing

If you want to contribute to this project, please read the Contributing section of the [Main README](../README.md) file, as well as the [CONTRIBUTING](../CONTRIBUTING.md) file in this repository.

## License

This project is licensed under the [Apache License 2.0](../LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](../LICENSE) file in this repository.
