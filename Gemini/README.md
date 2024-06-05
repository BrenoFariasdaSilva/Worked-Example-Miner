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

- [Gemini GenAI](https://pypi.org/project/google-generativeai/) -> Gemini is the core of this project. It analyzes good candidates to generate worked examples for Software Engineering course classes.
- [Pandas](https://pandas.pydata.org/) -> Pandas is used primarily to read and write CSV files.
- [Python dotenv Module](https://pypi.org/project/python-dotenv/) -> The dotenv module is used for loading environment variables from .env files in order to read the Google Gemini API Key.

Futhermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** 
   
   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `dotEnv`, `Gemini` and `pandas` will be installed.
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
   
   The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `gemini_script.py` file, use:

   ```
   make gemini_script
   ```

   This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

3. **Generate the requirements.txt file:**

   If you changed the project dependencies and want to update the `requirements.txt` file, you can run the following command:

   ```
   make generate_requirements
   ```

   This command will generate the `requirements.txt` file in the root of the tool directory (Gemini or RefactoringMiner), which will contain all the dependencies used in the virtual environment of the project.

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

1. `CSV_INPUT_FILE` constant refers to the path of the CSV file that contains the data generated by the `PyDriller/code_metrics.py` and `PyDriller/metrics_changes.py` scripts. The data from that CSV will be passed at the end of the `start_message`, which gives the context for Gemini on what to do.
2. `DESIRED_HEADER` list constant refers to the desired header of the `CSV_INPUT_FILE` file that will be passed to the `start_message` at the end of the script, so Gemini ain't flooded with unnecessary data.
3. `start_message` string contains the message that will be passed to the Gemini API in order to analyze the good candidates to generate a worked example for the classes of Software Engineering courses.

#### Run

Now that you have set the constants, you can run the following command to execute the `gemini_script.py` file:

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

6. **Send Message for Analysis:**
   - Calls `send_message()` to send a follow-up message asking the model to analyze the provided CSV data.
   - Receives the AI model's analysis as output.

7. **Print Output:**
   - Calls `print_output()` to print the AI model's response to the terminal.

8. **Write Output to File:**
   - Calls `write_output_to_file()` to save the AI model's response to the specified output file (`OUTPUT_FILE`).

9. **Play Sound on Completion:**
   - When the script finishes, it plays a notification sound to indicate completion, using the `play_sound()` function registered with `atexit`.

## Generated Data

The output of the scripts are stored in the `Gemini/` directory, which are the following:

### Output  

   This directory contains the ck metrics for each commit of the repositories, which are stored in the `./ck_metrics/repository_name/commit_number-commit_hash` directory. Each `commit_number-commit_hash` directory contains the `class.csv` and `method.csv` files, which contains the ck metrics of the classes and methods of the repository for the specified commit hash. The `ck_metrics` directory also contains the `repository_name-commits_list.csv` file, which contains the list of the commit hashes, commit messages and commit dates of the repository.

   The CSV header of the `class.csv` and `method.csv` files are the following:

   ```csv
   | file | class | class | cbo | cbo modified | fanin | fanout | wmc | dit | noc | rfc | lcom | lcom* | tcc | lcc | totalMethodsQty | staticMethodsQty | publicMethodsQty | privateMethodsQty | protectedMethodsQty | defaultMethodsQty | visibleMethodsQty | abstractMethodsQty | finalMethodsQty | synchronizedMethodsQty | totalFieldsQty | staticFieldsQty | publicFieldsQty | privateFieldsQty | protectedFieldsQty | defaultFieldsQty | finalFieldsQty | synchronizedFieldsQty | nosi | loc | returnQty | loopQty | comparisonsQty | tryCatchQty | parenthesizedExpsQty | stringLiteralsQty | numbersQty | assignmentsQty | mathOperationsQty | variablesQty | maxNestedBlocksQty | anonymousClassesQty | innerClassesQty | lambdasQty | uniqueWordsQty | modifiers | logStatementsQty |
   ```

   That's a visual representation of the CSV header of the `class.csv` and `method.csv` files, which contains the ck metrics of the classes and methods of the repository for the specified commit hash. The lines that comes below the CSV header are the values of the metrics for each class or method of the repository in that current commit hash.

   The main difference from the `class.csv` and `method.csv` files is that the third attribute in the csv header is the `method name` in the `method.csv` file and the `class type` in the `class.csv` file.

   The CSV header of the `repository_name-commits_list.csv` file is the following:

   ```csv
   | Commit Hash | Commit Message | Commit Date |
   ```

   That's a visual representation of the CSV header of the `repository_name-commits_list.csv` file, which contains the list of the commit hashes, commit messages and commit dates of the repository. The lines that comes below the CSV header are the values of the commit hashes, commit messages and commit dates of the repository for each commit.

## Contributing

If you want to contribute to this project, please read the Contributing section of the [Main README](../README.md) file, as well as the [CONTRIBUTING](../CONTRIBUTING.md) file in this repository.

## License

This project is licensed under the [Apache License 2.0](../LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](../LICENSE) file in this repository.
