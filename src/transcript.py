from youtube_transcript_api import TranscriptsDisabled, VideoUnavailable, YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound


def _seconds_to_mmss(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def fetch_transcript(video_id: str, chunk_size: int) -> str:
    """
    Fetches the transcript for a given YouTube video ID.
    Merges transcript into chunks of specified size (seconds).
    Returns timestamps in MM:SS format.

    Args:
        video_id (str): YouTube video ID
        chunk_size (int): Size of each text chunk in seconds (default: 30).
                         Transcript entries will be grouped into approximately chunk_size second intervals.

    Returns:
        str: Formatted transcript with timestamps in MM:SS format
    """
    yt_api = YouTubeTranscriptApi()
    try:
        transcript = yt_api.fetch(video_id)
    except NoTranscriptFound:
        return "<no_transcript>"
    except TranscriptsDisabled:
        return "<transcripts_disabled>"
    except VideoUnavailable:
        return "<video_unavailable>"
    except Exception as e:
        return "<error>"

    last = 0
    buffer = []
    result = ""
    for entry in transcript:
        # if I add this segment, what would duration be
        cumulative_duration = entry.start + entry.duration - last
        if cumulative_duration <= chunk_size:
            buffer.append(entry.text)
        else:
            buffer = " ".join(buffer)
            result += "{} - {}\n{}\n\n".format(
                _seconds_to_mmss(last), _seconds_to_mmss(entry.start), buffer)

            buffer = [entry.text]
            last = entry.start

    if buffer:
        segment_end = transcript[-1].start + \
            transcript[-1].duration if transcript else last
        buffer = " ".join(buffer)
        result += "{} - {}\n{}\n\n".format(_seconds_to_mmss(last),
                                           _seconds_to_mmss(segment_end), buffer)

    return result.strip()
