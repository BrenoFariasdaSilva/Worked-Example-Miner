<div align="center">

# [PyDriller.](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/tree/main/PyDriller)  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the PyDriller directory, in which you will find the scripts used to generate the ck metrics, commit diff files, commit hashes list, metrics changes, metrics evolution, metrics statistics and linear regressions of the Java Open-Source Repositories of interest. The scripts that are located in this directory are part of the [Worked-Example-Miner (WEM)](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) Tool.

---

</div>

- [PyDriller.  ](#pydriller--)
  - [Important Notes](#important-notes)
  - [Setup](#setup)
    - [Python and Pip](#python-and-pip)
      - [Linux](#linux)
      - [MacOS](#macos)
      - [Windows](#windows)
    - [Requirements](#requirements)
    - [Cleaning Up](#cleaning-up)
  - [How to use](#how-to-use)
    - [Main Scripts](#main-scripts)
      - [Code\_Metrics](#code_metrics)
        - [Configuration](#configuration)
        - [Run](#run)
        - [Workflow](#workflow)
      - [Metrics\_Changes](#metrics_changes)
        - [Configuration](#configuration-1)
        - [Run](#run-1)
        - [Workflow](#workflow-1)
    - [Auxiliar Scripts](#auxiliar-scripts)
      - [Empty Folders](#empty-folders)
        - [Configuration](#configuration-2)
        - [Run](#run-2)
        - [Workflow](#workflow-2)
      - [Extract Zip Files](#extract-zip-files)
        - [Configuration](#configuration-3)
        - [Run](#run-3)
        - [Workflow](#workflow-3)
      - [Generate Short Zip Files](#generate-short-zip-files)
        - [Configuration](#configuration-4)
        - [Run](#run-4)
        - [Workflow](#workflow-4)
      - [Generate Zip Files](#generate-zip-files)
        - [Configuration](#configuration-5)
        - [Run](#run-5)
        - [Workflow](#workflow-5)
      - [Move Extracted Files](#move-extracted-files)
        - [Run](#run-6)
        - [Workflow](#workflow-6)
      - [Track Files](#track-files)
        - [Configuration](#configuration-6)
        - [Run](#run-7)
        - [Workflow](#workflow-7)
  - [Generated Data](#generated-data)
    - [CK Metrics](#ck-metrics)
    - [Commit Diff Files](#commit-diff-files)
    - [Metrics Data](#metrics-data)
    - [Metrics Evolution](#metrics-evolution)
    - [Metrics Predictions](#metrics-predictions)
    - [Metrics Statistics](#metrics-statistics)
    - [Progress Files](#progress-files)
    - [Refactorings Files](#refactorings-files)
    - [Repositories Files](#repositories-files)
  - [Contributing](#contributing)
  - [License](#license)

## Important Notes

- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- All of the Scripts have a `Makefile`that handles virtual environment creation, dependencies installation and script execution. You can run the scripts by using the `make` command, as shown in the `How to use` section.
- All of the Scripts usually output an estimated time of the script execution, based on things like the number of commits of the repository, the number of classes or methods to be analyzed, etc. But this is just an estimate, the actual time does vary a lot depending on the machine you're using, on what is running on the machine, and many other factors.
- The execution of this scripts will take a long time and store a lot of data, so make sure you have enough space in your disk and be patient. Example: Running all the scrips only for `Apache Kafka` generates a total of 115 GB of data.
- Why is `metrics_changes.py` not parallelized? Because, for example, for running for `Apache Kafka` it uses so much CPU and RAM that it crashed in my Ryzen 7 3800X with 32GB of RAM and there is also a lot of I/O to the disk. I tried creating a thread for process each repository, just like i did for `code_metrics.py`, but most of the times it just crashes after a minute running. Talking about the `code_metrics.py`, the most performance i could take from it was, as said, to create a thread to process each repository, therefore it isn't possible to parallelize inside the processing of the repository, as the result of the iteration number `x` depends on the result since the `first iteration until x-1`. If you want to parallelize something in order to improve performance, feel free to do it, i'll be glad aproving your pull request. Also, if the `code_metrics.py` crashes in the middle of the execution, you can just run it again, as it will verify if the ck metrics are already calculated and where it stopped, so it will continue from where it stopped.

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

- [PyDriller](https://pydriller.readthedocs.io/en/latest/) -> PyDriller is the core of this project, as it is used to traverse the commits tree of the repositories and get many informations about it, like the commit hash, commit message, commit date and many other things.
- [MatPlotLib](https://matplotlib.org/) -> MatPlotLib is used to generate the graphics of the metrics evolution and the linear prediction.
- [NumPy](https://numpy.org/) -> NumPy is used to generate the linear prediction of the linear regression and to many operations in the list of the metrics.
- [Pandas](https://pandas.pydata.org/) -> Pandas is used maintly to read and write the csv files.
- [SciKit-Learn](https://scikit-learn.org/stable/) -> SciKit-Learn is used to generate the linear prediction of the linear regression.
- [TQDM](https://tqdm.github.io/) -> TQDM is used to show the progress bar of the scripts.

Futhermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** 
   
   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `matplotlib`, `numpy`, `pandas`, `pydriller`, `scikit-learn` and `tqdm`, will be installed.
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

   This command will generate the `requirements.txt` file in the root of the tool directory (PyDriller or RefactoringMiner), which will contain all the dependencies used in the virtual environment of the project.

### Cleaning Up

To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:

```
make clean
```

This command removes the `venv` directory and deletes any cached Python files in the project directory, helping maintain a clean workspace.

By following these instructions, you'll ensure that all project dependencies are correctly managed and isolated, leading to a more stable and consistent development environment.
	
## How to use 

### Main Scripts

In order to use the makefile rules, you must be in the `PyDriller/` directory.

#### Code_Metrics

This script is used to generate the ck metrics, commit diff files and commit hashes list of the repositories specified in the `DEFAULT_REPOSITORIES` dictionary. It is really usefull to generate the data that will be used in the `metrics_changes.py` script.

##### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `DEFAULT_REPOSITORIES` dictionary in the `code_metrics.py` file, in which you must specify the repository name and the repository url. As this and the `metrics_changes.py` python files, they are responsible for generating the data and metadata of this tool, so, in a first run, select a very small Java repository just to see how it works and get a good idea of the data generated by the tool. As a suggestion, define the constant as follows:
   
   ```python
   DEFAULT_REPOSITORIES = {"MacOS-Calculator-Clone": "https://github.com/muhammadbadrul1234/MacOS-Calculator-Clone"}
   ```

   The repository example above is a small repository that contains only 1 java file and only 9 commits, so it is a good example to see how the tool works.

   After that, you can select the repositories that you want to generate the data and metadata. The `DEFAULT_REPOSITORIES` dictionary is a dictionary in which the key is the repository name and the value is the repository url. For example, if you want to generate the data and metadata of the `zookeeper` repository, you must add the following key-value pair to the `DEFAULT_REPOSITORIES` dictionary.

##### Run

Now that you have set the constants, you can run the following command to execute the `code_metrics.py` file:

```
make code_metrics_script
```

##### Workflow

1. As for every file in this project, the first thing it will do is verify if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. Next, the main function ensures that the `ck` jar file is present in the `FULL_CK_JAR_PATH` directory. This verification is critical for the execution of the CK metrics. The process unfolds as follows:

   - Initially, the script checks for the existence of the `ck` jar file at the specified `RELATIVE_CK_JAR_PATH`. If the file is not found, the script proceeds to invoke `ensure_ck_jar_exists()`, which is tasked with verifying and potentially rectifying the absence of the `ck` jar file. So, at first, it verifies the `ck` submodule's presence and updates it if necessary by calling `init_and_update_submodules()`.
   - After that, if the `ck` jar is still missing, `ensure_ck_jar_exists()` proceeds with the build process. It executes a `make package` command within the CK directory, aiming to compile the necessary source into a runnable jar. This step is critical for ensuring that all tools required for metrics calculation are readily available and also avoids us storing the jar file (compiled code) in the repository.

   If the `ck` jar file was successfully compiled or was already present, the script proceeds to the next step. Otherwise, it outputs an error message and exits the program.
3. Now, it calls `process_repositories_in_parallel()` which will create a thread for each of the repositories inside the `DEFAULT_REPOSITORIES` dictionary and process it's ck metrics and save each commit file diff. Each thread has as it's target the `process_repository(repository_name, repository_url)` function.
4. Inside the `process_repository(repository_name, repository_url)` function, the `verify_ck_metrics_folder(repository_name)` function is called to verify if the ck metrics are already calculated. That verification is done by:
   
   1. Verifying if the repository commits list csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commits_list.csv`, for example: `zookeeper-commits_list.csv`;
   2. If the csv file exists, it will, for every commit hash in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant;  
   
   If any of those verifications are false, it stops executing, due to the fact that the ck metrics weren't calculated. If not, it will continue executing until the end and return true, meaning that the ck metrics are already calculated.

5. Now, as the ck metrics are not calculated, it will call `create_directory(absolute path, relative_path)` three times: for the `FULL_CK_METRICS_DIRECTORY_PATH`, `FULL_PROGRESS_DIRECTORY_PATH`, and `FULL_REPOSITORIES_DIRECTORY_PATH`, respectively. This function is used to create the output directories for the ck metrics, progress and repositories.
6.  With all the subfolders created, we must call `clone_repository(repository_name, repository_url)` function, which will clone the repository to the `FULL_REPOSITORY_DIRECTORY_PATH` directory.
7. In this step, we must calculate the number of commit in the current repository in order to be able to call the `traverse_repository(repository_name, repository_url, number_of_commits)` function.
8. As now we have the repository cloned, we must call `traverse_repository` function. In this function, we call the `get_last_execution_progress(repository_name, saved_progress_file, number_of_commits)` function, as it will read the progress file and return the commits_info and last commit hash that was processed. With that information, the loop for traversing the repository commit tree, we can jump to where the last execution stopped and resume the execution.
9.  With that in mind, we use the `PyDriller` library to traverse the repository commits tree with the use of `PyDriller.traverse_commits()` to go through all the commit hashes of the repository and do the following for each commit in the repository: 
    
   1. Get the tuple containing the `commit.hash`, `commit.msg` and `commit.committer_date` and append those commit's data in the `commits_info` list, in order to, later on, store them inside the `CK_METRICS_DIRECTORY_PATH/repository_name-commit_hashes.csv` file;  
   2. Call `generate_diffs(repository_name, commit, commit_number)`, which will fo through all the modified files of the current commit and store the diffs of the files in the `{START_PATH}{RELATIVE_DIFFS_DIRECTORY_PATH}/{repository_name}/{commit_number}-{commit.hash}/` directory;
   3. Now it must change the working directory to the `{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}` directory.
   4. Checkout to the `commit.hash` branch;  
   5. Create a subfolder inside the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name` named as `commit_number-commit.hash`;  
   6. Now it changes the working directory again to the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name/commit_number-commit.hash` directory, which is the output for the execution of the `ck` command for the current `commit.hash`;
   7. Lastly, with the call of the `run_ck_metrics_generator(cmd)` to execute the `cmd` command, which is a command defined to run ck for the current commit.hash and store the files that it generates in the `FULL_CK_METRICS_DIRECTORY_PATH/repository_name/commit_number-commit.hash` directory;
    
10. Now that we have the list of tuples containing the commit hashes, commit message and commit date for each commit, we must store those values in the `CK_METRICS_DIRECTORY_PATH/repository_name-commits_list.csv` file by calling the `write_commits_information_to_csv` function.
11. And lastly, we must call `checkout_branch` function passing the `main` branch as parameter, in order to return to the main branch of the repository.
12. After everything is done, the `code_metrics.py` script will be done and play a sound to notify you that the script has finished.

#### Metrics_Changes

This script is used to generate the metrics evolution, and metrics statistics and linear regressions of the repositories specified in the `DEFAULT_REPOSITORIES` dictionary. It is really usefull to analyze the changes of the metrics of the classes and methods of the repositories over time in order to select the classes and methods that had a substantial changes. Those changes can be related to changes in the software design, which can be related to refactorings, bugs, performance improvements and many other things. This data and metadas can be used for selecting good candidates in order to generate a worked example for the classes of Software Engineering courses, as this is the main goals of this project.

##### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE`: This is imported from the `code_metrics.py`file, in which you must specify if you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `DEFAULT_REPOSITORIES`: This is imported from the `code_metrics.py`file, in which you must specify the repository name and the repository url.
3. `MINIMUM_CHANGES`: This constant is used to specify the minimum number of changes that a class or method must have in order to be processed. If the class or method didn't have at least `MINIMUM_CHANGES` changes, it will not be processed.
4. `NUMBER_OF_METRIC`: This constant is used to specify the number of CK metrics that will be processed, in that case, it is set to 3 as we're using the `cbo`, `wmc` and `rfc` ck metrics.
5. `DESIRED_DECREASE`: This constant is used to specify the desired percentual of decrease of the metrics values in order to be considered a substantial change.
6. `IGNORE_CLASS_NAME_KEYWORDS`: This constant is used to specify the keywords that might be found in the class name that will be ignored in the substantial change verification. For example, if you want to ignore the classes that have the `Test` keyword in the class name, you must add it to the `IGNORE_CLASS_NAME_KEYWORDS` constant.
7. `IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS`: This constant is used to specify the keywords that might be found in the variable attribute that will be ignored in the substantial change verification. For example, if you want to ignore the classes of an specific type, like `anonymous`, `class`, `innerclasse`, `enum`, `interface`, `abstract`, you must add it to the `IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS` list.
8. `SUBSTANTIAL_CHANGE_METRIC`: This constant is used to specify the metric that will be used to verify if the current metrics values of the current class or method had a substantial decrease. In that case, it is set to `CBO`, which is the metric that can indicate the level of complexity of a class or method.
9. `METRICS_POSITION`: This constant is used to specify the position of each used metric in the `metrics` list, which is used to generate the linear prediction of the linear regression. In that case, it is set to `0` for `CBO`, `1` for `WMC` and `2` for `RFC`.
10. `DESIRED_REFACTORINGS_ONLY`: This constant is used to specify if you want to store only the substantial changes that are of any of the specified refactorings in the `DESIRED_REFACTORINGS` list. If you want to store all the substantial changes, you must set it to `False`.
11. `DESIRED_REFACTORINGS`: This constant is used to specify the desired refactorings that you want to store in the `substantial_changes.csv` file. If you want to store all the substantial changes of any type, you must set the `DESIRED_REFACTORINGS_ONLY` constant to `False`.

##### Run

Considering that you now have the ck metrics calculated and the constants set, you are able to run the following command to execute the `metrics_changes.py` file:

```
make metrics_changes_script
```

##### Workflow

1. The first thing it will do is ask you if you want to process classes or methods, if you want to process classes, type ```True```, if you want to process methods, type ```False```. Note that it is case sensitive, so make sure you type it correctly.
2. The second thing it will do is verify if you don't have whitespaces in the path of the project by calling the `path_contains_whitespaces` function. If you have, it will not work.
3. Now, it will verify if the `RefactoringMiner` bin file exists in the `FULL_REFACTORING_MINER_PATH` directory. If it doesn't exist, it will stop the code execution.
4. Here, the main function will call the `update_global_variables()`, which basically asks for the user input if he wants to process the classes or methods of the repositories, and, if he wants to process the classes, it will set the `CLASSES_OR_METHODS` constant to `classes`, if he wants to process the methods, it will set the `CLASSES_OR_METHODS` constant to `methods`.
5. Next, it will call the `process_all_repositories()` function, which will loop through the `DEFAULT_REPOSITORIES` dictionary and call the `process_repository(repository_name)` function for each repository name.
6. In this step, the `process_repository` function will call the `verify_ck_metrics_folder(repository_name)` function imported from `code_metrics.py`, as the code must verify if you have already executed the `code_metrics.py` file. If they aren't, it will tell you to run the `code_metrics.py` file, which will generate the ck metrics. This verification is done by:
   
   1. Verifying if the repository commit hash csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commits_list.csv`, for example: `zookeeper-commits_list.csv`. If it doesn't exist, it will return false;  
   2. If the csv file exists, it will, for every commit hash, which is inside the `commit hash` column in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as the value in the current `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant. If it doesn't exist, it will return false;

   If any of those verifications are false, it stops executing, due to the fact that the ck metrics weren't calculated. If not, it will continue executing until the end and return true, meaning that the ck metrics are already calculated.

7. Now it will call the `get_directory_path` for the current repository name, as it return the path for the ck files of that repository. With that, it can call the `create_directories` to create the `RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH` output directory, which will be, later on, be used to store the `metrics evolution`, `metrics_predictions` and`metrics statistics`.
8. With the output directories created, we get into the most important step, in which the `traverse_directory` will be executed and will do the following: 
   
   1. This function will call the `generate_commit_modified_files_dict(repository_name)` function, which return a dictionary where the keys are the commit hashes and the values are the list of modified files paths of the current commit. With that dictionary, later on, we'll be able to validate if the file associated to a metric change in the ck csv file was actually modified in the commit.
   2. Now, it lops throught every subfolder inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, where each subfolder should contain the `class.csv` and `method.csv` files, For each subfolder path, it calls the `process_csv_file` function, giving it the `commit_modified_files_dict` dictionary, the `file_path` string and `metrics_track_record` dictionary. With that in mind, the `process_csv_file` does the following:
   
      1. It will open file and get the values of the desired columns for each row. Each row is processed by calling the `get_identifier_and_metrics(row)` function, which return the informations of interest, that is, the `class`, the variable attribute, which could be the `type` or the `method` values, depending if it is the classes or methods to be processed. Also, it gets the values in the `cbo`, `wmc`, `rfc` metrics, as well as a counter of the number of times(occurrences) a class was referentiated or a method was invoked, which are metrics generated by ck. The counter originally wasn't included in the `ck` repository, so i made an effort to fix the broken build and add this new metric. For that three metrics, it creates a tuple to store them and create a identifier, being the combination of the `class_name` and the `variable attribute`;  
      2. Now, it verifies if that identifier is not already in the `metrics_track_record` dictionary. If not, in the `identifier` position of the dictionary, it starts two fields, the `metrics` list and the `changed` value, in which stores the number of times that the tuple (containing the combination of the cbo, wmc and rfc) changes, and lastly, the number of occurrences in the `occurrences` field. 
      3. Now it gets the metrics values list in the identifier position of the dictionary and verify if the current metrics combination aren't inside that metrics values list. If it ain't, it means that those metrics combination haven't appeared yet, so we can add it to the list and increment the value of times that this class or method changed. If they are in, we won't add them to the list, as those values would be repeated;  Also, in that verification, it will verify if the file associated to the metrics change was actually modified in the commit, if it wasn't, it will not add the metrics values to the list, as it would be a false positive (a change in the metrics values that wasn't related to a change in the code).
     
   Now that the `metrics_track_record` dictionary is filled with the metrics evolution of every class or method, the `traverse_directory` function will return the `metrics_track_record` dictionary, in order for the metrics be processed to generate statistics.

9. In this step, we must sort the `metrics_track_record` dictionary by the `commit_number`, which indicates the order of the commits. This is done by calling the `sort_commit_hashes_by_commit_number` function. 
10. Now its time to write those `sorted_metrics_track_record` to the `metrics_data` directory with the call of the `write_metrics_track_record_to_txt` function.  This function will basically write the values of the `sorted_metrics_track_record` dictionary to the `{FULL_METRICS_DATA_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}__track_record.txt` file. This file ain't much useful, but it tries to write the values of the `sorted_metrics_track_record` dictionary in a more human readable way, so it can be used to better understand the complex structure of the `sorted_metrics_track_record` dictionary.
11. In this step, we must call the `write_metrics_evolution_to_csv` function. This function will, for each class or method in the repository, write it's values inside the `sorted_metrics_track_record` dictionary to the `{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}` csv file and, at the end of each iteration, it writes the `identifier`, `commit hash`, `occurrences`, and the tree metrics (cbo, wmc and rc) to the metrics evolution file, as well as call the `linear_regression_graphics(metrics, class_name, variable_attribute, repository_name)` function to generate the linear regression graphics for that same class or method. The `linear_regression_graphics` function does the following:
    
    1.  It verifies if the metrics list ain't empty, if it is, it will not generate the linear regression graphics.
    2.  Then, it verifies if the values inside the metrics list are valid, that is, if they aren't `NaN` or `Infinity`. If they are, it will not generate the linear regression graphics.
    3.  Now, it loops through the `metrics` list and, for each metric, it will generate the linear regression graphics and store it in the `{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}` csv file. In this step, many other important things are done, such as:

        1. Call the `verify_substantial_metric_decrease` function for the specified metric name in the `SUBSTANTIAL_CHANGE_METRIC` constant, which will verify if the current metrics values of the current class or method had a substantial decrease, defined in the `DESIRED_DECREASED` constant. There are restrictions, for example, keywords that might be found in the class name or variable attribute; If it had any decrease equal or higher than the `DESIRED_DECREASED`.
        2. Get the `Refactorings Information` (`Refactorings Types` and `File Path`), which are generated by calling the `get_refactorings_info` function, which runs the `RefactoringMiner` bin file for an specific commit hash and class name and store the refactorings types and file paths in a dictionary named `refactorings_info`. If the `DESIRED_REFACTORINGS_ONLY` constant is set to `True`, it will only store the substantial changes that are of any of the specified refactorings in the `DESIRED_REFACTORINGS` list. If you want to store all the substantial changes, you must set the `DESIRED_REFACTORINGS_ONLY` constant to `False`.

      If the `DESIRED_REFACTORINGS_ONLY` constant is set to `True`, it will only store the substantial changes that are of any of the specified refactorings in the `DESIRED_REFACTORINGS` list. If you want to store all the substantial changes, you must set the `DESIRED_REFACTORINGS_ONLY` constant to `False`. 
      Those information will be saved in a csv file containing the `class_name`, `variable_attribute`, `From metric_value`, `To metric_value`, `Percentual Variation`, `Occurrences`, `Commit Number`, `Commit Hash`, `Refactorings Types` and `File Path` informations. The csv file is stored in the `{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}` path. 
    
12. Now that we have the record of the times the metrics changed and it's values for every class or method, the main function calls the `generate_metrics_track_record_statistics(repository_name, sorted_metrics_track_record)`, which will generate the metrics statistics (`Minimum`, `Maximum`, `Average` and `Third Quartile`) for every metric (`cbo`, `wmc` and `rfc`), which allow us to have a better understanding of the metrics behavior over time. Those statistics will be stored in the `{METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}-{CHANGED_METHODS_CSV_FILENAME}` file.
13. In this step, with those statistics generated and stored in the `{METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}-{CHANGED_METHODS_CSV_FILENAME}` csv file, the main funcion call the `sort_csv_by_changes(repository_name)` function that is going to sort the lines of the metrics statistics csv file by the `Changed` column, which is the number of times the metrics changed. The top changes will be stored in the `{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SORTED_CHANGED_METHODS_CSV_FILENAME}` csv file.  
14. Now, that we have the sorted csv file, the main function will call the `os.remove` to delete the old, unsorted csv file.
15. Finally, the main function will call the `sort_csv_by_percentual_variation(repository_name)` function to sort the substantial changes csv file named as `{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}` by the `Percentual Variation` column, which is the percentual variation of the metrics values.  
16. After all the processing is done, the `metrics_changes.py` script will output the elapsed execution time and play a sound to notify you that the script has finished.

### Auxiliar Scripts

In order to use the makefile rules, you must be in the `PyDriller/Scrips` directory.

#### Empty Folders

This script is used to verify if there are empty folders inside a specified directory. It is really usefull to make sure your files where processed or extracted correctly. 

##### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.

##### Run

Now that you have set the constants, you can run the following command to execute the following command:

```
make empty_folders_script
```

##### Workflow

1. The first thing it will do is ask you to specify the directory that you want to verify if there are empty folders inside it. If you don't specify the directory, type `Default` and it will use the directories stored in the `DATA_FOLDERS` constant, which is stored all of the directory names generated by this project. If you want to specify the directory, just type the directory name (in a relative or absolute path) and it will use it.
2. Then, it will, for each directory in the `initial_directory` list variable, call the `search_empty_folders` function, which will verify if there are empty folders inside the current directory. If there are, it will append the directory name to the `empty_folders` list. At the end, it will print the `empty_folders` list, which will contain the names of the empty folders inside the `initial_directory` list variable.

#### Extract Zip Files

This script is used to extract the zip files of the repositories. It is really usefull as i didn't want to reprocess the files, so i just packed them in zip files using the `generate_zip_files.sh`. 

##### Configuration

In order to execute it, you must modify the following constants:

1. `full_repositories`: This constant is used to specify the name of the repository that you want to extract the zip files.
2. `short_repositories`: This constant is used to specify the name of the repository that you want to extract the zip files, but in a shorter way, as it only have the useful generated data, like the `diffs`, `metrics_data`, `metrics_evolution`, `metrics_predictions`, `metrics_statistics` and `repositories`. So, it ignores the ck csv files stored in the `ck_metrics` directory, as they occupy a lot of space and are not useful, as they are only used for generating the metrics evolution, metrics predictions and metrics statistics files.

##### Run

Now that you have set the constants, you can run the following command to execute the following command:

```
make extract_zip_files_script
```

##### Workflow

1. **Verify the Execution Directory:** The script first verifies that it's being run from the `/PyDriller` directory. If not, it exits with a message instructing the user to run it from the correct location.

2. **Directory Setup:** It ensures that a directory named `compressed` exists within the current working directory. If this directory does not exist, the script creates it.

3. **Repository Definitions:** The script defines two arrays of repository names:
   - `full_repositories`: Contains names for the full versions of the repositories.
   - `short_repositories`: Contains names for shortened versions of the repositories.

4. **Unzipping Full Repositories:** For each repository name in the `full_repositories` array, the script looks for a corresponding zip file in the `compressed` directory and extracts it there. If the zip file doesn't exist, it outputs an error message.

5. **Unzipping Short Repositories:** Similarly, for each entry in the `short_repositories` array, it attempts to unzip the corresponding zip file into the `compressed` directory, with the same error handling for missing files.

6. **Sound Notification:** Upon successful extraction, the script attempts to play a notification sound from a predefined location (`../.assets/Sounds/NotificationSound.wav`). If the sound file is not found, it outputs a message indicating so.

7. **Completion Message:** Finally, it prints a message indicating the successful extraction of the files.

This script is intended to streamline the setup process for analyzing the specified repositories by ensuring all necessary data is extracted and ready for use.

#### Generate Short Zip Files

This script is used to generate the short zip files of the repositories. It is really usefull as i didn't want to reprocess the files, so i just packed them in zip files using the `generate_short_zip_files.sh`.

##### Configuration

In order to execute it, you must modify the following constants:

1. `repositories`: This constant is used to specify the names of the repositories that you want to generate the short zip files.
2. `subfolders`: This constant is used to specify the subfolders that you want to generate the short zip files. For example, if you want to generate the short zip files of the `diffs`, `metrics_data`, `metrics_evolution`, `metrics_predictions`, `metrics_statistics` and `repositories` subfolders, you must add them to the `subfolders` list.

##### Run

Now that you have set the constants, you can run the following command to execute the following command:

```
make generate_short_zip_files_script
```

##### Workflow

1. **Verify the Execution Directory:** The script first verifies that it's being run from the `/PyDriller` directory. If not, it exits with a message instructing the user to run it from the correct location.

2. **Directory Setup:** It ensures that a directory named `compressed` exists within the current working directory. If this directory does not exist, the script creates it.

3. **Repository Definitions:** The script defines two arrays of repository names:
   - `full_repositories`: Contains names for the full versions of the repositories.
   - `short_repositories`: Contains names for shortened versions of the repositories.

4. **Unzipping Full Repositories:** For each repository name in the `full_repositories` array, the script looks for a corresponding zip file in the `compressed` directory and extracts it there. If the zip file doesn't exist, it outputs an error message.

5. **Unzipping Short Repositories:** Similarly, for each entry in the `short_repositories` array, it attempts to unzip the corresponding zip file into the `compressed` directory, with the same error handling for missing files.

6. **Sound Notification:** Upon successful extraction, the script attempts to play a notification sound from a predefined location (`../.assets/Sounds/NotificationSound.wav`). If the sound file is not found, it outputs a message indicating so.

7. **Completion Message:** Finally, it prints a message indicating the successful extraction of the files.

#### Generate Zip Files

This script is used to generate the zip files of the repositories. As mentioned in the script above, tt is really usefull as i didn't want to reprocess the files, so i just packed them in zip files using the `generate_zip_files.sh`.

##### Configuration

In order to execute it, you must modify the following constants:

1. `repositories`: This constant is used to specify the names of the repositories that you want to generate the zip files.
2. `subfolders`: This constant is used to specify the subfolders that you want to generate the zip files. For example, if you want to generate the zip files of the `diffs`, `metrics_data`, `metrics_evolution`, `metrics_predictions`, `metrics_statistics` and `repositories` subfolders, you must add them to the `subfolders` list.

##### Run

Now that you have set the constants, you can run the following command to execute the following command:

```
make generate_zip_files_script
```

##### Workflow

1. **Directory Validation:** Initially, the script checks if it's being executed from the `/PyDriller` directory. If the script is not in the expected directory, it prompts the user to run it from `/PyDriller` and terminates.

2. **Repository and Subfolder Definition:** It defines an array named `repositories` that lists the names of repositories to be compressed. Additionally, an array named `subfolders` lists relevant subdirectories within each repository that need to be included in the zip files.

3. **Compression Directory Setup:** The script ensures a directory named `compressed` exists within the current working directory (`/PyDriller`). If this directory is absent, the script creates it to store the resulting zip files.

4. **Zip File Generation:**
   - The script iterates over each repository name in the `repositories` array.
   - For each repository, it constructs a list of paths by combining each subfolder's name with the repository name, ensuring all specified subfolders for each repository are included.
   - It also includes a CSV file (`repository_name-commits_list.csv`) located in the `ck_metrics` directory for each repository in the list of items to zip.
   - A zip file for each repository is created in the `compressed` directory, containing all specified subfolders and the commits list CSV file.

5. **Sound Notification:** Upon completion of the zip file creation process, the script attempts to play a notification sound from a specified path (`./../.assets/Sounds/NotificationSound.wav`). If the sound file cannot be found, it notifies the user.

6. **Completion Message:** A success message is displayed, indicating that the zip files have been created successfully.

#### Move Extracted Files

This is a really simple script, which is used to run after you execute the `extract_zip_files.sh` script, as it will move the extracted files to the right directory, for example, the extracted `/kafka/ck_metrics` will be placed in `/ck_metrics/kafka`.

##### Run

In order to execute it, you don't need to modify any constant, so you can just run the following command to execute the following command:

```
make move_extracted_files_script
```

##### Workflow

1. **Initial Setup and Validation:** The script starts by determining the current working directory. If the script is not executed from within the `/PyDriller` directory, it prompts the user to run it from the correct location and terminates to prevent unintended operations.

2. **Source Directory Specification:** It sets a variable `compressed_folder_path` to `"compressed"`, which is the directory containing the extracted folders that need to be organized.

3. **Destination Folders Definition:** An array named `extracted_folders` lists the names of the destination folders. These folders represent the different categories into which the extracted files will be organized.

4. **Moving Extracted Contents:**
   - The script iterates over each name in the `extracted_folders` array.
   - For each directory name, it first checks if the corresponding destination directory exists within the parent directory of the `compressed` directory. If a destination directory does not exist, the script creates it.
   - Then, the script moves all items from each extracted directory inside the `compressed` directory to the respective destination directory.
   - After successfully moving the files, it deletes the now-empty source directory within the `compressed` directory to clean up.

5. **Sound Notification:** Upon successfully organizing and cleaning up the files, the script attempts to play a notification sound. If the specified sound file cannot be found, it alerts the user about the missing file.

6. **Completion Message:** Finally, the script prints a success message indicating that the files have been moved and the source folders deleted, signaling the end of its operation.

#### Track Files

This script searches for files in the `PyDriller/diffs/` directory for any file defined in `TARGET_FILENAMES` constant for the repositories specified in the `REPOSITORIES` constant and write the list of found files to a txt file in `/PyDriller/metrics_data/repository_name/track_files_list.txt`. 

##### Configuration

In order to execute it, you must modify the following constants:

1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `TARGET_FILENAMES`: This dictionary is used to specify the names of the files that you want to track for each repository.
3. `REPOSITORIES`: This list is used to specify the names of the repositories that you want to track the files.

##### Run

Now that you have set the constants, you can run the following command to execute the following command:

```
make track_files_script
```

##### Workflow

1. This script will get the current directory and verify if it is the `PyDriller` directory.
2. Then, it will loop through the `REPOSITORIES` list and call the `search_files` function for each repository name.
3. The `search_files` function will get the `search_directory`, which is the `PyDriller/diffs/repository_name` directory, and the list inside the `TARGET_FILENAMES` dictionary for the current repository name. The `search_files` function will loop through the subfolders of the `search_directory` and search for the files in the `TARGET_FILENAMES` list. If it finds the file, it will append the file name to the `found_files` list and return the `found_files` list and the `found_file_counts` to the main function.
4. Lastly, it will write the `found_files` list to the `PyDriller/metrics_data/repository_name/track_files_list.txt` file.

## Generated Data

The outputs (generated data and metadata) of the scripts are stored in the `PyDriller/` directory, which are the following:

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

### Commit Diff Files 

   This directory contains the diffs files of the repositories, which are stored in the `./diffs/repository_name/commit_number-commit_hash/` directory. The `commit_number-commit_hash/` directory contains the diffs of the files of the repository for the specified commit hash.

   The `.diff` files have a similar structure to the `git diff` command output, which is as follows:

   ```diff
   def say_hi():
   -    print("Hello, World!")
   +    print("Hi!")
   ```

   The `-` symbol at the beginning of the line indicates that the line was removed, while the `+` symbol indicates that the line was added. The lines that don't have any symbol at the beginning of the line are the lines that are in the same state in both commits.

### Metrics Data  

   This directory contains the metrics data of the repositories, which are stored in the `metrics_data/repository_name` directory. The `repository_name` directory contains the `classes_track_record.txt` and/or `methods_track_record` files, which contains the data structure of the `metrics_track_record` dictionary, which contains the metrics evolution of the classes and methods of the repository.

   The `classes_track_record.txt` and `methods_track_record.txt` files have a similar structure to the `metrics_track_record` dictionary, which is as follows:

   ```txt
   Class name: 
      Metrics: [(CBO Value, WMC Value, RFC Value), (CBO Value 2, WMC Value 2, RFC Value 2), ... , (CBO Value N, WMC Value N, RFC Value N)]
      Commit Hashes: ['Commit Number 1 - Commit Hash 1', 'Commit Number 2 - Commit Hash 2', ... , 'Commit Number N - Commit Hash N']
      Changed: Number of times that the metrics changed (N)
   ```

   The above example is a short representation of the `metrics_track_record` dictionary, which contains the metrics evolution of the classes and methods of the repository. The example showed is what the `classes_track_record.txt` and `methods_track_record.txt` files contains, which (most likely) is various occurrences of the above example in the same file.

### Metrics Evolution  
   
   This directory contains the metrics evolution of the repositories, which are stored in the `metrics_evolution/repository_name` directory. The `repository_name` directory contains the `classes` and `methods` directories, which contains the metrics evolution of each classes and methods of the repository. In the csv file of each class or method, it contains the metrics values for each state (commit) of the repository where the class or method was modified.

   The CSV header of the `class.csv` and `method.csv` files are the following:

   ```csv
   | Class | Commit Hash | CBO | WMC | RFC |
   ```

   That's a visual representation of the CSV header of the `class.csv` and `method.csv` files, which contains the metrics evolution of the classes and methods of the repository. The lines that comes below the CSV header are the values of the commit hash and metrics for each class or method of the repository where the class or method was modified.

### Metrics Predictions  
   
   This directory contains the metrics linear regressions of the repositories, which are stored in the `metrics_predictions/repository_name` directory. The `repository_name` directory contains the `classes` and `methods` directories, which contains photos in the `.png` file format for each of the selected metrics of the classes and methods of the repository. The photos contains the linear regression graphics of the metrics values of the classes and methods of the repository.

   ![org.apache.zookeeper.server.quorum.Follower Class CBO Metric Linear Regression](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/blob/Outputs-Examples/PyDriller/Output-Examples/LinearRegression-CBO-org.apache.zookeeper.server.quorum.Follower.png)

### Metrics Statistics 

   This directory contains the metrics statistics and the substantial changes of the repositories, which are stored in the `metrics_statistics/repository_name` directory. The `repository_name/class_changes.csv` file stores the classes that, in descending order, changed the most times according to the tuple of selected metrics (CBO, WMC and RFC). The `repository_name/substantial_metric_name_classes_changes.csv` file stores the substantial changes of the classes of the repository, which contains the class name, variable attribute, from metric value, to metric value, percentual variation, commit number, commit hash, refactorings types and file path informations. The `repository_name/substantial_metric_name_classes_changes.csv` file stores the substantial changes of the methods of the repository, which contains the method name, variable attribute, from metric value, to metric value, percentual variation, commit number, commit hash, refactorings types and file path informations.

   The CSV header of the `class_changes.csv` and `method_changes.csv` files are the following:

   ```csv
   | Class | Type | Changed | CBO Min | CBO Max | CBO Avg | CBO Q3 | WMC Min | WMC Max | WMC Avg | WMC Q3 | RFC Min | RFC Max | RFC Avg | RFC Q3 | First Commit Hash | Last Commit Hash | 
   ```

   And the lines that comes below the CSV header are the occurrences of the classes the changed the most. The difference between the `class_changes.csv` and `method_changes.csv` files is that the `Type` attribute in the `class_changes.csv` file is the `class name` and the `Type` attribute in the `method_changes.csv` file is the `class_name` and `method name`.

   The CSV header of the `substantial_metric_name_classes_changes.csv` and `substantial_metric_name_methods_changes.csv` files are the following:

   ```csv
   | Class Name | Variable Attribute | From Metric Value | To Metric Value | Percentual Variation | Commit Number | Commit Hash | Refactorings Types | File Path |
   ```

   And the lines that comes below the CSV header are the occurrences of the substantial changes of the classes or methods of the repository.

### Progress Files  
   
   This directory contains the progress of the files generated by the `code_metrics.py` script, which are stored in the `progress/repository_name-progress.csv` file. This file is very useful for in case of the script execution stops in the middle of the execution, as it will store the progress of the script execution, so you can continue the execution from the last commit hash that was processed.

   The header of the `repository_name-progress.csv` file is the following:

   ```csv
   | Commit Hash | Commit Number | Commit Message | Commit Date |
   ```

   In the lines that comes below the header, it will store the history of all of the commits that were processed by the `code_metrics.py` script, in order to, in case of the script execution stops in the middle of the execution, you can continue the execution from the last commit hash that was processed.

### Refactorings Files

   This directory contains the refactorings of the repositories, which are stored in the `refactorings/repository_name/` directory. Inside the `repository_name` directory, there are the `commit_number-commit_hash.json` files, which contains the refactorings information of the repository for the specified commit hash.

   Here is an example of the `commit_number-commit_hash.json` file structure:

   ```json
   {
   "commits": [{
         "repository": "the_repository_name",
         "sha1": "the_commit_hash",
         "url": "the_commit_url",
         "refactorings": [{
            "type": "the_refactoring_type",
            "description": "the_refactoring_description",
            "leftSideLocations": {
               "filePath": "the_file_path",
               "startLine": "the_start_line",
               "endLine": "the_end_line"
            },
            "rightSideLocations": {
               "filePath": "the_file_path",
               "startLine": "the_start_line",
               "endLine": "the_end_line"
            }
         }]
      }]
   }
   ```

### Repositories Files
    
   This directory contains the cloned repositories, which are stored in the `repositories/repository_name` directory. We need this files locally to extract the ck metrics of the repositories.

## Contributing

If you want to contribute to this project, please read the Contributing section of the [Main README](../README.md) file, as well as the [CONTRIBUTING](../CONTRIBUTING.md) file in this repository.

## License

This project is licensed under the [Apache License 2.0](../LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](../LICENSE) file in this repository.
