import streamlit as st
import pandas as pd
import os

# Load data from CSV
DATA_PATH = "streamlit-data-genai.csv"
AUDIO_FOLDER = "audio"
PLOTS_FOLDER = "plots"  # Updated folder for images
df = pd.read_csv(DATA_PATH)

# Preprocess dataframe!
df = df.rename(columns={"index": "title"})
df["audio_file"] = [f"audio0{i+1}.mp3" for i in range(len(df))]

# Streamlit app setup
st.set_page_config(page_title="TEDsights - GenAI Insights from TED Talks", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: black; /* Black background */
        color: white; /* White text */
        text-align: center;
    }
    h1, h2, h3, h4 {
        color: red; /* Red headings */
    }
    .stButton>button {
        background-color: red; /* Red buttons */
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .st-collapsible, .stMarkdown, .st-expander {
        background-color: #2e2e2e; /* Slightly dark gray tiles */
        padding: 1rem;
        border-radius: 1rem;
        text-align: center;
    }
    .st-collapsible>div, .stMarkdown>div {
        color: white; /* White text inside tiles */
    }
    .stVideo, .stAudio, .stImage {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stExpander>div {
        text-align: center;
    }
    .stAlert {
        color: white;
        background-color: red;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("TEDsights")
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
plot_files = [
    "bar-graph.png",
    "histogram.png",
    "pie-chart.png",
    "violinplot.png",
    "wordcloud.png"
]

for plot in plot_files:
    plot_path = os.path.join(PLOTS_FOLDER, plot)  # Load images from 'plots' folder
    if os.path.exists(plot_path):
        st.image(plot_path, use_column_width=True)
    else:
        st.warning(f"Missing plot: {plot}")
