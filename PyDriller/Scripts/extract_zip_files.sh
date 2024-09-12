#!/bin/bash

# Run:
# chmod +x ./extract_zip_files.sh
# ./extract_zip_files.sh

# Echo welcome message
echo "Welcome to the Extract Zip Files script!"

# Get the current directory
current_dir="$(pwd)"

# Print the current directory
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "/PyDriller", then exit
if [[ "${current_dir}" != *"/PyDriller" ]]; then
   echo "Please run the script from the '/PyDriller' with the command './Scripts/extract_zip_files.sh'."
   exit 1 # Exit the script with an error code
fi

# Define the compressed directory
compressed_dir="compressed" # Set the compressed directory

# If the compressed directory does not exist, then exit
if [[ ! -d "$compressed_dir" ]]; then
   echo "The compressed directory does not exist. Please ensure there are zip files in the ${compressed_dir} directory."
   exit 1 # Exit the script with an error code
fi

# Get the list of zip files in the ./compressed directory (without extensions)
repositories=($(find "$compressed_dir" -maxdepth 1 -name "*.zip" -exec basename {} .zip \; | sort))

# Check if any zip files were found
if [[ ${#repositories[@]} -eq 0 ]]; then
   echo "No zip files found in ${compressed_dir}. Exiting..."
   exit 1 # Exit the script with an error code
fi

# Loop through the repository zip files and unzip them
for repo_name in "${repositories[@]}"; do
   zipfile="$compressed_dir/${repo_name}.zip" # Define the zip file path
   echo "Unzipping $zipfile to $compressed_dir..."
   if [[ -e "$zipfile" ]]; then # Check if the zip file exists
      unzip -q "$zipfile" -d "$compressed_dir" # Unzip the file
      echo "Unzipped $zipfile to $compressed_dir"
   else # If the zip file does not exist, then print an error message
      echo "File $zipfile not found in $compressed_dir"
   fi
done

# Print a success message
echo "Files extracted successfully."
