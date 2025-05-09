import time
import psutil
from datetime import datetime
import win32gui
import win32process
import pandas as pd
import os
from sklearn.model_selection import train_test_split

DATA_FILE_PATH = "Kouri_learning_logs.xlsx"
MAX_TIME_ON_APP = 30

if os.path.exists(DATA_FILE_PATH):
    df = pd.read_excel(DATA_FILE_PATH)
else:
    df = pd.DataFrame(columns=["app_name", "timestamp", "elapsed_time"])

def get_active_app():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    app_name = process.name()
    print(f"Active app name: {app_name}")
    return {
        "app_name": app_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

current_app = None
start_time = None
elapsed_time = None

print("Starting....")
print(f"Logs will be saved to {DATA_FILE_PATH}")

while True:
    app_info = get_active_app()
    print(app_info)
    time.sleep(10)

    """
        *** GOES AT THE BOTTOM OF THE IF, di ko muna nilagay para di mag pause yung scanning every 30 seconds of idle time on the app***
        
        if elapsed_time >= MAX_TIME_ON_APP:
            print(f"PAUSING TRACKER: stayed on {app_info['app_name']} for {elapsed_time} seconds")
            while current_app == app_info["app_name"]:
                time.sleep(1)
            print(f"RESUMED TRACKING: app changed to {app_info['app_name']}")
            start_time = datetime.now()
        new_row = {
            "app_name": app_info["app_name"],
            "timestamp": app_info["timestamp"],
            "elapsed_time": elapsed_time
        }
        df.loc[len(df)] = new_row
    """

    if current_app == app_info["app_name"]:
        elapsed_time = (datetime.now() - start_time).seconds
    else:
        current_app = app_info["app_name"]
        start_time = datetime.now()
        print(f"App Switched to {app_info}")
        new_row = {
            "app_name": app_info["app_name"],
            "timestamp": app_info["timestamp"],
            "elapsed_time": elapsed_time
        }
        df.loc[len(df)] = new_row

    with pd.ExcelWriter(DATA_FILE_PATH, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, index=False, sheet_name="App Usage logs")
        frequency_table = df["app_name"].value_counts().reset_index()
        frequency_table.columns = ["app_name", "launch_count"]
        frequency_table.to_excel(writer, index=False, sheet_name="App Frequency Table")

    print(f"Updated log and frequency table saved to {DATA_FILE_PATH}")