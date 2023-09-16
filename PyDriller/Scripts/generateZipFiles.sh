#!/bin/bash

# Run:
# chmod +x ./generateZipFiles.sh
# ./generateZipFiles.sh

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Define the list of subfolders
subfolders=("ck_metrics" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# List of the folder to zip
folders_list=("")

# Get the current directory
current_dir="$(pwd)"

echo "Current directory: ${current_dir}"

# Loop through the repositories
for repo_name in "${repositories[@]}"; do
   # Clean the folders_list variable
   folders_list=("")
   for folder in "${subfolders[@]}"; do
      if [[ "$current_dir" == *"Scripts" ]]; then
         # Change the directory to the repository
         folders_list+=("../${folder}/${repo_name}/")
      else
         # Change the directory to the repository
         folders_list+=("${folder}/${repo_name}/")
      fi
   done
   echo "${folders_list[@]}"
   # Create a zip file for the repository
   zip -r "${repo_name}.zip" "${folders_list[@]}"
done

echo "Zip files created successfully."