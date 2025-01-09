#!/bin/bash

# How to Run
# chmod +x update_branch.sh
# ./update_branch.sh


# Checkout to batch-processing branch
git checkout batch-processing

# Pull the latest changes from the main branch
git fetch origin
git merge origin/main

# Push changes to the batch-processing branch (optional)
git push origin batch-processing

echo "Batch-processing branch is updated with the latest from main."
