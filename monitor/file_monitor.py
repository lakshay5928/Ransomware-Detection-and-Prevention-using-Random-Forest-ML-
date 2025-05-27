import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import joblib
from utils.features import extract_features
import os
import pandas as pd

MODEL_PATH = "C:\\Users\\yasha\\OneDrive\\Desktop\\ransomware_detector\\model\\ransomware_model.pkl"
WATCH_DIR = "C:\\Users\\yasha\\OneDrive\\Desktop\\ransomware_detector\\monitor\\test_folder"

model = joblib.load(MODEL_PATH)

FEATURE_NAMES = [
    'event_count', 'unique_file', 'total_size_change', 'avg_file_size',
    'entropy', 'txt_ratio', 'exe_ratio', 'encrypted_ratio', 'locky_ratio',
    'created_ratio', 'modified_ratio', 'deleted_ratio'
]

class RansomwareHandler(FileSystemEventHandler):
    def __init__(self, on_detect=None):
        super().__init__()
        self.on_detect = on_detect  # callback to GUI

    def on_created(self, event):
        if not event.is_directory:
            print(f"[+] Created: {event.src_path}")
            self.check_file(event.src_path, event_type='created')

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[~] Modified: {event.src_path}")
            self.check_file(event.src_path, event_type='modified')

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[-] Deleted: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[>] Moved: from {event.src_path} to {event.dest_path}")
            self.check_file(event.dest_path, event_type='moved')

    def check_file(self, filepath, event_type):
        features = extract_features(filepath)
        if features:
            feature_values = [features[feature] for feature in FEATURE_NAMES]
            feature_df = pd.DataFrame([feature_values], columns=FEATURE_NAMES)
            prediction = model.predict(feature_df)[0]
            if prediction == 1:
                print(f"[!!] Ransomware activity detected ({event_type}) in file: {filepath}")
                try:
                    os.remove(filepath)
                    print(f"[X] Suspicious file deleted: {filepath}")
                    # Notify GUI here:
                    if self.on_detect:
                        self.on_detect(filepath=filepath, event_type=event_type)
                except Exception as e:
                    print(f"[!] Could not delete file: {e}")
            else:
                print(f"[OK] File is safe ({event_type}).")

def monitor_folder(on_detect=None):
    event_handler = RansomwareHandler(on_detect=on_detect)
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    print(f"Monitoring started on folder: {WATCH_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_folder()
