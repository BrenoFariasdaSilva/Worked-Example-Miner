#!/bin/bash

# Run:
# chmod +x ./generate_zip_files.sh
# ./generate_zip_files.sh

# Echo welcome message
echo "Welcome to the Generate Zip Files script!"

# Get the current directory
current_dir="$(pwd)"

# Print the current directory
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "/PyDriller", then exit
if [[ "${current_dir}" != *"/PyDriller" ]]; then
   echo "Please run the script from the '/PyDriller' directory with the command './Scripts/generate_zip_files.sh'."
   exit 1 # Exit the script with an error code
fi

# Get the list of repository names (directories only) from the ./repositories directory and sort them
repositories=($(find ./repositories -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort))

# Print the list of repositories
echo "List of repositories: ${repositories[@]}"

# Define the list of subfolders
subfolders=("ck_metrics" "diffs" "metrics_data" "metrics_evolution" "metrics_predictions" "metrics_statistics" "progress" "refactorings" "repositories")

# Create a "compressed" directory if it does not exist
if [[ ! -d "compressed/" ]]; then
   echo "Creating the compressed directory in the current path..."
   mkdir -p "compressed" # Create the directory
fi

# Loop through the repository names found in ./repositories
for repo_name in "${repositories[@]}"; do
   folders_list=("")  # Clear the folders_list variable

   # Loop through the subfolders
   for folder in "${subfolders[@]}"; do
      if [[ -d "./${folder}/${repo_name}" ]]; then  # Check if the subfolder exists for the repository
         folders_list+=("./${folder}/${repo_name}/")  # Add the folder to the list if it exists
      fi
   done

   # Add the commit list file if it exists
   if [[ -e "./${subfolders[0]}/${repo_name}-commits_list.csv" ]]; then
      folders_list+=("./${subfolders[0]}/${repo_name}-commits_list.csv")
   fi

   if [[ ${#folders_list[@]} -gt 1 ]]; then  # Proceed only if there are valid folders/files to zip
      echo "Creating a zip file for the ${repo_name} repository..."

      # Create a zip file for the repository
      zip -r "./compressed/${repo_name}.zip" "${folders_list[@]}"
   else
      echo "No valid folders or files to zip for the ${repo_name} repository."
   fi
done

# Play a sound when the script finishes
sound_file="./../../.assets/Sounds/NotificationSound.wav"

if [[ -e "$sound_file" ]]; then
   aplay "$sound_file" # Play the sound file
else
   echo "Sound file not found at: $sound_file"
fi

# Print a success message
echo "Zip files created successfully."
