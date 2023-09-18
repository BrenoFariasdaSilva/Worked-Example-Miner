#!/bin/bash

# Run:
# chmod +x ./moveExtractedFiles.sh
# ./moveExtractedFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Print the current directory
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "/PyDriller" or "/PyDriller/Scripts", then exit
if [[ "${current_dir}" != *"/PyDriller" && "${current_dir}" != *"/PyDriller/Scripts" ]]; then
   echo "Please run the script from the '/PyDriller' or '/PyDriller/Scripts' directory."
   exit
fi

# Define the save path prefix
path_prefix=""

# Check if the current directory ends with "/PyDriller" or "/PyDriller/Scripts"
if [[ "${current_dir}" == *"/PyDriller/Scripts" ]]; then
   path_prefix="../" # Set the save path prefix
fi

# Define the source and destination folder names
source_folders=("commons-lang" "jabref" "kafka" "zookeeper")
destination_folders=("ck_metrics" "diffs" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# Loop through the source folders and move their contents
for source_folder in "${source_folders[@]}"; do
   # Loop through the destination folders and move the contents
   for destination_folder in "${destination_folders[@]}"; do
      echo "Moving the contents from ${source_folder}/${destination_folder} to ${path_prefix}${destination_folder}/"
      # Create the destination folder if it doesn't exist
      mkdir -p "${path_prefix}${destination_folder}"
      
      # Move the contents from the source to destination folder
      mv "${source_folder}/${destination_folder}"/* "${path_prefix}${destination_folder}/"
   done

   # Delete the source folder after moving its contents
   rm -r "${source_folder}"
done

# Print a success message
echo "Files moved and source folders deleted successfully."