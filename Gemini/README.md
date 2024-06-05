<div align="center">

# [Google Gemini API.](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/tree/main/Gemini)  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the Google Gemini directory, in which you will find the script used to interact with the Google Gemini API in order to help analyze the good candidatessin order to generate a worked example for the classes of Software Engineering courses, as this is the main goals of this project.
 The scripts that are located in this directory are part of the [Worked-Example-Miner (WEM)](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) Tool.

---

</div>

- [Google Gemini API.  ](#google-gemini-api--)
  - [Important Notes](#important-notes)
  - [Setup](#setup)
    - [Python and Pip](#python-and-pip)
      - [Linux](#linux)
      - [MacOS](#macos)
      - [Windows](#windows)
    - [Requirements](#requirements)
    - [Cleaning Up](#cleaning-up)
  - [How to use](#how-to-use)
    - [Code\_Metrics](#code_metrics)
      - [Configuration](#configuration)
      - [Run](#run)
      - [Workflow](#workflow)
  - [Generated Data](#generated-data)
    - [CK Metrics](#ck-metrics)
  - [Contributing](#contributing)
  - [License](#license)

## Important Notes

- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- To enhance the readability of the code, please note that the files adhere to a Bottom-Up approach in function ordering. This means that each function is defined above the function that calls it.
- All of the Scripts have a `Makefile`that handles virtual environment creation, dependencies installation and script execution. You can run the scripts by using the `make` command, as shown in the `How to use` section.
- All of the Scripts usually output an estimated time of the script execution, based on things like the number of commits of the repository, the number of classes or methods to be analyzed, etc. But this is just an estimate, the actual time does vary a lot depending on the machine you're using, on what is running on the machine, and many other factors.
- The execution of this scripts will take a long time and store a lot of data, so make sure you have enough space in your disk and be patient. Example: Running all the scrips only for `Apache Kafka` generates a total of 115 GB of data.
- Why is `metrics_changes.py` isn't fully parallelized? Because, for example, for running for `Apache Kafka` it uses so much CPU and RAM that it crashed in my Ryzen 7 3800X with 32GB of RAM and there is also a lot of I/O to the disk. I tried creating a thread for process each repository, just like i did for `code_metrics.py`, but most of the times it just crashes after a minute running. Talking about the `code_metrics.py`, the most performance i could take from it was, as said, to create a thread to process each repository, therefore it isn't possible to parallelize inside the processing of the repository, as the result of the iteration number `x` depends on the result since the `first iteration until x-1`. If you want to parallelize something in order to improve performance, feel free to do it, i'll be glad aproving your pull request. Also, if the `code_metrics.py` crashes in the middle of the execution, you can just run it again, as it will verify if the ck metrics are already calculated and where it stopped, so it will continue from where it stopped.

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

- [Git](https://git-scm.com/) -> Git is used to clone the repositories and do operations in the repositories, such as switching branches, so it is a critical dependency for the code execution. As the installation process varies depending on the operating system, please refer to the official Git documentation for detailed instructions on how to install it on your machine. You can probably install it using the package manager of your operating system, like `sudo apt install git -y` in Linux, `brew install git` in MacOS and `choco install git` in Windows.
- [Gemini](https://Gemini.readthedocs.io/en/latest/) -> Gemini is the core of this project, as it is used to traverse the commits tree of the repositories and get many informations about it, like the commit hash, commit message, commit date and many other things.
- [MatPlotLib](https://matplotlib.org/) -> MatPlotLib is used to generate the graphics of the metrics evolution and the linear prediction.
- [NumPy](https://numpy.org/) -> NumPy is used to generate the linear prediction of the linear regression and to many operations in the list of the metrics.
- [Pandas](https://pandas.pydata.org/) -> Pandas is used maintly to read and write the csv files.
- [SciKit-Learn](https://scikit-learn.org/stable/) -> SciKit-Learn is used to generate the linear prediction of the linear regression.
- [TQDM](https://tqdm.github.io/) -> TQDM is used to show the progress bar of the scripts.

Futhermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** 
   
   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `matplotlib`, `numpy`, `pandas`, `Gemini`, `scikit-learn` and `tqdm`, will be installed.
This will also be handled by the `Makefile` during the dependencies installation process, so no command must be executed in order to create the virtual environment.

2. **Install Dependencies:** 
   
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

1. **Running Scripts:**
   
   The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `code_metrics.py` file, use:

   ```
   make code_metrics_script
   ```

   This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

2. **Generate the requirements.txt file:**

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

### Code_Metrics

This script is used to generate the ck metrics, commit diff files and commit hashes list of the repositories specified in the `DEFAULT_REPOSITORIES` dictionary. It is really usefull to generate the data that will be used in the `metrics_changes.py` script.

#### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `DEFAULT_REPOSITORIES` dictionary in the `code_metrics.py` file, in which you must specify the repository name and the repository url. As this and the `metrics_changes.py` python files, they are responsible for generating the data and metadata of this tool, so, in a first run, select a very small Java repository just to see how it works and get a good idea of the data generated by the tool. As a suggestion, define the constant as follows:
   
   ```python
   DEFAULT_REPOSITORIES = {"MacOS-Calculator-Clone": "https://github.com/muhammadbadrul1234/MacOS-Calculator-Clone"}
   ```

   The repository example above is a small repository that contains only 1 java file and only 9 commits, so it is a good example to see how the tool works.

   After that, you can select the repositories that you want to generate the data and metadata. The `DEFAULT_REPOSITORIES` dictionary is a dictionary in which the key is the repository name and the value is the repository url. For example, if you want to generate the data and metadata of the `zookeeper` repository, you must add the following key-value pair to the `DEFAULT_REPOSITORIES` dictionary.

#### Run

Now that you have set the constants, you can run the following command to execute the `code_metrics.py` file:

```
make code_metrics_script
```

#### Workflow

1. As for every file in this project, the first thing it will do is verify if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. Now, the main function will call the `verify_git()` function, which will verify if the `git` command is installed in your machine. If it isn't, it will stop the code execution. The `git` command is used to clone the repositories and do operations in the repositories, such as switching branches, so it is a critical dependency for the code execution.
3. Next, the main function ensures that the `ck` jar file is present in the `FULL_CK_JAR_PATH` directory. This verification is critical for the execution of the CK metrics. The process unfolds as follows:

   1. Initially, the script checks for the existence of the `ck` jar file at the specified `RELATIVE_CK_JAR_PATH`. If the file is not found, the script proceeds to invoke `ensure_ck_jar_exists()`, which is tasked with verifying and potentially rectifying the absence of the `ck` jar file. So, at first, it verifies the `ck` submodule's presence and updates it if necessary by calling `init_and_update_submodules()`.
   2. In this step, the `CK` repository branch might be needed to be switched to the branch defined in the `CK_BRANCH` constant. This is done by calling the `switch_ck_branch()` function. If the branch is already the one defined in the `CK_BRANCH` constant, the script proceeds to the next step, otherwise it switches to the branch defined in the `standard_branch` variable, which is the `master` branch.
   3. After that, if the `ck` jar is still missing, `ensure_ck_jar_exists()` proceeds with the build process. It executes a `mvn clean package -DskipTests` command within the CK directory, aiming to compile the necessary source into a runnable jar. This step is critical for ensuring that all tools required for metrics calculation are readily available and also avoids us storing the jar file (compiled code) in the repository.

   If the `ck` jar file was successfully compiled or was already present, the script proceeds to the next step. Otherwise, it outputs an error message and exits the program.
4. Now, it calls `process_repositories_in_parallel()` which will create a thread for each of the repositories inside the `DEFAULT_REPOSITORIES` dictionary and process it's ck metrics and save each commit file diff. Each thread has as it's target the `process_repository(repository_name, repository_url)` function.
5. Inside the `process_repository(repository_name, repository_url)` function, the `verify_ck_metrics_folder(repository_name)` function is called to verify if the ck metrics are already calculated. That verification is done by:
   
   1. Verifying if the repository commits list csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commits_list.csv`, for example: `zookeeper-commits_list.csv`;
   2. If the csv file exists, it will, for every commit hash in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant;  
   
   If any of those verifications are false, it stops executing, due to the fact that the ck metrics weren't calculated. If not, it will continue executing until the end and return true, meaning that the ck metrics are already calculated.

6. Now, as the ck metrics are not calculated, it will call `create_directory(absolute path, relative_path)` three times: for the `FULL_CK_METRICS_DIRECTORY_PATH`, `FULL_PROGRESS_DIRECTORY_PATH`, and `FULL_REPOSITORIES_DIRECTORY_PATH`, respectively. This function is used to create the output directories for the ck metrics, progress and repositories.
7.  With all the subfolders created, we must call `clone_repository(repository_name, repository_url)` function, which will clone the repository to the `FULL_REPOSITORY_DIRECTORY_PATH` directory.
8. In this step, we must calculate the number of commit in the current repository in order to be able to call the `traverse_repository(repository_name, repository_url, number_of_commits)` function.
9. As now we have the repository cloned, we must call `traverse_repository` function. In this function, we call the `get_last_execution_progress(repository_name, saved_progress_file, number_of_commits)` function, as it will read the progress file and return the commits_info and last commit hash that was processed. With that information, the loop for traversing the repository commit tree, we can jump to where the last execution stopped and resume the execution.
10. With that in mind, we use the `Gemini` library to traverse the repository commits tree with the use of `Gemini.traverse_commits()` to go through all the commit hashes of the repository and do the following for each commit in the repository: 
    
   1. Get the tuple containing the `commit.hash`, `commit.msg` and `commit.committer_date` and append those commit's data in the `commits_info` list, in order to, later on, store them inside the `CK_METRICS_DIRECTORY_PATH/repository_name-commit_hashes.csv` file;  
   2. Call `generate_diffs(repository_name, commit, commit_number)`, which will fo through all the modified files of the current commit and store the diffs of the files in the `{START_PATH}{RELATIVE_DIFFS_DIRECTORY_PATH}/{repository_name}/{commit_number}-{commit.hash}/` directory;
   3. Now it must change the working directory to the `{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}` directory.
   4. Checkout to the `commit.hash` branch;  
   5. Create a subfolder inside the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name` named as `commit_number-commit.hash`;  
   6. Now it changes the working directory again to the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name/commit_number-commit.hash` directory, which is the output for the execution of the `ck` command for the current `commit.hash`;
   7. Lastly, with the call of the `run_ck_metrics_generator(cmd)` to execute the `cmd` command, which is a command defined to run ck for the current commit.hash and store the files that it generates in the `FULL_CK_METRICS_DIRECTORY_PATH/repository_name/commit_number-commit.hash` directory;
    
11. Now that we have the list of tuples containing the commit hashes, commit message and commit date for each commit, we must store those values in the `CK_METRICS_DIRECTORY_PATH/repository_name-commits_list.csv` file by calling the `write_commits_information_to_csv` function.
12. And lastly, we must call `checkout_branch` function passing the `main` branch as parameter, in order to return to the main branch of the repository.
13. After everything is done, the `code_metrics.py` script will be done and play a sound to notify you that the script has finished.

## Generated Data

The outputs (generated data and metadata) of the scripts are stored in the `Gemini/` directory, which are the following:

### CK Metrics  

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
