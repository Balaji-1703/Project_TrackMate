import json
import time
from datetime import datetime
import os

ACTIVE_USERS_FILE = "active_users.json"
INACTIVE_TIMEOUT = 300  # 5 minutes in seconds

def load_active_users():
    if os.path.exists(ACTIVE_USERS_FILE):
        try:
            with open(ACTIVE_USERS_FILE, 'r') as f:
                users = json.load(f)
                # Convert stored timestamps back to float
                return {k: float(v) for k, v in users.items()}
        except json.JSONDecodeError:
            return {}
    return {}

def save_active_users(users):
    with open(ACTIVE_USERS_FILE, 'w') as f:
        json.dump(users, f)

def add_active_user(username, is_admin=False):
    users = load_active_users()
    users[username] = time.time()
    save_active_users(users)

def remove_active_user(username):
    users = load_active_users()
    if username in users:
        del users[username]
        save_active_users(users)

def cleanup_inactive_users():
    users = load_active_users()
    current_time = time.time()
    active_users = {
        user: timestamp
        for user, timestamp in users.items()
        if current_time - timestamp < INACTIVE_TIMEOUT
    }
    if active_users != users:
        save_active_users(active_users)
    return active_users

def update_user_activity(username):
    users = load_active_users()
    if username in users:
        users[username] = time.time()
        save_active_users(users)