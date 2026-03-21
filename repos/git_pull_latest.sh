#!/bin/bash
# accept variables for lab number and section number
LAB=$1
SEC=$2

# accept variables for lab number and section number
if [ -z "$LAB" ] || [ -z "$SEC" ]; then
  echo "Usage: $0 <lab_number> <section_number>"
  exit 1
fi
#set deadline date
#don't forget to set it +3 day from the actual deadline (for late submissions)
#if there're any changes in the lab deadlines, please update them here
# =============================
if [ $LAB -eq 1 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2025-12-05 00:00" 
elif [ $LAB -eq 1 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2025-12-08 00:00" 
elif [ $LAB -eq 2 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2025-12-11 00:00" 
elif [ $LAB -eq 2 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2025-12-14 00:00" 
elif [ $LAB -eq 3 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2025-12-19 00:00" 
elif [ $LAB -eq 3 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2025-12-22 00:00" 
elif [ $LAB -eq 4 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2025-12-26 00:00" 
elif [ $LAB -eq 4 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2025-12-29 00:00" 
elif [ $LAB -eq 5 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-01-09 00:00" 
elif [ $LAB -eq 5 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-01-12 00:00" 
elif [ $LAB -eq 6 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-01-26 00:00" 
elif [ $LAB -eq 6 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-01-26 00:00" 
elif [ $LAB -eq 7 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-02-06 00:00" 
elif [ $LAB -eq 7 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-02-09 00:00" 
elif [ $LAB -eq 8 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-02-13 00:00" 
elif [ $LAB -eq 8 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-02-16 00:00" 
elif [ $LAB -eq 9 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-02-20 00:00" 
elif [ $LAB -eq 9 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-02-23 00:00" 
elif [ $LAB -eq 10 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-03-06 00:00" 
elif [ $LAB -eq 10 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-03-09 00:00"
elif [ $LAB -eq 11 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-03-16 00:00" 
elif [ $LAB -eq 11 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-03-16 00:00" 
elif [ $LAB -eq 12 ] && [ $SEC -eq 1 ]; then
  DEADLINE="2026-03-23 00:00" 
elif [ $LAB -eq 12 ] && [ $SEC -eq 2 ]; then
  DEADLINE="2026-03-23 00:00" 
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
    git reset --hard HEAD
    git pull origin main
    # don't forget to checkout the latest commit before the deadline
    git checkout `git rev-list -n 1 --first-parent --before="$DEADLINE" main`
    cd ..
  else
    echo "Cloning $repo_url into $student_id"
    git clone "$repo_url" "$student_id" # check if the clone was successful
    if [ $? -ne 0 ]; then
      echo "Failed to clone $repo_url. Please check the URL or your network connection."
      continue
    fi

    cd "$student_id"
    git checkout `git rev-list -n 1 --first-parent --before="$DEADLINE" main`
    
    cd ..
  fi
  echo "Current commit ID:"
  git rev-parse HEAD
  echo "================================"
done < ./sec${SEC}.txt
