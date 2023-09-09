#!/bin/bash

# Run:
# chmod +x ./moveExtractedFiles.sh
# ./moveExtractedFiles.sh

# Define the source and destination folder names
source_folders=("Commons Lang" "Kafka" "JabRef" "ZooKeeper")
destination_folders=("ck_metrics" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# Loop through the source folders and move their contents
for source_folder in "${source_folders[@]}"; do
   # Loop through the destination folders and move the contents
   for destination_folder in "${destination_folders[@]}"; do
      # Create the destination folder if it doesn't exist
      mkdir -p "$destination_folder"
      
      # Move the contents from the source to destination folder
      mv "$source_folder/$destination_folder"/* "$destination_folder/"
   done

   # Delete the source folder after moving its contents
   rm -r "$source_folder"
done

echo "Files moved and source folders deleted successfully."