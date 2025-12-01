from transcript import fetch_transcript

video_id = "ys6it2_7pII"
transcript = fetch_transcript(video_id, chunk_size=10)
print(transcript)
