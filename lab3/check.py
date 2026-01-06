import os
import sys
import subprocess
import glob
import shlex

# Lab 3 Target Files
TARGETS = [
    {"filename": "ConfigurableRPS.java", "mode": "manual", "repeat": 4},
    {"filename": "ConfigurableRPSGames.java", "mode": "manual"},
    {"filename": "MultiplicationTable.java", "mode": "auto_args", "args_list": [["8"], ["-1"], ["0"], ["15"]]},
    {"filename": "PatternMaker.java", "mode": "manual","repeat": 2},
    {"filename": "GeometryCalculator.java", "mode": "manual","repeat": 2}
]
current_cwd = os.getcwd()

def press_key():
    key = input("Press Enter to continue to the next file, or type 'q' to quit: ")
    if key.lower() == "q":
        print("Quitting...")
        sys.exit(0)

def process_directory(student_id):
    student_path = f"../repos/{student_id}"
    if not os.path.isdir(student_path):
        print(f"Directory '{student_path}' does not exist. Skipping...")
        return

    print(f"\nChanging into directory {student_path}")
    original_dir = os.getcwd()
    os.chdir(student_path)

    #Removing Pre-compiled .class files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".class"):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error removing {os.path.join(root, file)}: {e}")

    for target_config in TARGETS:
        target_filename = target_config["filename"]
        # Recursively find target file(s)
        found_files = []
        for root, dirs, files in os.walk("."):
            if target_filename in files:
                found_files.append(os.path.join(root, target_filename))
        
        while not found_files:
            print(f"File {target_filename} not found in {student_path}.")
            response = input("Would you like to try again? (y/n): ")
            if response.lower() == "n":
                break
            # Optional: Allow user to search for a different file name if needed, 
            # though this overrides the config for this iteration.
            manual_search = input("Enter the file name to search (or empty to skip): ")
            if not manual_search:
                break
            
            target_filename = manual_search
            for root, dirs, files in os.walk("."):
                if target_filename in files:
                    found_files.append(os.path.join(root, target_filename))
        else:
            for target_file in found_files:
                input(f"Found {target_file}. Press Enter to compile and run...")
                print(f"\nCompiling {target_file}...")
                compile_proc = subprocess.run(["javac", "-cp", ".", target_file])
                
                while compile_proc.returncode != 0:
                    print(f"Compilation failed for {target_file}.")
                    response = input("Would you like to try again compiling? (y/n): ")
                    if response.lower() == "n":
                        break
                    compile_proc = subprocess.run(["javac", "-cp", ".", target_file])
                else:
                    print("Compilation successful.")
                    
                    # Convert file path to package name / class name logic
                    norm_path = os.path.normpath(target_file)
                    if norm_path.endswith(".java"):
                         class_path = norm_path[:-5]
                    else:
                         class_path = norm_path
                    class_name = class_path.replace(os.path.sep, ".")
                    
                    print("---------------------------------------------------------")
                    
                    repeat_count = target_config.get("repeat", 1)
                    for i in range(repeat_count):
                        run_display = f" (Run {i+1}/{repeat_count})" if repeat_count > 1 else ""
                        
                        if target_config.get("mode") == "auto_args":
                            print(f"Running {target_filename} AUTOMATICALLY with arguments...{run_display}")
                            args_list = target_config.get("args_list", [])
                            print(f"\n>>> Input Args: ")
                            try:
                                subprocess.run(["java", "-cp", ".", class_name])
                            except Exception as e:
                                print(f"Error running execution: {e}")
                            for args in args_list:
                                print(f"\n>>> Input Args: {' '.join(args)}")
                                try:
                                    subprocess.run(["java", "-cp", ".", class_name] + args)
                                except Exception as e:
                                    print(f"Error running execution: {e}")
                        else:
                            print(f"Running {target_filename} INTERACTIVELY...{run_display}")
                            print("Please enter input manually.")
                            try:
                                subprocess.run(["java", "-cp", ".", class_name])
                            except KeyboardInterrupt:
                                print("\nProgram interrupted by user.")
                        
                        if i < repeat_count - 1:
                            print("\n---------------------------------------------------------")
                    
                    print("---------------------------------------------------------")
                        
    os.chdir(original_dir)

def main():
    while True:
        student_id = input("Enter the directory (student ID) to run, or type 'q' to quit: ").strip()
        if student_id.lower() == "q":
            print("Quitting...")
            break
        process_directory(student_id)

    print("All tasks completed.")

if __name__ == "__main__":
    main()
