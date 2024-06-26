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
   exit # Exit the script
fi

# Define the compressed directory
compressed_dir="compressed" # Set the compressed directory

# If the compressed directory does not exist, then create it
if [[ ! -d "$compressed_dir" ]]; then
   echo "Creating the ${compressed_dir} directory in current path..."
   mkdir -p "$compressed_dir" # Create the directory
fi

# Define the list of repositories
full_repositories=("commons-lang" "jabref" "kafka" "zookeeper")
short_repositories=("commons-lang-short" "jabref-short" "kafka-short" "zookeeper-short")

# Loop through the specified repository names and unzip the corresponding files
for repo_name in "${full_repositories[@]}"; do
   zipfile="$compressed_dir/${repo_name}.zip" # Define the zip file path
   echo "Unzipping $zipfile to $compressed_dir..."
   if [ -e "$zipfile" ]; then                  # Check if the zip file exists
      unzip -q "$zipfile" -d "$compressed_dir" # Unzip the file
      echo "Unzipped $zipfile to $compressed_dir"
   else # If the zip file does not exist, then print an error message
      echo "File $zipfile not found in $compressed_dir"
   fi
done

# Loop through the specified repository names and unzip the corresponding files
for repo_name in "${short_repositories[@]}"; do
   zipfile="$compressed_dir/${repo_name}.zip" # Define the zip file path
   echo "Unzipping $zipfile to $compressed_dir..."
   if [ -e "$zipfile" ]; then                  # Check if the zip file exists
      unzip -q "$zipfile" -d "$compressed_dir" # Unzip the file
      echo "Unzipped $zipfile to $compressed_dir"
   else # If the zip file does not exist, then print an error message
      echo "File $zipfile not found in $compressed_dir"
   fi
done

# Play a sound when the script finishes
sound_file="./../../.assets/Sounds/NotificationSound.wav"

if [ -e "$sound_file" ]; then
   aplay "$sound_file" # Play the sound file
else
   echo "Sound file not found at: $sound_file"
fi

# Print a success message
echo "Files extracted successfully."
