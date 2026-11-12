import re
import pandas as pd

def parse_chat(lines):
    # Pattern 1: iPhone / Desktop bracketed format -> [28/10/2026, 11:44:55 AM] Sender: Message
    bracket_pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\]\s([^:]+):\s(.*)$'
    bracket_sys = r'^\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\]\s-\s'

    # Pattern 2: Android unbracketed format -> 28/10/2026, 11:44 AM - Sender: Message
    android_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\s-\s([^:]+):\s(.*)$'
    android_sys = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\s-\s'

    parsed_data = []

    for line in lines:
        # Clean hidden mobile spaces (\u202f, \u00a0) and left-to-right marks (\u200e)
        clean_line = (
            line.replace('\u202f', ' ')
                .replace('\u00a0', ' ')
                .replace('\u200e', '')
                .strip()
        )
        if not clean_line:
            continue

        match_bracket = re.match(bracket_pattern, clean_line)
        match_android = re.match(android_pattern, clean_line)

        if match_bracket:
            timestamp, sender, message = match_bracket.groups()
            parsed_data.append([timestamp, sender, message])
        elif match_android:
            timestamp, sender, message = match_android.groups()
            parsed_data.append([timestamp, sender, message])
        elif re.match(bracket_sys, clean_line) or re.match(android_sys, clean_line):
            continue
        elif parsed_data:
            parsed_data[-1][2] += f" {clean_line}"

    df = pd.DataFrame(parsed_data, columns=["Timestamp", "Sender", "Message"])

    if not df.empty:
        # errors="coerce" prevents any unexpected timestamp string from ever crashing the app
        df["Datetime"] = pd.to_datetime(df["Timestamp"], format="mixed", dayfirst=True, errors="coerce")
        df = df.dropna(subset=["Datetime"]).reset_index(drop=True)

        df["Date"] = df["Datetime"].dt.date
        df["Day_of_Week"] = df["Datetime"].dt.day_name()
        df["Hour"] = df["Datetime"].dt.hour
        df["Word_Count"] = df["Message"].apply(lambda x: len(x.split()))

    return df
