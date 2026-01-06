import os
import sys
import subprocess
import glob
import shlex

# ไฟล์เป้าหมายสำหรับ Lab 3
TARGET_FILES = [
    "ConfigurableRPS.java",
    "ConfigurableRPSGames.java", 
    "MultiplicationTable.java",
    "PatternMaker.java",
    "GeometryCalculator.java"
]

current_cwd = os.getcwd()

def press_key():
    """รอให้ผู้ใช้กด Enter หรือพิมพ์ 'q' เพื่อออก"""
    key = input("Press Enter to continue to the next file, or type 'q' to quit: ")
    if key.lower() == "q":
        print("Quitting...")
        sys.exit(0)

def process_directory(student_id):
    """ประมวลผลไดเรกทอรีของนักศึกษา"""
    student_id = f"../repos/{student_id}"
    if not os.path.isdir(student_id):
        print(f"Directory '{student_id}' does not exist. Skipping...")
        return

    print(f"\nChanging into directory {student_id}")
    original_dir = os.getcwd()
    os.chdir(student_id)

    # Removing Pre-compiled .class files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".class"):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error removing {os.path.join(root, file)}: {e}")

    # ประมวลผลแต่ละไฟล์เป้าหมาย
    for TARGET_FILE in TARGET_FILES:
        process_target_file(TARGET_FILE, student_id)
        
    os.chdir(original_dir)

def process_target_file(TARGET_FILE, student_id):
    """ประมวลผลไฟล์เป้าหมายแต่ละไฟล์"""
    print(f"\nLooking for {TARGET_FILE}...")
    
    # ค้นหาไฟล์แบบ recursive
    found_files = []
    for root, dirs, files in os.walk("."):
        if TARGET_FILE in files:
            found_files.append(os.path.join(root, TARGET_FILE))
    
    if not found_files:
        print(f"File {TARGET_FILE} not found in {student_id}.")
        response = input("Would you like to try again? (y/n): ")
        if response.lower() != "n":
            # ลองค้นหาอีกครั้ง
            for root, dirs, files in os.walk("."):
                if TARGET_FILE in files:
                    found_files.append(os.path.join(root, TARGET_FILE))
        
        if not found_files:
            print(f"Skipping {TARGET_FILE}...")
            return
    
    # ประมวลผลแต่ละไฟล์ที่พบ
    for target_file in found_files:
        compile_and_run(target_file, TARGET_FILE)

def compile_and_run(target_file, TARGET_FILE):
    """คอมไพล์และรันโปรแกรม"""
    print(f"\nFound {target_file}. Compiling...")
    
    compile_proc = subprocess.run(
        ["javac", "-cp", ".", target_file],
        capture_output=True,
        text=True
    )
    
    if compile_proc.returncode != 0:
        print(f"Compilation failed for {target_file}.")
        print("Error output:")
        print(compile_proc.stderr)
        response = input("Would you like to try again compiling? (y/n): ")
        if response.lower() == "y":
            compile_proc = subprocess.run(
                ["javac", "-cp", ".", target_file],
                capture_output=True,
                text=True
            )
            if compile_proc.returncode != 0:
                print("Compilation failed again. Skipping...")
                return
        else:
            return
    
    print("Compilation successful. Running the program...")
    
    # เตรียมพาธสำหรับ test cases
    # แก้ไขพาธให้ตรงกับโครงสร้างไดเรกทอรีของคุณ
    input_dir = f"D:/Work/TA adcom2025/ACP/lab3/{TARGET_FILE.replace('.java', '')}/"
    
    if not os.path.isdir(input_dir):
        print(f"No input directory found: {input_dir} for {TARGET_FILE}. Skipping execution...")
    else:
        run_test_cases(target_file, input_dir)

def run_test_cases(target_file, input_dir):
    """รัน test cases จากไฟล์"""
    in_files = sorted(glob.glob(os.path.join(input_dir, "*.in")))
    arg_files = sorted(glob.glob(os.path.join(input_dir, "*.arg")))
    
    test_count = 0
    passed_count = 0
    
    # รัน test cases ที่ใช้ input file
    if in_files:
        for input_file in in_files:
            test_count += 1
            print(f"\nRunning with input file {input_file}...")
            
            try:
                passed = run_with_input_file(target_file, input_file)
                if passed:
                    passed_count += 1
            except Exception as e:
                print(f"Error in test: {e}")
    
    # รัน test cases ที่ใช้ command line arguments
    if arg_files:
        for arg_file in arg_files:
            test_count += 1
            print(f"\nRunning with argument file {arg_file}...")
            
            try:
                passed = run_with_arg_file(target_file, arg_file)
                if passed:
                    passed_count += 1
            except Exception as e:
                print(f"Error in test: {e}")
    
    # แสดงผลสรุป
    if test_count > 0:
        print(f"\nTest Summary: {passed_count}/{test_count} tests passed")
    else:
        print("\nNo test cases found.")

