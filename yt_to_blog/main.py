# YouTube Transcript to Blog Post Converter
# Main script file

import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def extract_video_id(video_url: str) -> str | None:
    """
    Extract YouTube video ID from various YouTube URL formats.
    
    Args:
        video_url (str): YouTube URL in various formats
        
    Returns:
        str | None: Video ID if found, None if not a valid YouTube URL or no ID found
        
    Supported formats:
        - youtube.com/watch?v=VIDEO_ID
        - youtu.be/VIDEO_ID
        - youtube.com/embed/VIDEO_ID
        - youtube.com/shorts/VIDEO_ID
    """
    # Define regex patterns for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',  # youtube.com/watch?v=VIDEO_ID
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',              # youtu.be/VIDEO_ID
        r'(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})',     # youtube.com/embed/VIDEO_ID
        r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})'     # youtube.com/shorts/VIDEO_ID
    ]
    
    # Try each pattern to find a match
    for pattern in patterns:
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
    
    # Return None if no pattern matches
    return None


def get_youtube_transcript(video_id: str) -> str | None:
    """
    Fetch YouTube video transcript and return as a single string.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str | None: Transcript text as a single string if successful, 
                   None if transcript not found or error occurs
    """
    try:
        # Fetch transcript from YouTube
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Concatenate all text segments into a single string
        transcript_text = " ".join([segment['text'] for segment in transcript_list])
        
        return transcript_text
        
    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video ID: {video_id}")
        return None
    except NoTranscriptFound:
        print(f"Error: No transcript found for video ID: {video_id}")
        return None
    except Exception as e:
        print(f"Error fetching transcript for video ID {video_id}: {str(e)}")
        return None 