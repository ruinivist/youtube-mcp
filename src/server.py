"""
youtube-mcp

simple mcp project built so as to learn the basics of mcps
at the time of writing I thought the idea was unique but apparently ( like always ) it wasn't

Prompts:
- Can you summarise this video?
- Can you give a timestamped link where the guy talks about X?
- Can you segment the video into chapters?
"""

from mcp.server.fastmcp import FastMCP
from transcript import fetch_transcript
from typing import Literal

mcp = FastMCP("youtube-mcp", json_response=True)


@mcp.tool()
def video_transcript(video_id: str) -> str:
    """
    Fetches the transcript for a given YouTube video ID.
    Merges transcript into chunks of specified size (seconds).
    Returns timestamps in MM:SS format.

    Args:
        video_id (str): YouTube video ID

    Returns:
        str: Formatted transcript with timestamps in MM:SS format
    """
    return fetch_transcript(video_id, chunk_size=10)  # 10 seconds chunk size


@mcp.prompt()
def analyze_video(video_url: str, task: Literal["summarize", "create chapters"]) -> str:
    """
    Prompt for analyzing YouTube videos with their transcripts.

    Args:
        video_url (str): YouTube video URL
        task (str): Type of analysis - "summarize" or "create chapters"

    Returns:
        str: Prompt text guiding the LLM to use the video_transcript tool
    """
    if task == "summarize":
        return f"Fetch the transcript for YouTube video '{video_url}' and provide a concise summary of the video content."
    elif task == "create chapters":
        return f"Fetch the transcript for YouTube video '{video_url}' and segment it into logical chapters with descriptive titles and timestamped links. Ensure each chapter is a coherent section of the video."
    # Literal choice ensures only valid tasks are passed


@mcp.prompt()
def find_topic(video_url: str, topic: str) -> str:
    """
    Prompt for finding specific topics in YouTube videos.

    Args:
        video_url (str): YouTube video URL
        topic (str): The topic to search for in the video

    Returns:
        str: Prompt text guiding the LLM to find the topic in the video transcript
    """
    return f"Fetch the transcript for YouTube video '{video_url}' and find where '{topic}' is discussed. Provide timestamped links for all relevant sections where this topic appears."


if __name__ == "__main__":
    mcp.run(transport='stdio')
