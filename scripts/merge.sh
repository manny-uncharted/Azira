#!/bin/bash

## This file is a script to merge the current branch into another branch in the current git repository.

# Show current branch and also show all branches
current_branch=$(git symbolic-ref --short HEAD)
all_branches=$(git branch)
echo "Current branch: $current_branch"
echo "All branches: $all_branches"

# Ask user for the destination branch
read -p "Enter the name of the destination branch to merge into: " destination_branch

# Confirm the merge operation
read -p "Are you sure you want to merge '$current_branch' into '$destination_branch'? (y/n): " answer

if [[ $answer == "y" || $answer == "Y" ]]; then
  # Checkout the destination branch
  git checkout "$destination_branch"
  echo "Switched to branch '$destination_branch'."

  # Merge the current branch into the destination branch
  git merge "$current_branch"
  echo "Merged '$current_branch' into '$destination_branch'."

  # Push the changes (optional)
  read -p "Do you want to push the changes to the remote repository? (y/n): " push_answer

  if [[ $push_answer == "y" || $push_answer == "Y" ]]; then
    git push origin "$destination_branch"
  fi

else
  echo "Merge canceled."
fi
