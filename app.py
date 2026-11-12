import streamlit as st
import pandas as pd
from parser import parse_chat
from stats import generate_wrapped_stats

# 1. Page Configuration
st.set_page_config(
    page_title="Memory Loop ✨ Digital Scrapbook",
    page_icon="🎀",
    layout="centered"
)

# 2. Custom Chic & Nostalgic Hot Pink CSS Styling
st.markdown("""
<style>
@import url('https://googleapis.com');

/* Bold Hot Pink Full-Screen Background */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: linear-gradient(160deg, #FF2A85 0%, #FF66A8 55%, #FF8DC2 100%) !important;
    font-family: 'Quicksand', sans-serif !important;
    color: #FFFFFF;
}

/* Dreamy Cursive Headings with Soft Glow */
h1, h2, h3 {
    font-family: 'Pacifico', cursive !important;
    font-weight: 400 !important;
    color: #FFFFFF !important;
    text-shadow: 0 2px 10px rgba(142, 15, 70, 0.35);
    letter-spacing: 0.5px;
}

/* Responsive single-line Hero Title that stays centered on all phones */
.hero-title {
    font-family: 'Pacifico', cursive !important;
    font-weight: 400 !important;
    color: #FFFFFF !important;
    text-shadow: 0 3px 12px rgba(142, 15, 70, 0.4);
    text-align: center !important;
    font-size: clamp(1.75rem, 7.2vw, 3rem) !important;
    white-space: nowrap !important;
    width: 100% !important;
    display: block !important;
    margin: 0 auto 10px auto !important;
    padding: 0 !important;
}


/* Make Story Tab Labels Readable on Hot Pink */
button[data-baseweb="tab"] p {
    font-family: 'Quicksand', sans-serif !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Chic White Polaroid / Scrapbook Cards (Pop against Hot Pink) */
.polaroid-card {
    background: #FFFFFF;
    border: 2px solid #FFE0EE;
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
    box-shadow: 0 10px 28px rgba(138, 12, 66, 0.22);
    text-align: center;
}

.polaroid-label {
    font-family: 'Quicksand', sans-serif;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #D62872;
    font-weight: 700;
    margin-bottom: 6px;
}

.polaroid-value {
    font-family: 'Pacifico', cursive;
    font-size: 2rem;
    font-weight: 400;
    color: #9E114F;
}

/* Dedicated Pink Headline for Slide 4 Keepsake Card */
.keepsake-title {
    font-family: 'Pacifico', cursive;
    font-size: 2.2rem;
    font-weight: 400;
    color: #FF1476 !important;
    margin: 10px 0;
}

.memory-box {
    font-family: 'Quicksand', sans-serif;
    background: #FFFFFF;
    border-left: 5px solid #C2185B;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 16px 0;
    font-style: italic;
    font-weight: 600;
    color: #5C1635;
    box-shadow: 0 8px 20px rgba(138, 12, 66, 0.18);
}

/* Style the file uploader outer card */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 2.5px dashed #FF1476 !important;
    border-radius: 18px !important;
    padding: 18px !important;
}

/* Make "Drop your exported WhatsApp chat..." label bold & dark berry */
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] label p,
[data-testid="stFileUploader"] [data-testid="stWidgetLabel"] p {
    font-family: 'Quicksand', sans-serif !important;
    color: #8E1546 !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
}

/* Disable clicking across the dropzone box so it acts as a static frame */
[data-testid="stFileUploaderDropzone"] {
    pointer-events: none !important;
    cursor: default !important;
}

/* Keep "Drag and drop file here" dark berry */
[data-testid="stFileUploaderDropzoneInstructions"] > div > span:first-child {
    font-family: 'Quicksand', sans-serif !important;
    color: #5C1635 !important;
    font-weight: 600 !important;
}

/* Make "Limit 200MB per file • TXT" plain white text with NO hot pink card & non-clickable */
[data-testid="stFileUploaderDropzoneInstructions"] > div > span:last-child,
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] small * {
    font-family: 'Quicksand', sans-serif !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background-color: transparent !important;
    padding: 0 !important;
    border-radius: 0 !important;
    font-weight: 600 !important;
    pointer-events: none !important;
    cursor: default !important;
}

/* Re-enable clicking ONLY on the "Browse files" button */
[data-testid="stFileUploaderDropzone"] button {
    font-family: 'Quicksand', sans-serif !important;
    pointer-events: auto !important;
    cursor: pointer !important;
    background-color: #FF2A85 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Hero Header
st.markdown("<div class='hero-title'>🎀 Memory Loop 🎀</div>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 1.1rem; color: #FFF5F9; font-weight: 600;'>"
    "A nostalgic digital scrapbook of your favorite Chat memories, late-night talks & inside jokes."
    "</p>",
    unsafe_allow_html=True
)

# 4. File Uploader
uploaded_file = st.file_uploader("💌 Drop your exported chat history (.txt) to open your scrapbook", type=["txt"])

if uploaded_file is not None:
    lines = uploaded_file.getvalue().decode("utf-8").splitlines()
    
    with st.spinner("✨ Unfolding your memories..."):
        df = parse_chat(lines)

    if df.empty:
        st.error("Oops! Could not read messages from this file. Please upload an unedited chat `.txt` export.")
    else:
        st.balloons()
        stats = generate_wrapped_stats(df)

        # Interactive Story Tabs (Like Instagram / Spotify Wrapped Slides)
        tab1, tab2, tab3, tab4 = st.tabs([
            "💌 Slide 1: Our Origin",
            "👑 Slide 2: Chat Energy",
            "💫 Slide 3: Our Rhythm",
            "📸 Slide 4: Keepsake Card"
        ])

        # SLIDE 1: Nostalgic Beginning
        with tab1:
            st.markdown("### Where It All Began...")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="polaroid-card">
                    <div class="polaroid-label">Memories Since</div>
                    <div class="polaroid-value" style="font-size: 1.5rem;">{stats['first_date']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="polaroid-card">
                    <div class="polaroid-label">Total Messages Shared</div>
                    <div class="polaroid-value">{stats['total_messages']:,} 💬</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="memory-box">
                <strong>✨ The Very First Text ({stats['first_sender']}):</strong><br/>
                “{stats['first_message']}”
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<p style='text-align:center; color:#FFFFFF; font-weight:600;'>You’ve written <b>{stats['total_words']:,} words</b> together—that’s basically your own mini novel! 📖</p>",
                unsafe_allow_html=True
            )

        # SLIDE 2: Who Carries the Conversation
        with tab2:
            st.markdown("### Who Carries the Chat? 💅")
            st.markdown(f"""
            <div class="polaroid-card">
                <div class="polaroid-label">Certified Yap Queen 👑</div>
                <div class="polaroid-value">{stats['top_sender']}</div>
                <p style="margin-top:8px; color:#7A4B60; font-weight:600;">Sent <b>{stats['top_sender_pct']}%</b> of all messages in this chat!</p>
            </div>
            """, unsafe_allow_html=True)

            st.bar_chart(stats["sender_counts"], color="#E06D9B")

        # SLIDE 3: Peak Hours & Inside Words
        with tab3:
            st.markdown("### Your Friendship Rhythm 🕰️")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="polaroid-card">
                    <div class="polaroid-label">Favorite Catch-Up Day</div>
                    <div class="polaroid-value" style="font-size: 1.6rem;">{stats['top_day']}s 🌸</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="polaroid-card">
                    <div class="polaroid-label">Peak Gossip Hour</div>
                    <div class="polaroid-value" style="font-size: 1.6rem;">{stats['peak_hour']} ✨</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 🔤 Your Signature Vocabulary")
            if stats["top_words"]:
                words_html = " ".join([
                    f"<span style='display:inline-block; background:#FCE4EC; color:#8E2952; padding:8px 16px; border-radius:20px; margin:5px; font-weight:700;'>#{w} ({c})</span>"
                    for w, c in stats["top_words"]
                ])
                st.markdown(f"<div style='text-align:center; margin: 12px 0;'>{words_html}</div>", unsafe_allow_html=True)

            hourly_full = stats["hourly_counts"].reindex(range(24), fill_value=0)
            st.line_chart(hourly_full, color="#D65A8A")

        # SLIDE 4: Shareable Keepsake
        with tab4:
            st.markdown("### 📸 Screenshot & Send to Your Love(s) ")
            st.markdown(f"""
            <div class="polaroid-card" style="background: linear-gradient(135deg, #FFF0F5 0%, #FFE4EE 100%);">
                <div class="polaroid-label">🎀 OUR CHAT WRAPPED 🎀</div>
                <div class="keepsake-title">{stats['total_messages']:,} Memories</div>
                <p style="color:#5C3346; font-size:1rem; font-weight:600;">
                    👑 <b>Top Chatter:</b> {stats['top_sender']} ({stats['top_sender_pct']}%)<br/>
                    🌸 <b>Favorite Day:</b> {stats['top_day']}s at {stats['peak_hour']}<br/>
                    📖 <b>Words Written:</b> {stats['total_words']:,}<br/>
                    💌 <b>Timeline Started:</b> {stats['first_date']}
                </p>
            </div>
            """, unsafe_allow_html=True)

