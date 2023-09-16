#!/bin/bash

# Run:
# chmod +x ./generateZipFiles.sh
# ./generateZipFiles.sh

# Define the list of repositories
repositories=("commons-lang" "jabref" "kafka" "zookeeper")

# Define the list of subfolders
subfolders=("ck_metrics" "graphics" "metrics_evolution" "metrics_predictions" "metrics_statistics" "repositories")

# Loop through the repositories
for repo_name in "${repositories[@]}"; do
   echo "${subfolders[@]/%//${repo_name}}"
   # Create a zip file for the repository
   zip -r "${repo_name}.zip" "${subfolders[@]/%//${repo_name}}"
done

echo "Zip files created successfully."