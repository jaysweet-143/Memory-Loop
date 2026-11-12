# 🎀 Memory Loop — Chat Memories Wrapped

A nostalgic, interactive digital scrapbook that turns any exported WhatsApp chat (`.txt`) into a personalized "Year in Review" experience. Built for both one-on-one chats and close friend groups.

### ✨ [Launch Live App Here](https://memory-loop.streamlit.app/)


### 💡 What It Does
* **Parses Unstructured Text:** Cleans raw chat history `.txt` exports using Regular Expressions (`re`) and Pandas.
* **Nostalgic Origin Story:** Finds the very first message sent and calculates total days of friendship.
* **Chat Energy & Rhythm:** Identifies the top chatter, peak messaging hours, most active days, and signature vocabulary.
* **Privacy-First Design:** Uploaded files are processed temporarily in memory and are never saved or stored.

### 🛠️ Tech Stack
* **Python** (Regex, Collections)
* **Pandas** (Data Cleaning, Datetime Feature Engineering)
* **Streamlit** (Interactive Web App & Custom CSS UI)
