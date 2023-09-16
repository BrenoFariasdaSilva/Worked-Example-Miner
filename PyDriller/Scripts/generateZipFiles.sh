#!/bin/bash

# Run:
# chmod +x ./generateZipFiles.sh
# ./generateZipFiles.sh

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Define the list of subfolders
subfolders=("ck_metrics" "diffs" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# List of the folder to zip
folders_list=("")

# Get the current directory
current_dir="$(pwd)"
save_path_prefix=""
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "PyDriller" or "Scripts", then exit
if [[ "${current_dir}" != *"Scripts" && "${current_dir}" != *"PyDriller" ]]; then
   echo "Please run the script from the /PyDriller or PyDriller/Scripts directory."
   exit
fi

# Create a "Compressed" directory if it does not exist
if [[ "${current_dir}" == *"Scripts" ]]; then
   save_path_prefix="../"
   if [[ ! -d "${save_path_prefix}compressed/" ]]; then
      echo "Creating the compressed directory in parent path..."
      mkdir -p "${save_path_prefix}compressed" # Create the directory
   fi
fi
if [[ "${current_dir}" == *"PyDriller" ]]; then
   if [[ ! -d "compressed/" ]]; then
      echo "Creating the compressed directory in current path..."
      mkdir -p "compressed" # Create the directory
   fi
fi

# Loop through the repositories
for repo_name in "${repositories[@]}"; do
   # Clean the folders_list variable
   folders_list=("")
   for folder in "${subfolders[@]}"; do
      folders_list+=("${save_path_prefix}${folder}/${repo_name}/") # Add the folder to the list
   done

   # Create a zip file for the repository
   zip -r "${save_path_prefix}compressed/${repo_name}.zip" "${folders_list[@]}"
done

echo "Zip files created successfully."