#!/bin/bash

# Run:
# chmod +x ./extractZipFiles.sh
# ./extractZipFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Check if the current directory ends with "/Scripts" or "/PyDriller"
if [[ "$current_dir" == *"/Scripts" ]]; then
   compressed_dir="../compressed"
elif [[ "$current_dir" == *"/PyDriller" ]]; then
   compressed_dir="/compressed"
else
   echo "This script is meant to run in a directory ending with '/PyDriller' or '/PyDriller/Scripts'."
   exit
fi

# Check if the "compressed" directory exists
if [ -d "$compressed_dir" ]; then
   # Loop through the specified repository names and unzip the corresponding files
   for repo_name in "commons-lang" "jabref" "kafka" "zookeeper"; do
      zipfile="$compressed_dir/${repo_name}.zip"
      if [ -e "$zipfile" ]; then
         unzip -q "$zipfile" -d "$compressed_dir"
         echo "Unzipped $zipfile to $compressed_dir"
      else
         echo "File $zipfile not found in $compressed_dir"
      fi
   done
else
  echo "The 'compressed' directory does not exist in the expected location."
  exit 1
fi
