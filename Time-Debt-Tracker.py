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


def collect_time_entries(person):
    print(f"\n⏳ Enter {person}'s time (format like '2h3min1s').")
    print("Press Enter with no input when done.\n")
    total_seconds = 0

    while True:
        entry = input(f"{person}: ").strip()
        if not entry:
            break
        try:
            total_seconds += parse_time_string(entry)
        except ValueError as e:
            print(e)
    return total_seconds


def main():
    print("👯‍♀️ Alicia & Wanwei Time Debt Tracker")

    alicia_seconds = collect_time_entries("Alicia")
    wanwei_seconds = collect_time_entries("Wanwei")

    print("\n🧮 Totals:")
    print(f"🔹 Alicia: {format_seconds(alicia_seconds)}")
    print(f"🔹 Wanwei: {format_seconds(wanwei_seconds)}")

    difference = alicia_seconds - wanwei_seconds
    if difference == 0:
        print("\n⚖️ Neither owes time! It’s a perfect match.")
    elif difference > 0:
        print(f"\n💰 Wanwei owes Alicia {format_seconds(difference)}.")
    else:
        print(f"\n💰 Alicia owes Wanwei {format_seconds(-difference)}.")


if __name__ == "__main__":
    main()
