#!/bin/bash

# Run:
# chmod +x ./generate_short_zip_files.sh
# ./generate_short_zip_files.sh

# Echo welcome message
echo "Welcome to the Generate Short Zip Files script!"

# Get the current directory
current_dir="$(pwd)"

# Print the current directory
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "/PyDriller", then exit
if [[ "${current_dir}" != *"/PyDriller" ]]; then
   echo "Please run the script from the '/PyDriller' with the command './Scripts/generate_short_zip_files.sh'."
   exit # Exit the script
fi

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Define the list of subfolders
subfolders=("diffs" "metrics_data" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# List of the folder to zip
folders_list=("")

# Create a "Compressed" directory if it does not exist
if [[ "${current_dir}" == *"/PyDriller" ]]; then
   if [[ ! -d "compressed/" ]]; then # Check if the directory does not exist
      echo "Creating the compressed directory in current path..."
      mkdir -p "compressed" # Create the directory
   fi
fi

# Loop through the repositories names
for repo_name in "${repositories[@]}"; do
   folders_list=("")                              # Clean the folders_list variable
   for folder in "${subfolders[@]}"; do           # Loop through the subfolders
      folders_list+=("./${folder}/${repo_name}/") # Add the folder to the list
   done

   # Add the .//ck_metrics/repository_name-commits_list.csv file to the list
   folders_list+=("./ck_metrics/${repo_name}-commits_list.csv")

   echo "Creating a zip file for the ${repo_name} repository..."

   # Create a zip file for the repository
   zip -r "./compressed/${repo_name}-short.zip" "${folders_list[@]}"
done

# Play a sound when the script finishes
sound_file="./../.assets/Sounds/NotificationSound.wav"

if [ -e "$sound_file" ]; then
   aplay "$sound_file" # Play the sound file
else
   echo "Sound file not found at: $sound_file"
fi

# Print a success message
echo "Short Zip Files created successfully."
