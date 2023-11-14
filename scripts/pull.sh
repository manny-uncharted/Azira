#!/bin/bash

## This file is a script to pull from the main branch to the current branch in the current git repository.

# Show current branch
current_branch=$(git symbolic-ref --short HEAD)
echo "Current branch: $current_branch"

# Ask user if they want to pull from the main branch to the current branch
read -p "Do you want to pull from the main branch to the $current_branch? (y/n): " answer

if [[ $answer == "y" || $answer == "Y" ]]; then
  # Perform git add
  git add --all

  # Ask for commit message
  read -p "Enter commit message: " commit_message

  # Commits the current changes made on the current branch
  git commit -m "$commit_message"

  # Pulls from the main branch
  git pull origin main

  # Ask user if they want to push the saved changes after pulling
  read -p "Do you want to push the saved changes to the $current_branch? (y/n): " push_answer

  if [[ $push_answer == "y" || $push_answer == "Y" ]]; then
    # Push to the current branch
    git push origin "$current_branch"
  else
    echo "Changes pulled from main branch but not pushed to $current_branch."
  fi

else
  # Ask user to specify the branch to pull from
  read -p "Enter the branch you want to pull from to $current_branch: " branch

  # Perform git add
  git add --all

  # Ask for commit message
  read -p "Enter commit message: " commit_message

  # Commits the current changes made on the current branch
  git commit -m "$commit_message"

  # Pulls from the specified branch
  git pull origin "$branch"

  # Ask user if they want to push the saved changes after pulling
  read -p "Do you want to push the saved changes to $current_branch? (y/n): " push_answer

  if [[ $push_answer == "y" || $push_answer == "Y" ]]; then
    # Push to the current branch
    git push origin "$current_branch"
  else
    echo "Changes pulled from $branch but not pushed to $current_branch."
  fi
fi

