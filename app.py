
import streamlit as st
import pandas as pd
import json
import os

# Set page config
st.set_page_config(page_title="TEDsights", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
            color: white;
        }
        .css-1v0mbdj, .stButton > button {
            background-color: #d12b2b;
            color: white;
            border-radius: 12px;
            padding: 0.5em 1em;
        }
        .css-1v0mbdj:hover, .stButton > button:hover {
            background-color: #a51919;
        }
        .section-tile {
            background-color: #111111;
            padding: 1.2em;
            border-radius: 12px;
            margin: 1em 0;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
        }
        h1, h2, h3 {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
video_df = pd.read_csv("data/video_urls.csv")
with open("data/transcriptions.json", "r") as f:
    transcriptions = json.load(f)
with open("data/summarized_transcriptions.json", "r") as f:
    summaries = json.load(f)
analysis_df = pd.read_csv("data/analysis.csv")

# Limit to first 4 TED Talks
video_df = video_df.head(4)
analysis_df = analysis_df.head(4)

# Sidebar
st.sidebar.title("🎤 Choose a TED Talk")
talk_titles = video_df['title'].tolist()
selected_title = st.sidebar.radio("Select a talk:", talk_titles)

# Get index and data
index = talk_titles.index(selected_title)
video_url = video_df.iloc[index]['url']
audio_file = f"audio/audio0{index+1}.mp3"

# Layout begins
st.title("🎙️ TEDsights")
st.markdown("#### GenAI-powered insights from TED Talks")

st.markdown(f"""
<div class="section-tile">
<h2>{selected_title}</h2>
<p><strong>🔗 Video:</strong> <a href="{video_url}" target="_blank">{video_url}</a></p>
<p><strong>🔊 Audio:</strong></p>
<audio controls style="width: 100%;">
  <source src="{audio_file}" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
</div>
""", unsafe_allow_html=True)

# Transcription
with st.expander("📜 Transcription"):
    st.markdown(f'<div class="section-tile">{transcriptions[selected_title]}</div>', unsafe_allow_html=True)

# Summary
with st.expander("📝 Summary"):
    st.markdown(f'<div class="section-tile">{summaries[selected_title]}</div>', unsafe_allow_html=True)

# Impactful Ideas
with st.expander("💡 Impactful Ideas"):
    impactful_ideas = analysis_df.iloc[index]['impactful_ideas']
    st.markdown(f'<div class="section-tile">{impactful_ideas}</div>', unsafe_allow_html=True)

# Sentiment
with st.expander("📈 Sentiment Score"):
    sentiment_score = analysis_df.iloc[index]['avg_sentiment_score']
    st.markdown(f'<div class="section-tile">Average Sentiment Score: **{sentiment_score:.2f}**</div>', unsafe_allow_html=True)

# Emotions
with st.expander("❤️ Top Emotions"):
    emotions = analysis_df.iloc[index]['top_3_emotions']
    st.markdown(f'<div class="section-tile">Top 3 Emotions: **{emotions}**</div>', unsafe_allow_html=True)

# Visualizations
st.subheader("📊 Project Visualizations")
st.markdown('<div class="section-tile">', unsafe_allow_html=True)
cols = st.columns(2)

with cols[0]:
    st.image("plots/pie-chart.png", caption="Sentiment Distribution", use_column_width=True)
    st.image("plots/bar-graph.png", caption="Avg Sentiment Scores", use_column_width=True)
    st.image("plots/wordcloud.png", caption="Impactful Idea Word Cloud", use_column_width=True)

with cols[1]:
    st.image("plots/histogram.png", caption="Top 3 Emotions Frequency", use_column_width=True)
    st.image("plots/violinplot.png", caption="Sentiment by Emotion", use_column_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center>Made with 🤖 using Whisper, FLAN-T5, Streamlit, and GenAI</center>", unsafe_allow_html=True)
