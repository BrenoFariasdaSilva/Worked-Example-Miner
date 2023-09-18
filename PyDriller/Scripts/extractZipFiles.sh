#!/bin/bash

# Run:
# chmod +x ./extractZipFiles.sh
# ./extractZipFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Define the compressed directory
compressed_dir="" 
prefix_path=""

# If the current_dir doesn't end with "/PyDriller" or "/PyDriller/Scripts", then exit
if [[ "${current_dir}" != *"/PyDriller" && "${current_dir}" != *"/PyDriller/Scripts" ]]; then
   echo "Please run the script from the '/PyDriller' or '/PyDriller/Scripts' directory."
   exit
fi

# Check if the current directory ends with "/PyDriller" or "/PyDriller/Scripts"
if [[ "$current_dir" == *"/PyDriller" ]]; then
   compressed_dir="/compressed" # Set the compressed directory
elif [[ "$current_dir" == *"/PyDriller/Scripts" ]]; then
   compressed_dir="../compressed" # Set the compressed directory
   prefix_path="../" # Set the prefix path
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
   echo "Unzipping $zipfile to $compressed_dir..."
   if [ -e "$zipfile" ]; then # Check if the zip file exists
      unzip -q "$zipfile" -d "$compressed_dir" # Unzip the file
      echo "Unzipped $zipfile to $compressed_dir" 
   else # If the zip file does not exist, then print an error message
      echo "File $zipfile not found in $compressed_dir"
   fi
done

# Play a sound when the script finishes
sound_file="${prefix_path}../.assets/NotificationSound.wav"

if [ -e "$sound_file" ]; then
  aplay "$sound_file" # Play the sound file
else
  echo "Sound file not found at: $sound_file"
fi

# Print a success message
echo "Files unzipped successfully."