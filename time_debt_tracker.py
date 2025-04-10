# time_debt_tracker.py

import re


def parse_time_string(time_str):
    """
    Parses a time string like '2h59min3s' into total seconds.
    Accepts 'min' or 'm'.
    """
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
    """
    Formats a total number of seconds into 'XhYminZs', supports negative values.
    """
    negative = total_seconds < 0
    total_seconds = abs(total_seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{'-' if negative else ''}{hours}h{minutes}min{seconds}s"
