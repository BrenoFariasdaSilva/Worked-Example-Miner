#!/bin/bash

# Run:
# chmod +x ./extractZipFiles.sh
# ./extractZipFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Define the compressed directory
compressed_dir="" 

# If the current_dir doesn't end with "/PyDriller" or "/PyDriller/Scripts", then exit
if [[ "${current_dir}" != *"/PyDriller" && "${current_dir}" != *"/PyDriller/Scripts" ]]; then
   echo "Please run the script from the '/PyDriller' or '/PyDriller/Scripts' directory."
   exit
fi

# Check if the current directory ends with "/PyDriller" or "/PyDriller/Scripts"
if [[ "$current_dir" == *"/PyDriller" ]]; then
   compressed_dir="/compressed"
elif [[ "$current_dir" == *"/PyDriller/Scripts" ]]; then
   compressed_dir="../compressed"
fi

# If the compressed directory does not exist, then create it
if [[ ! -d "$compressed_dir" ]]; then
   echo "Creating the ${compressed_dir} directory in current path..."
   mkdir -p "$compressed_dir" # Create the directory
fi

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Loop through the specified repository names and unzip the corresponding files
for repo_name in "${repositories[@]}"; do
   zipfile="$compressed_dir/${repo_name}.zip" # Define the zip file path
   if [ -e "$zipfile" ]; then # Check if the zip file exists
      unzip -q "$zipfile" -d "$compressed_dir" # Unzip the file
      echo "Unzipped $zipfile to $compressed_dir" 
   else # If the zip file does not exist, then print an error message
      echo "File $zipfile not found in $compressed_dir"
   fi
done

echo "Files unzipped successfully."