# File: history.py
# Save and load image caption history using CSV

import csv
import os
from datetime import datetime

CSV_FILE = "captions.csv"

def save_caption(image_path, caption):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, image_path, caption])

def load_captions():
    captions = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            captions = list(reader)
    return captions
