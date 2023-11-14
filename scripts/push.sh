#!/bin/bash

## This file is a script to push to the current branch in the current git repository.

# Pull from the 'main' branch
git pull origin main

# Show current branch
current_branch=$(git symbolic-ref --short HEAD)
echo "Current branch: $current_branch"

# Ask user if they want to push to the current branch
read -p "Do you want to push to the current branch? (y/n): " answer

if [[ $answer == "y" || $answer == "Y" ]]; then
  # Perform git add
  git add --all

  # Ask for commit message
  read -p "Enter commit message: " commit_message

  # Commit and push to the current branch
  git commit -m "$commit_message"
  git push origin "$current_branch"
else
  # Ask user to specify the branch to push to
  read -p "Enter the branch you want to push to: " branch

  # Switch to the specified branch
  git checkout "$branch"

  # Ask for commit message
  read -p "Enter commit message: " commit_message

  # Perform git add, commit, and push to the specified branch
  git add --all
  git commit -m "$commit_message"
  git push origin "$branch"
fi
