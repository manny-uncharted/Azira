#!/bin/bash


## This file is a script to create a new branch in the current git repository.

# Show current branch
current_branch=$(git symbolic-ref --short HEAD)
echo "Current branch: $current_branch"

# Ask user for the new branch name
read -p "Enter the name of the new branch: " new_branch

# Create the new branch
git branch "$new_branch"
echo "New branch '$new_branch' created."

# Switch to the new branch
git checkout "$new_branch"
echo "Switched to branch '$new_branch'."

# Push the new branch to remote repository (optional)
read -p "Do you want to push the new branch to the remote repository? (y/n): " push_answer

if [[ $push_answer == "y" || $push_answer == "Y" ]]; then
  git push origin "$new_branch"
fi
