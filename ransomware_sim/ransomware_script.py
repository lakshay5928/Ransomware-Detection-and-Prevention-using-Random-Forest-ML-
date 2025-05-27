
import os
import time
import random

# Folder to simulate ransomware attack
TARGET_FOLDER = "C:\\Users\\yasha\\OneDrive\\Desktop\\ransomware_detector\\monitor\\test_folder"

def create_encrypted_files(num_files=3):
    for i in range(num_files):
        filename = f"encrypted_file_{i}.locky"
        filepath = os.path.join(TARGET_FOLDER, filename)
        with open(filepath, 'w') as f:
            f.write("This file has been encrypted by ransomware simulation.\n")
        print(f"[Created] {filepath}")
        time.sleep(0.5)

def rename_files():
    files = [f for f in os.listdir(TARGET_FOLDER) if os.path.isfile(os.path.join(TARGET_FOLDER, f))]
    for f in files:
        if not f.endswith('.locked') and not f.endswith('.locky'):
            old_path = os.path.join(TARGET_FOLDER, f)
            new_path = old_path + '.locked'
            os.rename(old_path, new_path)
            print(f"[Renamed] {old_path} -> {new_path}")
            time.sleep(0.5)

def lock_files():
    files = [f for f in os.listdir(TARGET_FOLDER) if os.path.isfile(os.path.join(TARGET_FOLDER, f))]
    for f in files:
        if f.endswith('.locked') or f.endswith('.locky'):
            filepath = os.path.join(TARGET_FOLDER, f)
            with open(filepath, 'w') as file:
                file.write("!!! FILE LOCKED BY RANSOMWARE SIMULATION !!!\n")
            print(f"[Locked] {filepath}")
            time.sleep(0.5)

def simulate_attack():
    print("Starting ransomware simulation...")
    create_encrypted_files()
    rename_files()
    lock_files()
    print("Ransomware simulation finished.")

if __name__ == "__main__":
    simulate_attack()

