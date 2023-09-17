#!/bin/bash

# Run:
# chmod +x ./extractZipFiles.sh
# ./extractZipFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Define the compressed directory
compressed_dir="" 

# Check if the current directory ends with "/Scripts" or "/PyDriller"
if [[ "$current_dir" == *"/Scripts" ]]; then
   compressed_dir="../compressed"
elif [[ "$current_dir" == *"/PyDriller" ]]; then
   compressed_dir="/compressed"
else
   echo "This script is meant to run in a directory ending with '/PyDriller' or '/PyDriller/Scripts'."
   exit
fi

# if the compressed directory does not exist, then create it
if [[ ! -d "$compressed_dir" ]]; then
   echo "Creating the compressed directory in current path..."
   mkdir -p "$compressed_dir" # Create the directory
fi

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Loop through the specified repository names and unzip the corresponding files
for repo_name in "${repositories[@]}"; do
   zipfile="$compressed_dir/${repo_name}.zip"
   if [ -e "$zipfile" ]; then
      unzip -q "$zipfile" -d "$compressed_dir"
      echo "Unzipped $zipfile to $compressed_dir"
   else
      echo "File $zipfile not found in $compressed_dir"
   fi
done
