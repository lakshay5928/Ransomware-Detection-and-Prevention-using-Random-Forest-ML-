import os
from plyer import notification
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from monitor.file_monitor import monitor_folder
import threading
import winsound

class RansomwarePreventionGUI:
    def __init__(self, log_file="prevention_log.txt"):
        self.log_file = os.path.abspath(log_file)

        # GUI setup
        self.root = tk.Tk()
        self.root.title("Ransomware Prevention")
        self.root.geometry("500x300")
        self.root.configure(bg="#fff")

        self.label = tk.Label(
            self.root,
            text="Waiting for ransomware detection...",
            font=("Arial", 14),
            bg="#fff",
            fg="black"
        )
        self.label.pack(pady=40)

        self.details = tk.Text(self.root, height=8, width=50)
        self.details.pack(pady=10)
        self.details.configure(state='disabled')

    def log_action(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_file, "a") as log:
            log.write(log_entry)
        print(log_entry.strip())
        self.update_gui(log_entry)

    def update_gui(self, message):
        self.details.configure(state='normal')
        self.details.insert(tk.END, message)
        self.details.see(tk.END)
        self.details.configure(state='disabled')

    def show_alert(self, message):
        try:
            notification.notify(
                title="🚨 Ransomware Alert!",
                message=message,
                timeout=5
            )
        except Exception as e:
            print(f"[!] Alert failed: {e}")

    def on_detection(self, filepath=None, event_type=None):
        # Play alert sound
        try:
            winsound.PlaySound("alert.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[!] Could not play sound: {e}")

        # Update label with red warning
        self.label.config(
            text="⚠ Ransomware detected!",
            fg="red"
        )
        message = f"Detected ransomware file ({event_type}): {filepath}\n"
        self.log_action(message)
        self.show_alert(f"Ransomware detected in file: {os.path.basename(filepath)}")

    def run(self):
        # Start monitor thread with callback
        monitor_thread = threading.Thread(target=monitor_folder, args=(self.on_detection,), daemon=True)
        monitor_thread.start()
        self.root.mainloop()


# Entry point
if __name__ == "_main_":
    gui = RansomwarePreventionGUI()
    gui.run()