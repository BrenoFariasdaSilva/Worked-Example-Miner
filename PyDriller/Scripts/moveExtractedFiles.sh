#!/bin/bash

# Run:
# chmod +x ./moveExtractedFiles.sh
# ./moveExtractedFiles.sh

# Get the current directory
current_dir="$(pwd)"

# Print the current directory
echo "Current directory: ${current_dir}"

# If the current_dir doesn't end with "/PyDriller", then exit
if [[ "${current_dir}" != *"/PyDriller" ]]; then
   echo "Please run the script from the '/PyDriller' with the command './Scripts/moveExtractedFiles.sh'."
   exit # Exit the script
fi

compressed_folder_path="/compressed" # Set the compressed directory

# Define the extraced folder names
extracted_folders=("ck_metrics" "diffs" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# Loop through the destination folders and move the contents
for extracted_folder in "${extracted_folders[@]}"; do
   echo "Moving the contents from ${compressed_folder_path}/${extracted_folder} to ../${extracted_folder}/"

   # If the destination folder doesn't exist, then create it
   if [[ ! -d "../${extracted_folder}" ]]; then
      mkdir "../${extracted_folder}"
   fi
   
   # Move the contents from the source to destination folder
   mv "${compressed_folder_path}/${extracted_folder}"/* "../${extracted_folder}/"

   # Delete the source folder
   rm -rf "${compressed_folder_path}/${extracted_folder:?}"
done

# Play a sound when the script finishes
sound_file="../.assets/NotificationSound.wav"

if [ -e "$sound_file" ]; then
  aplay "$sound_file" # Play the sound file
else
  echo "Sound file not found at: $sound_file"
fi

# Print a success message
echo "Files moved and source folders deleted successfully."