# File: auth.py
# Handles login and signup with password hashing using bcrypt

import json
import bcrypt
import os

USERS_FILE = "users.json"

# Ensure the file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

def login(username, password):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if username in users:
        stored_hash = users[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False

def signup(username, password):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if username in users:
        return False  # User already exists
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed.decode('utf-8')
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    return True
