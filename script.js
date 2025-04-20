let videoData = [];
let transcripts = {};
let summaries = {};
let analysisData = [];

async function loadData() {
  // Load CSV (video_urls)
  const videoCSV = await fetch('data/video_urls.csv').then(res => res.text());
  const videoLines = videoCSV.trim().split('\n').slice(1, 5); // Only first 4
  videoData = videoLines.map(line => {
    const [title, url] = line.split(',');
    return { title: title.trim(), url: url.trim() };
  });

  // Load JSON files
  transcripts = await fetch('data/transcriptions.json').then(res => res.json());
  summaries = await fetch('data/summarized_transcriptions.json').then(res => res.json());

  // Load analysis CSV
  const analysisCSV = await fetch('data/analysis.csv').then(res => res.text());
  const analysisLines = analysisCSV.trim().split('\n').slice(1); // Skip header
  analysisData = analysisLines.map(line => {
    const [title, ideas, sentiment, emotions] = line.split(',');
    return {
      title: title.trim(),
      ideas: ideas.trim(),
      sentiment: sentiment.trim(),
      emotions: emotions.trim()
    };
  });

  displayTalkButtons();
}

function displayTalkButtons() {
  const fileTitles = document.getElementById('fileTitles');
  videoData.forEach((talk, index) => {
    const button = document.createElement('button');
    button.textContent = talk.title;
    button.className = 'btn';
    button.addEventListener('click', () => displayTalkDetails(index));
    fileTitles.appendChild(button);
  });
}

function displayTalkDetails(index) {
  const talk = videoData[index];
  const title = talk.title;

  document.getElementById('selectedTitle').textContent = title;
  document.getElementById('videoLink').href = talk.url;

  // Load audio (audio files assumed to be audio01.mp3, audio02.mp3, audio03.mp3)
  const audioSrc = `audio/audio0${index + 1}.mp3`;
  document.getElementById('audioPlayer').src = audioSrc;

  // Load transcript
  document.getElementById('transcriptText').textContent = transcripts[title] || 'Transcript not available';

  // Load summary
  document.getElementById('summaryText').textContent = summaries[title]?.summary || 'Summary not available';

  // Load analysis
  const talkAnalysis = analysisData.find(item => item.title === title);
  if (talkAnalysis) {
    document.getElementById('ideasText').textContent = talkAnalysis.ideas || 'N/A';
    document.getElementById('sentimentScore').textContent = talkAnalysis.sentiment || 'N/A';
    document.getElementById('emotionsList').textContent = talkAnalysis.emotions || 'N/A';
  } else {
    document.getElementById('ideasText').textContent = 'N/A';
    document.getElementById('sentimentScore').textContent = 'N/A';
    document.getElementById('emotionsList').textContent = 'N/A';
  }
}

loadData();
