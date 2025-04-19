const fileTitles = document.getElementById("fileTitles");
const selectedTitle = document.getElementById("selectedTitle");
const videoLink = document.getElementById("videoLink");
const audioPlayer = document.getElementById("audioPlayer");
const transcriptText = document.getElementById("transcriptText");
const summaryText = document.getElementById("summaryText");
const ideasText = document.getElementById("ideasText");
const sentimentScore = document.getElementById("sentimentScore");
const emotionsList = document.getElementById("emotionsList");

let videoData = [];
let transcripts = [];
let summaries = [];
let analysis = [];

async function fetchData() {
  const videoRes = await fetch("data/video_urls.csv");
  const transcriptRes = await fetch("data/transcriptions.json");
  const summaryRes = await fetch("data/summarized_transcriptions.json");
  const analysisRes = await fetch("data/analysis.json");

  const videoText = await videoRes.text();
  videoData = videoText.trim().split("\n").slice(0, 4); // Only 4 talks

  transcripts = Object.values(await transcriptRes.json()).slice(0, 4);
  summaries = Object.values(await summaryRes.json()).slice(0, 4);
  analysis = (await analysisRes.json()).slice(0, 4);

  populateTalkList();
}

function populateTalkList() {
  fileTitles.innerHTML = "";
  videoData.forEach((_, idx) => {
    const li = document.createElement("li");
    li.textContent = `TED Talk ${idx + 1}`;
    li.style.cursor = "pointer";
    li.onclick = () => displayTalk(idx);
    fileTitles.appendChild(li);
  });
}

function displayTalk(index) {
  selectedTitle.textContent = `TED Talk ${index + 1}`;
  videoLink.href = videoData[index];
  audioPlayer.src = `audio/audio${index + 1}.mp3`;
  transcriptText.textContent = transcripts[index];
  summaryText.textContent = summaries[index];
  ideasText.textContent = analysis[index].impactful_ideas;
  sentimentScore.textContent = analysis[index].sentiment.join(", ");
  emotionsList.textContent = analysis[index].emotion.join(", ");
}

fetchData();
