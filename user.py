import pandas as pd

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

def authenticate_user(username, password):
    try:
        df = pd.read_csv("Credentials.csv")
        user_row = df[(df['username'] == username) & (df['password'] == password)]
        if not user_row.empty:
            role = user_row.iloc[0]['role']
            return User(username, role)
    except Exception as e:
        print(f"Error reading credentials: {e}")
    return None