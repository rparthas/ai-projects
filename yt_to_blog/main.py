# YouTube Transcript to Blog Post Converter
# Main script file

import re

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