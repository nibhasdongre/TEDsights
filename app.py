import streamlit as st
import pandas as pd
import os

# Paths
DATA_PATH = "streamlit-data-genai.csv"
AUDIO_FOLDER = "audio"
PLOT_FOLDER = "plots"

# Predefined TED Talk URLs (the ones you provided)
video_urls = [
    "https://www.ted.com/talks/adeola_fayehun_africa_is_a_sleeping_giant_i_m_trying_to_wake_it_up?language=en",
    "https://www.ted.com/talks/ali_kashani_a_friendly_autonomous_robot_that_delivers_your_food?language=en",
    "https://www.ted.com/talks/swizz_beatz_how_to_support_and_celebrate_living_artists?language=en",
    "https://www.ted.com/talks/shekinah_elmore_the_courage_to_live_with_radical_uncertainty?language=en"
]

# Load data
df = pd.read_csv(DATA_PATH)
df = df.rename(columns={"index": "title"})
df["audio_file"] = [f"audio0{i+1}.mp3" for i in range(len(df))]

# Streamlit config
st.set_page_config(page_title="TEDsights - GenAI Insights from TED Talks", layout="wide")

# Custom styling
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: black !important;
        color: white !important;
    }
    .stButton>button {
        background-color: red !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold;
        padding: 10px 16px;
        font-size: 16px;
    }
    .st-collapsible, .st-expander, .stMarkdown {
        background-color: #1e1e1e !important;
        color: white !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
    }
    .block-container {
        padding: 2rem;
    }
    h1, h2, h3, h4 {
        color: red !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("TEDsights")
st.markdown("#### Explore GenAI-powered insights from impactful TED Talks")

# Sidebar - TED Talk selection
talk_titles = df["title"].tolist()
selected_title = st.sidebar.selectbox("🎙️ Select a TED Talk", talk_titles)
selected_row = df[df["title"] == selected_title].iloc[0]

# Display video buttons for the predefined TED Talk URLs
st.markdown("### 🎥 Watch TED Talks")

# Loop through the predefined video URLs and create a button for each
for i, url in enumerate(video_urls):
    st.markdown(
        f"""
        <a href="{url}" target="_blank">
            <button style='background-color: red; color: white; border-radius: 12px;
                        padding: 10px 20px; font-size: 18px; margin: 10px 0;'>
                ▶️ TED Talk {i+1}
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# Audio player
st.markdown("### 🔊 Audio")
st.audio(os.path.join(AUDIO_FOLDER, selected_row["audio_file"]), format="audio/mp3")

# Expander sections
with st.expander("📄 Summary"):
    st.write(selected_row["summary"])

with st.expander("💡 Impactful Ideas"):
    st.write(selected_row["impactful_ideas"])

with st.expander("📊 Sentiment Score"):
    st.write(f"Average Sentiment Score: {selected_row['avg_sentiment']:.2f}")
    
with st.expander("🎭 Top Emotions"):
    emotions = selected_row["top_3_emotions"].split(',')
    st.write(", ".join([emotion.strip().capitalize() for emotion in emotions]))

with st.expander("📝 Transcription"):
    st.write(selected_row["transcription"])

# Visualizations
st.markdown("---")
st.markdown("### 📈 Visual Insights")

plot_files = [
    "bar-graph.png",
    "histogram.png",
    "pie-chart.png",
    "violinplot.png",
    "wordcloud.png"
]

for plot in plot_files:
    plot_path = os.path.join(PLOT_FOLDER, plot)
    if os.path.exists(plot_path):
        st.image(plot_path, use_container_width=True)
    else:
        st.warning(f"Missing plot: {plot}")
