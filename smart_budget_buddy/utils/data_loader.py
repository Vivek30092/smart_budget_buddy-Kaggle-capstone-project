import pandas as pd
import os

DATASET_DIR = r"c:\Users\housh\Desktop\5-Day AI Agents Intensive Course with Google\dataset"
PROFILE_FILE = "student_spending (1).csv"
TRANSACTION_FILE = "budjet (2).csv"

class DataLoader:
    def __init__(self, directory_path=None):
        self.directory_path = directory_path or DATASET_DIR

    def list_files(self):
        if os.path.exists(self.directory_path):
            return os.listdir(self.directory_path)
        return []

    def load_csv(self, filename):
        path = os.path.join(self.directory_path, filename)
        if os.path.exists(path):
            return pd.read_csv(path)
        return None

def load_profiles():
    path = os.path.join(DATASET_DIR, PROFILE_FILE)
    if not os.path.exists(path):
        print(f"Warning: Dataset not found at {path}")
        return pd.DataFrame() # Return empty DataFrame
    df = pd.read_csv(path)
    # Clean column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def load_transactions():
    path = os.path.join(DATASET_DIR, TRANSACTION_FILE)
    if not os.path.exists(path):
        print(f"Warning: Dataset not found at {path}")
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Convert date
    # The format in file is '2022-07-06 05:57:10 +0000'
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

def get_student_profile(df_profiles, student_id=0):
    """Returns a single student profile as a dictionary (or Series)."""
    if student_id < len(df_profiles):
        return df_profiles.iloc[student_id]
    return None
