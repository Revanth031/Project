import pandas as pd
import csv
from datetime import datetime
import os

def load_patient_data(file_path):
    return pd.read_csv(file_path)

def save_patient_data(file_path, df):
    df.to_csv(file_path, index=False)

def load_note_data(file_path):
    return pd.read_csv(file_path)

def save_note_data(file_path, df):
    df.to_csv(file_path, index=True)
    
def log_usage(username, role, action, status="success", log_file="usage_log.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "username", "role", "action", "status"])
        writer.writerow([timestamp, username, role, action, status])

