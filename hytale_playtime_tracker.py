import psutil
import time
import json
import os
import shutil
import re
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# === PATHS ===
LOG_PATH = r'C:\Users\sonof\AppData\Roaming\Hytale\UserData\Logs' 
TRACKER_DIR = r'C:\Users\sonof\Documents\HytaleTracker'
BACKUP_DIR = os.path.join(TRACKER_DIR, "Log_Backups")
DATA_FILE = os.path.join(TRACKER_DIR, "hytale_playtime.json")
CSV_FILE = os.path.join(TRACKER_DIR, "hytale_sessions.csv")
GAME_PROCESS_NAME = "HytaleClient.exe"

# Ensure folders exist
for folder in [TRACKER_DIR, BACKUP_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"total_seconds": 0, "session_count": 0, "processed_logs": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_to_csv(start_dt, end_dt, duration_seconds):
    """Writes the session details into the CSV file."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Start Time", "End Time", "Duration (Mins)"])
        
        writer.writerow([
            start_dt.strftime("%Y-%m-%d"),
            start_dt.strftime("%H:%M:%S"),
            end_dt.strftime("%H:%M:%S"),
            round(duration_seconds / 60, 2)
        ])

def sync_and_backup_logs(data):
    if not os.path.exists(LOG_PATH):
        return data
    new_seconds = 0
    for filename in os.listdir(LOG_PATH):
        if filename.endswith(".log") and filename not in data.get("processed_logs", []):
            src = os.path.join(LOG_PATH, filename)
            dst = os.path.join(BACKUP_DIR, filename)
            try:
                with open(src, 'r', errors='ignore') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        start_m = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', lines[0])
                        end_m = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', lines[-1])
                        if start_m and end_m:
                            s_dt = datetime.strptime(start_m.group(1), "%Y-%m-%d %H:%M:%S")
                            e_dt = datetime.strptime(end_m.group(1), "%Y-%m-%d %H:%M:%S")
                            new_seconds += (e_dt - s_dt).total_seconds()
                shutil.copy2(src, dst)
                if "processed_logs" not in data: data["processed_logs"] = []
                data["processed_logs"].append(filename)
            except:
                continue
    data["total_seconds"] += int(new_seconds)
    return data

def show_popup(session_seconds, total_seconds, session_num):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    s_mins = int(session_seconds // 60)
    t_hrs = int(total_seconds // 3600)
    t_mins = int((total_seconds % 3600) // 60)
    message = (f"🎮 Hytale Session #{session_num} Summary\n"
               f"---------------------------\n"
               f"This session: {s_mins} minutes\n"
               f"Lifetime total: {t_hrs}h {t_mins}m")
    messagebox.showinfo("Hytale Tracker", message)
    root.destroy()

def is_game_running():
    for proc in psutil.process_iter(['name']):
        try:
            # Convert name to lowercase to avoid capitalization issues
            p_name = proc.info['name'].lower()
            
            # 1. Must contain "hytale"
            # 2. Must NOT contain "launcher"
            # 3. Must NOT be the tracker itself (.exe or .py)
            if "hytale" in p_name and "launcher" not in p_name and "tracker" not in p_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def main():
    data = load_data()
    data = sync_and_backup_logs(data)
    save_data(data)
    session_active = False
    start_dt = None

    while True:
        game_active = is_game_running()
        if game_active and not session_active:
            session_active = True
            start_dt = datetime.now() # Capture start time
            data["session_count"] = data.get("session_count", 0) + 1
            save_data(data)
        elif not game_active and session_active:
            end_dt = datetime.now() # Capture end time
            elapsed = int((end_dt - start_dt).total_seconds())
            data["total_seconds"] += elapsed
            
            # Sync logs, then Save data, then LOG TO CSV
            data = sync_and_backup_logs(data)
            save_data(data)
            log_to_csv(start_dt, end_dt, elapsed) # THIS LINE UPDATES THE CSV
            
            show_popup(elapsed, data["total_seconds"], data["session_count"])
            session_active = False
        time.sleep(15)

if __name__ == "__main__":
    main()