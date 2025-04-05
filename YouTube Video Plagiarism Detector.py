import datetime
import requests
import subprocess
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

def extract_published_date(video_id):
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': 'YOUTUBE_API_KEY'
    }

    response = requests.get(url, params=params)
    video_metadata = response.json()

    published_at_str = video_metadata['items'][0]['snippet']['publishedAt']
    published_at_datetime = datetime.datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ')

    return published_at_datetime

def transcribe_video_audio(video_id):
    audio_file = f'{video_id}.wav'
    
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    output_file = f'{video_id}.mp4'
    subprocess.call(['youtube-dl', '-o', output_file, video_url])
    
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
    ffmpeg_extract_audio(output_file, audio_file)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = ""
    except sr.RequestError:
        transcript = ""
    
    os.remove(output_file)
    os.remove(audio_file)
    
    return transcript

def find_earliest_video(df):
    earliest_video = None
    earliest_publish_date = datetime.datetime.now()

    for index, row in df.iterrows():
        published_date = extract_published_date(row['video_id'])
        if published_date < earliest_publish_date:
            earliest_publish_date = published_date
            earliest_video = row

    return earliest_video

def calculate_plagiarism_percentage(transcript1, transcript2):
    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform([transcript1, transcript2])

    cosine_similarity_value = cosine_similarity(X[0], X[1])[0][0]

    plagiarism_percentage = cosine_similarity_value * 100

    return plagiarism_percentage

def detect_plagiarism(df):
    earliest_video = find_earliest_video(df)

    if earliest_video is None:
        print("No videos found for plagiarism detection.")
        return None

    print("Details of the Earliest Published Video:")
    print("Video Name:", earliest_video['name'])
    print("Video Title:", earliest_video['title'])
    print("Published Date:", earliest_video['published_date'])
    print("\n")

    plagiarism_results = []

    for index, row in df.iterrows():
        plagiarism_percentage = calculate_plagiarism_percentage(
            earliest_video['transcript'],
            row['transcript']
        )

        plagiarism_results.append({
            'Video 1': earliest_video['name'],
            'Video 2': row['name'],
            'Plagiarism Percentage': plagiarism_percentage
        })

    plagiarism_df = pd.DataFrame(plagiarism_results)

    return plagiarism_df

if __name__ == "__main__":
    video_df = pd.read_csv('video_data.csv')

    for index, row in video_df.iterrows():
        video_df.at[index, 'transcript'] = transcribe_video_audio(row['video_id'])

    plagiarism_results_df = detect_plagiarism(video_df)

    if not plagiarism_results_df.empty:
        print("Plagiarism Results:")
        print(plagiarism_results_df)
    else:
        print("No videos found for plagiarism detection.")
