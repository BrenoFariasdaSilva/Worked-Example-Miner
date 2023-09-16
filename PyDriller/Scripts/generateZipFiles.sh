#!/bin/bash

# Run:
# chmod +x ./generateZipFiles.sh
# ./generateZipFiles.sh

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Define the list of subfolders
subfolders=("ck_metrics" "diff" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# List of the folder to zip
folders_list=("")

# Get the current directory
current_dir="$(pwd)"

# If the current_dir doesn't end with "PyDriller" or "Scripts", then exit
if [[ "$current_dir" != *"Scripts" ]] && [[ "$current_dir" != *"PyDriller" ]]; then
   echo "Please run the script from the /PyDriller or PyDriller/Scripts directory."
   exit
fi

# Create a "Compressed" directory if it does not exist
if [[ "$current_dir" == *"Scripts" ]] && [[ ! -d "../compressed/" ]]; then
   mkdir -p "../Compressed/" # Create the directory
fi
if [[ "$current_dir" == *"PyDriller" ]] && [[ ! -d "../compressed/" ]]; then
   mkdir -p "/Compressed/" # Create the directory
fi

# Loop through the repositories
for repo_name in "${repositories[@]}"; do
   # Clean the folders_list variable
   folders_list=("")
   for folder in "${subfolders[@]}"; do
      if [[ "$current_dir" == *"Scripts" ]]; then
         # Change the directory to the repository
         folders_list+=("../${folder}/${repo_name}/")
      fi
      if [[ "$current_dir" == *"PyDriller" ]]; then
         # Change the directory to the repository
         folders_list+=("${folder}/${repo_name}/")
      fi
   done
   echo "${folders_list[@]}"

   # Create a zip file for the repository
   zip -r "${repo_name}.zip" "${folders_list[@]}"
done

echo "Zip files created successfully."