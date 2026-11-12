import re
import pandas as pd

def parse_chat(lines):
    pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[AP]M)\]\s([^:]+):\s(.*)$'
    system_pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[AP]M)\]\s-\s'

    parsed_data = []

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        match = re.match(pattern, clean_line)
        if match:
            timestamp, sender, message = match.groups()
            parsed_data.append([timestamp, sender, message])
        elif re.match(system_pattern, clean_line):
            continue
        elif parsed_data:
            parsed_data[-1][2] += f" {clean_line}"

    df = pd.DataFrame(parsed_data, columns=["Timestamp", "Sender", "Message"])
    df["Datetime"] = pd.to_datetime(df["Timestamp"], format="%m/%d/%y, %I:%M:%S %p")
    df["Date"] = df["Datetime"].dt.date
    df["Day_of_Week"] = df["Datetime"].dt.day_name()
    df["Hour"] = df["Datetime"].dt.hour
    df["Word_Count"] = df["Message"].apply(lambda x: len(x.split()))
    return df
