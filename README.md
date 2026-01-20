Hytale Playtime Tracker (2026)
A lightweight, automated background utility designed for Hytale players to track their lifetime gameplay hours. This tool bypasses launcher limitations by monitoring the game engine directly, providing accurate session summaries and permanent log backups.

✨ Features
Automatic Tracking: Detects when Hytale starts and stops without manual input.

Session Summaries: Displays a popup notification after every session showing your time played and lifetime total.

Future-Proof: Smart process detection ignores the launcher and adapts to game updates automatically.

Data Integrity: Automatically backs up Hytale logs to a safe directory to prevent the launcher from rotating/deleting your history.

Cloud Sync Ready: Designed to work perfectly with Dropbox/OneDrive for multi-PC syncing.

Portable Design: Works on any Windows machine without modifying the source code.

🚀 Installation
Option 1: The Quick Start (Recommended)
Go to the Releases page and download hytale_tracker.exe.

Press Win + R, type shell:startup, and press Enter.

Place a shortcut of the .exe in that folder to ensure it starts with Windows.

Option 2: Run from Source
If you prefer running the Python script directly:

Install Python 3.x and the required library:

Bash

pip install psutil
Run the script:

Bash

python hytale_tracker.py
☁️ Syncing Across Multiple PCs (Dropbox)
To keep your playtime unified across your Desktop and Laptop, follow these steps to create a Symbolic Link:

Move the Documents/HytaleTracker folder into your Dropbox.

Delete the empty folder from your Documents.

Open Command Prompt as Administrator and run:

DOS

mklink /D "%USERPROFILE%\Documents\HytaleTracker" "C:\Users\YOUR_NAME\Dropbox\HytaleTracker"
(Replace YOUR_NAME and the Dropbox path with your actual local paths.)

📊 Data Files
The tracker stores all data in %USERPROFILE%\Documents\HytaleTracker:

hytale_playtime.json: Your master record (Total hours & session count).

hytale_sessions.csv: A timestamped history of every play session (Open with Excel).

Log_Backups/: Permanent copies of your Hytale game logs.

🛡️ Privacy & Security
Transparency: This tool is open-source. You can audit the hytale_tracker.py to see exactly how it interacts with your system.

Process Monitoring: The script uses the psutil library to see if HytaleClient.exe is running. It does not read your screen or log your keystrokes.

Note: Some Antivirus software may flag the standalone .exe as a false positive because it monitors active processes. If this occurs, you can run the script directly from the Python source code.

⚖️ License
Distributed under the MIT License. See LICENSE for more information.
