import os
import sys
import subprocess
import glob
import shlex

# แก้ให้ตรงกับแล็บตัวเอง
TARGET_FILES = ["ArrayStats.java"]
current_cwd = os.getcwd()

def press_key():
    key = input("Press Enter to continue to the next file, or type 'q' to quit: ")
    if key.lower() == "q":
        print("Quitting...")
        sys.exit(0)

def process_directory(student_id):
    student_id = f"../repos/{student_id}"
    if not os.path.isdir(student_id):
        print(f"Directory '{student_id}' does not exist. Skipping...")
        return

    print(f"\nChanging into directory {student_id}")
    original_dir = os.getcwd()
    os.chdir(student_id)

    #Removing Pre-compiled .class files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".class"):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error removing {os.path.join(root, file)}: {e}")

    for TARGET_FILE in TARGET_FILES:
        # Recursively find target file(s)
        found_files = []
        for root, dirs, files in os.walk("."):
            if TARGET_FILE in files:
                found_files.append(os.path.join(root, TARGET_FILE))
        while not found_files:
            print(f"File {TARGET_FILE} not found in {student_id}.")
            response = input("Would you like to try again? (y/n): ")
            if response.lower() == "n":
                break
            for root, dirs, files in os.walk("."):
                if TARGET_FILE in files:
                    found_files.append(os.path.join(root, TARGET_FILE))
        else:
            for target_file in found_files:
                print(f"\nFound {target_file}. Compiling...")
                compile_proc = subprocess.run(["javac", "-cp", ".", target_file])
                while compile_proc.returncode != 0:
                    print(f"Compilation failed for {target_file}.")
                    response = input("Would you like to try again compiling? (y/n): ")
                    if response.lower() == "n":
                        break
                    compile_proc = subprocess.run(["javac", "-cp", ".", target_file])
                else:
                    print("Compilation successful. Running the program...")
                
                    # The input directory is located one level up from current folder,
                    # with the folder name equal to TARGET_FILE's basename (without .java)
                    input_dir = f"{current_cwd}/{TARGET_FILE}"
                    # input_dir = f"D:/Work/TA adcom2025/ACP/lab2/{TARGET_FILE}/"
                    
                    if not os.path.isdir(input_dir):
                        print(f"No input directory found: {input_dir} for {TARGET_FILE}. Skipping execution...")
                    else:
                        in_files = glob.glob(os.path.join(input_dir, "*.in"))
                        arg_files = glob.glob(os.path.join(input_dir, "*.arg"))
                        out_files = glob.glob(os.path.join(input_dir, "*.out"))
                        if in_files:
                            in_files.sort()
                            for input_file in in_files:
                                print(f"Running with input file {input_file}...")
                                # If windows, take this
                                class_name = target_file.lstrip("./").lstrip("\\") #.replace("/", ".")
                                proc = subprocess.run(f"java -cp . {class_name} < {input_file}", encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                                print("========[Output]========\n", proc.stdout.strip(), "\n========================")
                                if proc.stderr:
                                    print("=========[Error]========\n", proc.stderr.strip(), "\n=======================")
                                
                                expected_output_file = input_file[:-3] + ".out"
                                if os.path.isfile(expected_output_file):
                                    with open(expected_output_file, 'r', encoding='utf-8') as ef:
                                        expected_output = ef.read()
                                    if proc.stdout.strip() == expected_output.strip():
                                        print("✅Output")
                                    else:
                                        print("========[Expected]========\n", expected_output.strip(), "\n========================")
                                        print("⚠️Output")
                                expected_error_file = input_file[:-3] + ".err"
                                if os.path.isfile(expected_error_file):
                                    with open(expected_error_file, 'r', encoding='utf-8') as ef:
                                        expected_error = ef.read()
                                    if proc.stderr.strip() == expected_error.strip():
                                        print("✅Error")
                                    else:
                                        print("========[Expected]========\n", expected_error.strip(), "\n===============================")
                                        print("⚠️Error")
                                
                        if arg_files:
                            arg_files.sort()
                            for arg_file in arg_files:
                                print(f"Running with argument file {arg_file}...")
                                with open(arg_file, 'r', encoding='utf-8') as af:
                                    arg_content = af.read().strip()
                                # ใช้ shlex.split() เพื่อแยก arguments อย่างถูกต้องตามเครื่องหมาย quotes
                                args = shlex.split(arg_content) # ใช้ shlex.split() เพื่อแยก arguments อย่างถูกต้องตามเครื่องหมาย quotes
                                class_name = target_file.lstrip("./").lstrip("\\") #.replace("/", ".")
                                proc = subprocess.run(["java", "-cp", ".", class_name] + args, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                print("========[Output]========\n", proc.stdout.strip(), "\n========================")
                                if proc.stderr:
                                    print("========[Error]=========\n", proc.stderr.strip(), "\n=======================")
                                
                                expected_output_file = arg_file[:-4] + ".out"
                                if os.path.isfile(expected_output_file):
                                    with open(expected_output_file, 'r', encoding='utf-8') as ef:
                                        expected_output = ef.read()
                                    if proc.stdout.strip() == expected_output.strip():
                                        print("✅Output")
                                    else:
                                        print("⚠️Output")
                                expected_error_file = arg_file[:-4] + ".err"
                                if os.path.isfile(expected_error_file):
                                    with open(expected_error_file, 'r', encoding='utf-8') as ef:
                                        expected_error = ef.read()
                                    if proc.stderr.strip() == expected_error.strip():
                                        print("✅Error")
                                    else:
                                        print("⚠️Error")
                        
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