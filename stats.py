from collections import Counter
import re
from parser import parse_chat

STOP_WORDS = {
    "the", "to", "and", "a", "i", "is", "it", "in", "you", "of", "for",
    "on", "that", "this", "my", "me", "with", "be", "have", "are", "was",
    "so", "not", "but", "what", "at", "he", "she", "we", "they", "do",
    "omitted", "image", "video", "sticker", "audio", "forwarded", "voice", "message"
}

def generate_wrapped_stats(df):
    total_messages = len(df)
    total_words = int(df["Word_Count"].sum())

    # 1. Nostalgic Origin Stats (First Message & Timeline)
    first_row = df.iloc[0]
    first_date = first_row["Datetime"].strftime("%B %d, %Y")
    first_sender = first_row["Sender"]
    first_message = first_row["Message"]
    days_active = (df["Datetime"].max() - df["Datetime"].min()).days + 1

    # 2. Top Chatter
    sender_counts = df["Sender"].value_counts()
    top_sender = sender_counts.index[0]
    top_sender_pct = round((sender_counts.iloc[0] / total_messages) * 100, 1)

    # 3. Peak Day & Peak Hour
    top_day = df["Day_of_Week"].value_counts().index[0]
    peak_hour_24 = int(df["Hour"].value_counts().index[0])
    peak_hour_12 = f"{peak_hour_24 % 12 or 12} {'AM' if peak_hour_24 < 12 else 'PM'}"

    # 4. Top 5 Meaningful Words
    all_words = []
    for msg in df["Message"]:
        clean_msg = re.sub(r'http\S+|[^\w\s]', '', msg.lower())
        words = [w for w in clean_msg.split() if w not in STOP_WORDS and len(w) > 2]
        all_words.extend(words)

    top_words = Counter(all_words).most_common(5)

    return {
        "total_messages": total_messages,
        "total_words": total_words,
        "first_date": first_date,
        "first_sender": first_sender,
        "first_message": first_message,
        "days_active": days_active,
        "top_sender": top_sender,
        "top_sender_pct": top_sender_pct,
        "sender_counts": sender_counts,
        "top_day": top_day,
        "peak_hour": peak_hour_12,
        "hourly_counts": df["Hour"].value_counts().sort_index(),
        "top_words": top_words
    }
