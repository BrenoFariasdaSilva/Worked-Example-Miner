#!/bin/bash

# Run:
# chmod +x ./generateZipFiles.sh
# ./generateZipFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Print the current directory
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "/PyDriller" or "/PyDriller/Scripts", then exit
if [[ "${current_dir}" != *"/PyDriller" && "${current_dir}" != *"/PyDriller/Scripts" ]]; then
   echo "Please run the script from the '/PyDriller' or '/PyDriller/Scripts' directory."
   exit # Exit the script
fi

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Define the list of subfolders
subfolders=("ck_metrics" "diffs" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# List of the folder to zip
folders_list=("")

# Define the save path prefix
path_prefix=""

# Create a "Compressed" directory if it does not exist
if [[ "${current_dir}" == *"/PyDriller" ]]; then
   if [[ ! -d "compressed/" ]]; then # Check if the directory does not exist
      echo "Creating the compressed directory in current path..."
      mkdir -p "compressed" # Create the directory
   fi
fi
if [[ "${current_dir}" == *"/PyDriller/Scripts" ]]; then
   path_prefix="../" # Set the save path prefix
   if [[ ! -d "${path_prefix}compressed/" ]]; then # Check if the directory does not exist
      echo "Creating the compressed directory in parent path..."
      mkdir -p "${path_prefix}compressed" # Create the directory
   fi
fi

# Loop through the repositories names
for repo_name in "${repositories[@]}"; do
   folders_list=("") # Clean the folders_list variable
   for folder in "${subfolders[@]}"; do # Loop through the subfolders
      folders_list+=("${path_prefix}${folder}/${repo_name}/") # Add the folder to the list
   done

   echo "Creating a zip file for the ${repo_name} repository..."

   # Create a zip file for the repository
   zip -r "${path_prefix}compressed/${repo_name}.zip" "${folders_list[@]}"
done

# Play a sound when the script finishes
sound_file="${path_prefix}../.assets/NotificationSound.wav"

if [ -e "$sound_file" ]; then
  aplay "$sound_file" # Play the sound file
else
  echo "Sound file not found at: $sound_file"
fi

# Print a success message
echo "Zip files created successfully."