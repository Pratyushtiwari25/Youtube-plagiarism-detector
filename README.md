
# YouTube Video Plagiarism Detection  
**Detecting Transcript Similarity Across YouTube Videos Using NLP & Audio Processing**

##  Overview

This project automates the process of detecting potential **plagiarism between YouTube videos** by analyzing and comparing their **spoken content** (transcripts). The system:
- Extracts audio from videos,
- Transcribes the speech using **Google Speech Recognition**, and
- Calculates **plagiarism percentage** using **TF-IDF** and **cosine similarity**.

The comparison is anchored against the **earliest published video** to determine if newer videos have overlapping content.

---

##  Tech Stack

| Tool/Library | Description |
|--------------|-------------|
| `youtube-dl` | Downloads YouTube videos |
| `moviepy` | Extracts audio from video |
| `SpeechRecognition` | Transcribes audio to text using Google API |
| `requests` | Fetches YouTube video metadata via YouTube Data API |
| `pandas` | Data manipulation |
| `scikit-learn` | TF-IDF vectorization & cosine similarity |
| `os`, `subprocess`, `datetime` | System operations and time parsing |

---

##  Features

-  Automatically fetches YouTube video metadata
-  Downloads video and extracts audio
-  Transcribes audio to text using Google Speech API
-  Computes plagiarism percentage using text similarity (TF-IDF + Cosine Similarity)
-  Identifies and compares content against the **earliest published** video

---

## Input Format

### `video_data.csv`
A CSV file with the following columns:
- `video_id`: YouTube Video ID (e.g., `dQw4w9WgXcQ`)
- `name`: Short name or alias of the video
- `title`: Title of the video (optional)

**Example:**
```csv
video_id,name,title
dQw4w9WgXcQ,Video A,Understanding AI
3tmd-ClpJxA,Video B,Intro to Machine Learning
```

---

##  How to Run

###  Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure you have the following:
- `youtube-dl` installed (`pip install youtube-dl`)
- `ffmpeg` installed and added to your system path
- A valid **YouTube Data API v3** key set in the script (replace `YOUTUBE_API_KEY`)

##  Workflow

1. **Download** each video via `youtube-dl`
2. **Extract** audio using `moviepy`
3. **Transcribe** speech with `SpeechRecognition`
4. **Identify** the earliest published video using YouTube API
5. **Compute** similarity of transcripts (TF-IDF + Cosine Similarity)
6. **Output** plagiarism percentage between earliest and all other videos

---

##  Sample Output

```text
Details of the Earliest Published Video:
Video Name: Video A
Video Title: Understanding AI
Published Date: 2019-05-15 10:30:00

Plagiarism Results:
     Video 1   |  Video 2   |  Plagiarism Percentage
------------------------------------------------------
    Video A    |  Video A   |         100.00
    Video A    |  Video B   |          65.43
```

---

##  Notes

- The **Google Speech Recognition API** has usage limits; long videos or poor audio quality may reduce transcription accuracy.
- Accuracy of plagiarism detection depends on transcription quality and the presence of spoken content.
- Replace `'YOUTUBE_API_KEY'` in the script with your actual API key.

---

##  Folder Structure

```
├── YouTube Video Plagiarism Detector.py
├── requirements.txt
└── README.md
```

---

## 🙌 Acknowledgements

- [Google Speech Recognition API](https://cloud.google.com/speech-to-text/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [TF-IDF + Cosine Similarity](https://scikit-learn.org/)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl/)
