import os # OS module in Python provides functions for interacting with the operating system
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 

DEFAULT_OUTPUT_DIRECTORY = "output"
DEFAULT_REPOSITORY_URL = "https://github.com/apache/commons-lang"

# TODO: Informar o último parâmetro o diretório de saída

# @brief: If inputs are empty, use the default values
# @param: repository_url: URL of the repository to be analyzed
# @param: output_directory: Directory to save the output files
# @return: The repository URL and the output directory
def check_inputs(repository_url, output_directory):
    if not repository_url:
        repository_url = DEFAULT_REPOSITORY_URL
    if not output_directory:
        output_directory = DEFAULT_OUTPUT_DIRECTORY
    return repository_url, output_directory

# @brief: Create a subdirectory to save the output files
# @param: directory_name: Name of the directory to be created
# @return: None
def create_output_directory(directory_name):
    try:
        os.mkdir(directory_name)
    except OSError:
        print ("Creation of the directory %s failed" % directory_name)
    else:
        print ("Successfully created the directory %s " % directory_name)

# @brief: Main function
# @param: None
# @return: None
def main():
    # Ask for use input of the output directory
    output_directory = input("Enter the output directory: ")
    # Ask for use input of the repository URL
    repository_url = input("Enter the github repository URL: ")

    # Check if the inputs are empty
    repository_url, output_directory = check_inputs(repository_url, output_directory)

    # Create the output directory
    create_output_directory(output_directory)

    for commit in Repository(repository_url).traverse_commits():
        cmd = f"java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {commit.hash}"
        # TODO: Olhar como ele percorre a ´arvore dos commits
        # TODO: Variables and Metrics tentar desabilitar isso
        # TODO: Caminho do projet FALSE 0 FALSE directory
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())

if __name__ == '__main__':
    main() 