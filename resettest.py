import os

# Path to the folder you want to clean
test_folder ="C:\\Users\\somra\\Desktop\\ransomware_detector\\monitor\\test_folder"

def reset_test_folder():
    if not os.path.exists(test_folder):
        print(f"[!] Folder not found: {test_folder}")
        return

    for filename in os.listdir(test_folder):
        file_path = os.path.join(test_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"[✓] Deleted: {file_path}")
        except Exception as e:
            print(f"[X] Error deleting {file_path}: {e}")

if __name__ == "__main__":
    reset_test_folder()
