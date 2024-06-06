<div align="center">
  
# [Refactoring Miner.](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/tree/main/RefactoringMiner) <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the Refactoring Miner directory, in which you will find the scripts that generates the refactoring script of an specific commit of a class or method of a repository and the script that generates the refactorings for an entire repository. The scripts that are located in this directory are part of the [Worked-Example-Miner (WEM)](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) Tool.

RefactoringMiner stands out as an instrument for the analysis of software maintenance and evolution, empowering both developers and researchers with deep insights into the dynamics of code evolution via refactorings. The tool captures refactorings, cataloging them in JSON files. These files serve as a codebase analyses, enabling the identification of significant refactoring patterns and trends that mark the software's evolutionary journey. Such insights are crucial for comprehensively understanding the ramifications of refactorings on the codebase, shedding light on their influence on the software's quality and maintainability.

With our objective to craft a compelling worked example for Software Engineering classes, particularly focusing on Distributed Systems Open-Source Softwares, RefactoringMiner's capabilities become even more pronounced. It aids in pinpointing potential classes and methods ripe for refactoring, setting the stage for the development of a meticulously designed example. This not only demonstrates the practical application of refactorings but also enhances the learning experience by providing a real-world context to the theoretical concepts discussed in class.
  
---

</div> 

- [Refactoring Miner. ](#refactoring-miner-)
  - [Important Notes](#important-notes)
  - [Setup](#setup)
    - [Python and Pip](#python-and-pip)
      - [Linux](#linux)
      - [MacOS](#macos)
      - [Windows](#windows)
    - [Requirements](#requirements)
    - [Cleaning Up](#cleaning-up)
  - [How to use](#how-to-use)
    - [Metrics Evolution Refactorings](#metrics-evolution-refactorings)
      - [Configuration](#configuration)
      - [Run](#run)
      - [Workflow](#workflow)
    - [Repositories Refactorings](#repositories-refactorings)
      - [Configuration](#configuration-1)
      - [Run](#run-1)
      - [Workflow](#workflow-1)
  - [Generated Data](#generated-data)
    - [Metrics Evolution Refactorings](#metrics-evolution-refactorings-1)
    - [Repositories Refactorings](#repositories-refactorings-1)
  - [Contributing](#contributing)
  - [License](#license)

## Important Notes

- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- To enhance the readability of the code, please note that the files adhere to a Bottom-Up approach in function ordering. This means that each function is defined above the function that calls it
- All of the Scripts have a `Makefile`that handles virtual environment creation, dependencies installation and script execution. You can run the scripts by using the `make` command, as shown in the `How to use` section.
- All of the Scripts usually output an estimated time of the script execution, based on things like the number of commits of the repository, the number of classes or methods to be analyzed, etc. But this is just an estimate, the actual time does vary a lot depending on the machine you're using, on what is running on the machine, and many other factors.

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

- [NumPy](https://numpy.org/) -> NumPy is used to generate the linear prediction of the linear regression and to many operations in the list of the metrics.
- [Pandas](https://pandas.pydata.org/) -> Pandas is used mainly to read and write the csv files.
- [PyDriller](https://pydriller.readthedocs.io/en/latest/) -> PyDriller is used to get the number of commits of the repositories.
- [TQDM](https://tqdm.github.io/) -> TQDM is used to show the progress bar of the scripts.

Futhermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment** 
   
   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `numpy`, `pandas` and `tqdm`, will be installed.
This will also be handled by the `Makefile` during the dependencies installation process, so no command must be executed in order to create the virtual environment.

1. **Install Dependencies** 
   
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

2. **Running Scripts**
   
   The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `repositories_refactorings.py` file, use:

   ```
   make repositories_refactorings_script
   ```

   This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

3. **Generate the requirements.txt file**

   If you changed the project dependencies and want to update the `requirements.txt` file, you can run the following command:

      ```
      make generate_requirements
      ```

   This command will generate the `requirements.txt` file in the root of the tool directory (`RefactoringMiner/`) which will contain all the dependencies used in the virtual environment of the project.

### Cleaning Up

To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:

```
make clean
```

This command removes the `venv` directory and deletes any cached Python files in the project directory, helping maintain a clean workspace.

By following these instructions, you'll ensure that all project dependencies are correctly managed and isolated, leading to a more stable and consistent development environment.

## How to use

In order to use the makefile rules, you must be in the `RefactoringMiner` directory.

### Metrics Evolution Refactorings

This script is used to generate the refactorings json file of an specific commit of a class or method stored in the `FILES_TO_ANALYZE` dictionary for the repository name stored in the `DEFAULT_REPOSITORY`dictionary, in case they were not already generated. In order to run this script, you must have already executed the PyDriller `code_metrics.py` and `metrics_evolution.py` scripts, as the classes and methods to be analyzed are the ones selected by the result of the analysis of the PyDriller generated data and metadata.

#### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant. This constant is imported from the `repositories_refactorings.py` file.  
2. `DESIRED_REFACTORINGS_ONLY`: A boolean that indicates if you want to filter the refactorings by the ones listed on the `DESIRED_REFACTORING_TYPE` list. If set to `True`, it will filter the refactorings by the `DESIRED_REFACTORING_TYPE` variable. If set to `False`, it will not filter the refactorings by the `DESIRED_REFACTORING_TYPE` variable.
3. `DESIRED_REFACTORING_TYPE`: This must only be modified if the `DESIRED_REFACTORINGS_ONLY` is set to `True`. This is a list of the refactoring types that you are interested in. It must contain the names of the refactorings detected by RefactoringMiner. See more [here](https://github.com/tsantalis/RefactoringMiner?tab=readme-ov-file#general-info).  
4. `DEFAULT_REPOSITORY`: The repository name that has the classes or methods to be analyzed.  
5. `FILES_TO_ANALYZE`: A dictionary to store the files to analyze in the repository. It's keys (class name) and value (method name) must be the names of classes or methods that you want to analyze deeper after selecting them from the analysis of the PyDriller generated data and metadata.

#### Run

Now that you have set the constants, you can run the following command to execute the `metrics_evolution_refactorings.py` file:

```shell
make metrics_evolution_refactorings_script
```

#### Workflow

1. The first thing this script does is verify if the path contains whitespace, if so, it will not work, so it will ask the user to remove the whitespace from the path and then run the script again.
2. Now it will create the json output directory and the repository directory if they don't exist.
3. Now it calls `process_repository(DEFAULT_REPOSITORY, DEFAULT_REPOSITORIES[DEFAULT_REPOSITORY])`, which will do the following steps:
   
   1. Call the `clone_repository(repository_name, repository_url)` to clone or update the repository, depending on whether it already exists or not.
   2. Then, it calls `generate_refactorings_concurrently(repository_name)` where, for each of the items in the `FILES_TO_ANALYZE` dictionary, creating a thread for handling the analysis of each file. The target function of the thread is the `generate_commit_refactorings_for_class_or_methods(repository_name, classname, variable_attribute)`.
        1. In this function, it will loop through each of the commit hashes in the csv from the `PyDriller/metrics_evolution` directory and generate the refactorings for the commit hashes where that specified classes or method was modified using the `-c` parameter of the `RefactoringMiner` tool and save the output in the `json_files` directory.
        2. Lastly, it calls the `filter_json_file(classname, json_filepath, json_filtered_filepath)` that will read the generated json file and filter the refactorings by the `DESIRED_REFACTORING_TYPES` variable and save the filtered refactorings in the `json_files` directory.
4. Finally, it will output the execution time of the script and wait for all the threads to finish to output a end of the execution message.

### Repositories Refactorings

This script is used to generate the refactorings json file of an entire repository. It will generate the refactorings for each commit of the specified repositories in the `DEFAULT_REPOSITORIES` dictionary, in case they were not already generated.

#### Configuration

In order to run this code as you want, you must modify the following constants:

1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `DEFAULT_REPOSITORIES` dictionary in the `code_metrics.py` file, in which you must specify the repository name and the repository url.

#### Run

Now that you have set the constants, you can run the following command to execute the `repositories_refactorings.py` file:

  ```shell
  make repositories_refactorings_script
  ```

#### Workflow

1. As for every file in this project, the first thing it will do is verify if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. In this step, the main function will call the `verify_refactorings()` to verify if the RefactoringMiner refactorings for the DEFAULT_REPOSITORIES were already generated. If not, it will generate them. This verification is done by verifying if the RefactoringMiner json output file is located in the `{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH}/{repository_name}.{JSON_FILE_FORMAT}` directory. If the file is not found, it will add the repository url to the `repositories` dictionary, using the repository name as the key.  
3. Now, in case there are repositories to be analyzed, it will create the json output directory and the repository directory if they don't exist.
4. Now it calls `process_repositories_concurrently(repositories)`, which will do the following steps:
   
   1. This function will loop through each of the repositories in the `repositories` dictionary.
   2. Inside this loop, it will output an estimated time of the script execution, based on the number of commits of the repository.
   3. Then, it will create a thread for handling the analysis of each repository, executing the `process_repository(repository_name, repository_url)` function.
   
5. Inside the `process_repository(repository_name, repository_url)` function, it will do the following steps: 
   1. It calls the `clone_repository(repository_name, repository_url)` function, which will clone or update the repository, depending on whether it already exists or not.
   2. In the next step, it will call the `generate_commit_refactorings(repository_name)` function, which will generate the refactorings for each of the commits in the repository using the `-a` parameter of the `RefactoringMiner` tool and save the output in the `{FULL_JSON_FILES_DIRECTORY_PATH}{RELATIVE_REPOSITORIES_REFACTORINGS_DIRECTORY_PATH}/{repository_name}.{JSON_FILE_FORMAT}` filepath.
   3. Lastly, it will output the execution time of the script, based on the start time and the end time of the script execution.
   
6. Now, the thread will finish and the script will wait for all the threads to finish, and output a end of the execution message.

## Generated Data

The outputs (generated data) of the scripts are JSON files containing the refactorings identified by RefactoringMiner. These files are stored in the `json_files` directory.

The generated files for both the `repositories_refactorings.py` and `metrics_evolution_refactorings.py` scripts are structured in a similar way, with the main difference being where they are stored, their size, and if they represent the refactorings of an entire repository or the refactorings of a specific commit of a class or method. With that in mind, the json files are similar to the following example:

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

Below is a breakdown of what each field in these files represents:

- `commits`: An array holding information about each commit that includes refactorings. This is the top-level element that encapsulates all data about the refactorings in a specific repository.

  - `repository`: Indicates the name of the repository to which the commit belongs. This helps in identifying the source repository for the refactorings.

  - `refactorings`: An array within each commit object, listing all the refactorings detected in that commit.
  
    - `commit`: Contains the hash of the commit where the refactorings were found. This serves as a unique identifier for the commit in the repository's history.

    - `refactorings`: Nested within the previous `refactorings` array, this is another level deeper array that details each refactoring action.
    
      - `type`: Specifies the type of refactoring that was performed, such as "Extract Method" or "Rename Variable". This helps in understanding the nature of the change.
      
      - `description`: Provides a textual description of the refactoring, offering insights into what was changed and possibly why.
      
      - `leftSideLocations` and `rightSideLocations`: These objects detail the locations in the source code before (`leftSideLocations`) and after (`rightSideLocations`) the refactoring, respectively.
      
        - `filePath`: The path to the file where the refactoring took place. This path is relative to the repository root.
        
        - `startLine`: The line number in the file where the refactoring begins. This aids in locating the specific block of code that was refactored.
        
        - `endLine`: The line number in the file where the refactoring ends, marking the scope of the change.

This structure allows for a comprehensive overview of refactorings within a repository, making it easier to track and analyze changes over time.

### Metrics Evolution Refactorings

Just like the json file structure mentioned above, the json files generated by the `metrics_evolution_refactorings.py` script are similar, but they will contain the refactorings of the specific commits where a specified class or method where modified. The `metrics_evolution_refactorings.py` script generated data are stored in the `json_files/metrics_evolution_refactorings` directory, using the `{repository_name}/{CLASS OR METHODS}/{classname}/{commit_number-commit_hash}.{JSON_FILE_FORMAT}` filename.

### Repositories Refactorings

As mentioned before, the structure of the json files generated by the `repositories_refactorings.py` script is similar to the one above, but it will contain the refactorings of an entire repository, instead of the refactorings of a specific commit of a class or method. The `repositories_refactorings.py` script generates the refactorings for each commit of the specified repositories and are stored in the `json_files/repositories_refactorings` directory, using the the `{repository_name}.{JSON_FILE_FORMAT}` filename.

## Contributing

If you want to contribute to this project, please read the Contributing section of the [Main README](../README.md) file, as well as the [CONTRIBUTING](../CONTRIBUTING.md) file in this repository.

## License

This project is licensed under the [Apache License 2.0](../LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](../LICENSE) file in this repository.