def run_with_input_file(target_file, input_file):
    """รันโปรแกรมด้วย input file"""
    class_name = target_file.lstrip("./").lstrip("\\")
    
    # อ่าน input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return False
    
    # วิธีที่ 1: ใช้ stdin โดยตรง (น่าเชื่อถือกว่า shell redirect)
    try:
        proc = subprocess.run(
            ["java", "-cp", ".", class_name],
            input=input_content,
            encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
    except subprocess.TimeoutExpired:
        print("⚠️ Program timeout (30 seconds)")
        return False
    except Exception as e:
        print(f"Error running program: {e}")
        return False
    
    print("========[Output]========")
    print(proc.stdout.strip())
    print("========================")
    
    if proc.stderr:
        print("========[Error]=========")
        print(proc.stderr.strip())
        print("========================")
    
    # ตรวจสอบ expected output
    passed = check_expected_output(input_file, proc)
    
    return passed

def run_with_arg_file(target_file, arg_file):
    """รันโปรแกรมด้วย command line arguments"""
    class_name = target_file.lstrip("./").lstrip("\\")
    
    # อ่าน arguments
    try:
        with open(arg_file, 'r', encoding='utf-8') as f:
            arg_content = f.read().strip()
    except Exception as e:
        print(f"Error reading argument file: {e}")
        return False
    
    # ใช้ shlex.split() เพื่อแยก arguments อย่างถูกต้องตามเครื่องหมาย quotes
    args = shlex.split(arg_content) if arg_content else []
    
    # รันโปรแกรม
    try:
        proc = subprocess.run(
            ["java", "-cp", ".", class_name] + args,
            encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
    except subprocess.TimeoutExpired:
        print("⚠️ Program timeout (30 seconds)")
        return False
    except Exception as e:
        print(f"Error running program: {e}")
        return False
    
    print("========[Output]========")
    print(proc.stdout.strip())
    print("========================")
    
    if proc.stderr:
        print("========[Error]=========")
        print(proc.stderr.strip())
        print("========================")
    
    # ตรวจสอบ expected output
    passed = check_expected_output_arg(arg_file, proc)
    
    return passed

def check_expected_output(input_file, proc):
    """ตรวจสอบ output ที่คาดหวัง"""
    passed = True
    expected_output_file = input_file[:-3] + ".out"
    
    if os.path.isfile(expected_output_file):
        with open(expected_output_file, 'r', encoding='utf-8') as f:
            expected_output = f.read()
        
        if proc.stdout.strip() == expected_output.strip():
            print("✅Output")
        else:
            print("⚠️Output")
            passed = False
    
    expected_error_file = input_file[:-3] + ".err"
    if os.path.isfile(expected_error_file):
        with open(expected_error_file, 'r', encoding='utf-8') as f:
            expected_error = f.read()
        
        if proc.stderr.strip() == expected_error.strip():
            print("✅Error")
        else:
            print("⚠️Error")
            passed = False
    
    return passed

def check_expected_output_arg(arg_file, proc):
    """ตรวจสอบ output ที่คาดหวังสำหรับ argument file"""
    passed = True
    expected_output_file = arg_file[:-4] + ".out"
    
    if os.path.isfile(expected_output_file):
        with open(expected_output_file, 'r', encoding='utf-8') as f:
            expected_output = f.read()
        
        if proc.stdout.strip() == expected_output.strip():
            print("✅Output")
        else:
            print("⚠️Output")
            passed = False
    
    expected_error_file = arg_file[:-4] + ".err"
    if os.path.isfile(expected_error_file):
        with open(expected_error_file, 'r', encoding='utf-8') as f:
            expected_error = f.read()
        
        if proc.stderr.strip() == expected_error.strip():
            print("✅Error")
        else:
            print("⚠️Error")
            passed = False
    
    return passed

def run_interactive(target_file):
    """รันโปรแกรมแบบ interactive"""
    class_name = target_file.lstrip("./").lstrip("\\")
    print(f"\nRunning {class_name} interactively...")
    print("(The program will run and you can interact with it)")
    print("-" * 50)
    
    try:
        subprocess.run(["java", "-cp", ".", class_name])
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

def main():
    """ฟังก์ชันหลัก"""
    while True:
        student_id = input("Enter the directory (student ID) to run, or type 'q' to quit: ").strip()
        
        if student_id.lower() == "q":
            print("Quitting...")
            break
        
        process_directory(student_id)
    
    print("All tasks completed.")

if __name__ == "__main__":
    main()