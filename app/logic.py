# app/logic.py
import os
from datetime import datetime
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BALANCE_FILE = os.path.join(BASE_DIR, "..", "data", "balance.json")


def parse_time_string(time_str):
    hours = minutes = seconds = 0

    h_match = re.search(r"(\d+)h", time_str)
    m_match = re.search(r"(\d+)(?:min|m)", time_str)
    s_match = re.search(r"(\d+)s", time_str)

    if not (h_match or m_match or s_match):
        raise ValueError(f"⛔ Invalid time string: '{time_str}'")

    if h_match:
        hours = int(h_match.group(1))
    if m_match:
        minutes = int(m_match.group(1))
    if s_match:
        seconds = int(s_match.group(1))

    return hours * 3600 + minutes * 60 + seconds


def format_seconds(total_seconds):
    negative = total_seconds < 0
    total_seconds = abs(total_seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{'-' if negative else ''}{hours}h{minutes}min{seconds}s"


def load_balance():
    try:
        with open(BALANCE_FILE, "r") as f:
            data = json.load(f)
            return data["balance_seconds"], data["last_updated"]
    except FileNotFoundError:
        return 0, None


def save_balance(balance_seconds):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BALANCE_FILE, "w") as f:
        json.dump({"balance_seconds": balance_seconds, "last_updated": now}, f)
    print(f"💾 Saved balance: {balance_seconds} seconds at {now}")
    return now
