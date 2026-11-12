import re
import pandas as pd

def parse_chat(lines):
    # Matches bracketed timestamps: [28/10/2026, 11:44:55 AM] Sender: Message
    pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\]\s([^:]+):\s(.*)$'
    system_pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\]\s-\s'

    parsed_data = []

    for line in lines:
        # Replace hidden mobile narrow spaces (\u202f and \u00a0) with normal spaces
        clean_line = line.replace('\u202f', ' ').replace('\u00a0', ' ').strip()
        if not clean_line:
            continue

        match = re.match(pattern, clean_line)
        if match:
            timestamp, sender, message = match.groups()
            parsed_data.append([timestamp, sender, message])
        elif re.match(system_pattern, clean_line):
            continue
        elif parsed_data:
            parsed_data[-1] += f" {clean_line}"

    df = pd.DataFrame(parsed_data, columns=["Timestamp", "Sender", "Message"])

    if not df.empty:
        # Automatically handles DD/MM/YYYY, MM/DD/YY, 2-digit or 4-digit years, and 12h/24h clocks
        df["Datetime"] = pd.to_datetime(df["Timestamp"], format="mixed", dayfirst=True)
        df["Date"] = df["Datetime"].dt.date
        df["Day_of_Week"] = df["Datetime"].dt.day_name()
        df["Hour"] = df["Datetime"].dt.hour
        df["Word_Count"] = df["Message"].apply(lambda x: len(x.split()))

    return df
