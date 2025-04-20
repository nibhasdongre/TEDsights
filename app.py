import streamlit as st
import pandas as pd
import os

# Load data from CSV
DATA_PATH = "streamlit-data-genai.csv"
AUDIO_FOLDER = "audio"
df = pd.read_csv(DATA_PATH)

# Preprocess dataframe!
df = df.rename(columns={"index": "title"})
df["audio_file"] = [f"audio0{i+1}.mp3" for i in range(len(df))]

# Streamlit app setup
st.set_page_config(page_title="TEDsights - GenAI Insights from TED Talks", layout="wide")
st.markdown("""
    <style>
    body {background-color: black; color: white;}
    .stButton>button {background-color: red; color: white; border-radius: 12px;}
    .st-collapsible, .stMarkdown {background-color: #1a1a1a; padding: 1rem; border-radius: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🎤 TEDsights")
st.markdown("#### Explore GenAI-powered insights from impactful TED Talks")

# Sidebar selection
talk_titles = df["title"].tolist()
selected_title = st.sidebar.selectbox("Select a TED Talk", talk_titles)
selected_row = df[df["title"] == selected_title].iloc[0]

# Main content
st.video(selected_row["video_url"])

# Audio player
st.audio(os.path.join(AUDIO_FOLDER, selected_row["audio_file"]), format="audio/mp3")

# Collapsible sections
with st.expander("📝 Transcription"):
    st.write(selected_row["transcription"])

with st.expander("📄 Summary"):
    st.write(selected_row["summary"])

with st.expander("💡 Impactful Ideas"):
    st.write(selected_row["impactful_ideas"])

with st.expander("📊 Sentiment Score"):
    st.write(f"Average Sentiment Score: {selected_row['avg_sentiment']:.2f}")

with st.expander("🎭 Top Emotions"):
    emotions = selected_row["top_3_emotions"].split(',')
    st.write(", ".join([emotion.strip().capitalize() for emotion in emotions]))

# Visualizations section
st.markdown("---")
st.markdown("### 📈 Visual Insights")
plot_files = ["plot1.png", "plot2.png", "plot3.png", "plot4.png", "plot5.png"]
for plot in plot_files:
    if os.path.exists(plot):
        st.image(plot, use_column_width=True)
    else:
        st.warning(f"Missing plot: {plot}")
