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

compressed_folder_path=""

if [[ "${current_dir}" == *"/PyDriller" ]]; then
   compressed_folder_path="/compressed" # Set the compressed directory
elif [[ "${current_dir}" == *"/PyDriller/Scripts" ]]; then
   compressed_folder_path="../compressed" # Set the compressed directory
fi

# Define the extraced folder names
extracted_folders=("ck_metrics" "diffs" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# Loop through the destination folders and move the contents
for extracted_folders in "${extracted_folders[@]}"; do
   echo "Moving the contents from ${compressed_folder_path}/${extracted_folders} to ../"

   # If the destination folder doesn't exist, then create it
   if [[ ! -d "../${extracted_folders}" ]]; then
      mkdir "../${extracted_folders}"
   fi
   
   # Move the contents from the source to destination folder
   mv "${compressed_folder_path}/${extracted_folders}"/* "../${extracted_folders}/"

   # Delete the source folder
   rm -rf "${compressed_folder_path}/${extracted_folders}"
done

# Print a success message
echo "Files moved and source folders deleted successfully."