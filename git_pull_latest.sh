#!/bin/bash

# accept variables for lab number and section number
LAB=$1
SEC=$2

#set deadline date
#don't forget to set it +3 day from the actual deadline (for late submissions)
#if there're any changes in the lab deadlines, please update them here
# =============================
# lab 1
if [ $LAB -eq 1 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2025-12-05 00:00" # lab 1 sec 1
elif [ $LAB -eq 1 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2025-12-08 00:00" # lab 1 sec 2
elif [ $LAB -eq 2 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2025-12-11 00:00" # lab 2 sec 1
elif [ $LAB -eq 2 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2025-12-14 00:00" # lab 2 sec 2
# elif [ $LAB -eq 3 ] && [ $SEC -eq 1 ]; then
#   DEADLINE="2025-12-30 00:00" # lab 3 sec 1 (EXPECTED)
# elif [ $LAB -eq 3 ] && [ $SEC -eq 2 ]; then
#   DEADLINE="2026-01-04 00:00" # lab 3 sec 2 (EXPECTED)
else
  echo "Please set the correct LAB and SEC variables, or update the deadlines in the script."
  exit 1
fi

# =============================

# Read the file line by line
while IFS=';' read -r student_id repo_url; do
  # Extract the directory name from the repo URL
  repo_name=$(basename "$repo_url" .git)
  
  echo "================================"
  echo "$student_id"
  # Check if the directory already exists
  if [ -d "$student_id" ]; then
    echo "Directory $student_id already exists. Resetting and fetching latest version."
    cd "$student_id"
    git reset --hard
    git pull
    # don't forget to checkout the latest commit before the deadline
    git checkout `git rev-list -n 1 --first-parent --before="$DEADLINE" main`
    cd ..
  else
    echo "Cloning $repo_url into $student_id"
    git clone "$repo_url" "$student_id"
    cd "$student_id"
    git checkout `git rev-list -n 1 --first-parent --before="$DEADLINE" main`
    
    cd ..
  fi
  echo "Current commit ID:"
  git rev-parse HEAD
  echo "==============================="
done < ./git-sec${SEC}.txt