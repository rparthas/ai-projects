# YouTube Transcript to Blog Post Converter
# Main script file

import re
import os
import sys
import argparse
import ollama
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Load environment variables from .env file
load_dotenv()

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


def create_blog_post_prompt(transcript_text: str) -> str:
    """
    Formats the transcript into a prompt for an LLM to generate a blog post.
    
    Args:
        transcript_text (str): The video transcript text
        
    Returns:
        str: Formatted prompt for LLM to generate a blog post
    """
    prompt_template = """Please convert the following video transcript into a well-structured, engaging blog post. Follow these guidelines:

1. Create an engaging title for the blog post and prefix it with "Title: "
2. Write in a professional yet engaging tone that's accessible to a general audience
3. Organize the content with clear headings and well-structured paragraphs
4. Extract the key points and main ideas from the transcript
5. Add smooth transitions between sections to improve readability
6. Ensure the blog post flows logically from introduction to conclusion
7. Remove any filler words, repetitions, or transcript artifacts (like "um", "uh", etc.)
8. Make the content informative and valuable to readers

Here is the video transcript to convert:

{transcript_text}

Please provide the blog post content below:"""

    return prompt_template.format(transcript_text=transcript_text)


def generate_blog_post_with_ollama(prompt: str, model_name: str) -> str | None:
    """
    Sends the prompt to a local Ollama model and returns the generated blog post text.
    
    Args:
        prompt (str): The formatted prompt for the LLM
        model_name (str): Name of the Ollama model to use
        
    Returns:
        str | None: Generated blog post text if successful, None if error occurs
    """
    try:
        # Make the API call to Ollama
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts video transcripts into engaging blog posts."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the content from the response
        blog_post_content = response['message']['content']
        
        return blog_post_content
        
    except ollama.ResponseError as e:
        print(f"Error: Ollama API error with model '{model_name}': {str(e)}")
        return None
    except Exception as e:
        print(f"Error: Connection or other error when calling Ollama: {str(e)}")
        return None


def extract_title_from_blog_post(blog_post: str) -> str:
    """
    Extract the title from the blog post content.
    
    Args:
        blog_post (str): The generated blog post content
        
    Returns:
        str: Extracted title, sanitized for use as filename
    """
    # Look for "Title: " pattern at the beginning of the blog post
    title_match = re.search(r'^Title:\s*(.+)$', blog_post, re.MULTILINE | re.IGNORECASE)
    
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Fallback: use the first line if no "Title:" found
        first_line = blog_post.split('\n')[0].strip()
        # Remove common markdown headers
        title = re.sub(r'^#+\s*', '', first_line)
    
    # Sanitize title for filename (remove invalid characters)
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)
    sanitized_title = re.sub(r'\s+', '_', sanitized_title)  # Replace spaces with underscores
    sanitized_title = sanitized_title[:100]  # Limit length to 100 characters
    
    # Ensure we have a valid filename
    if not sanitized_title or sanitized_title.isspace():
        sanitized_title = "blog_post"
    
    return sanitized_title


def main_logic():
    """Main script logic for converting YouTube video to blog post."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert YouTube video transcript to blog post using Ollama")
    parser.add_argument("youtube_url", help="YouTube video URL to convert")
    args = parser.parse_args()
    
    # Retrieve OLLAMA_MODEL_NAME from environment variables
    ollama_model = os.getenv("OLLAMA_MODEL_NAME")
    if not ollama_model:
        print("Error: OLLAMA_MODEL_NAME not set in .env or environment. Please set it (e.g., 'llama3.2') and ensure the model is pulled with 'ollama pull <model_name>'.")
        sys.exit(1)
    
    # Use the provided YouTube URL
    youtube_url = args.youtube_url
    print(f"Processing YouTube URL: {youtube_url}")
    
    # Extract video ID
    video_id = extract_video_id(youtube_url)
    if video_id is None:
        print(f"Error: Could not extract video ID from URL: {youtube_url}")
        sys.exit(1)
    
    print(f"Extracted Video ID: {video_id}")
    
    # Fetch transcript
    print(f"Fetching transcript for video ID: {video_id}...")
    transcript_text = get_youtube_transcript(video_id)
    if transcript_text is None:
        print("Transcript not found or error fetching.")
        sys.exit(1)
    
    print("Transcript fetched successfully.")
    
    # Create prompt
    print(f"Creating prompt for Ollama model: {ollama_model}...")
    prompt = create_blog_post_prompt(transcript_text)
    
    # Generate blog post with Ollama
    print("Sending prompt to Ollama...")
    blog_post = generate_blog_post_with_ollama(prompt, ollama_model)
    if blog_post is not None:
        print("Blog post generated successfully.")
        
        # Extract title from blog post and create filename
        title = extract_title_from_blog_post(blog_post)
        output_filename = f"{title}.md"
        
        # Write blog post to file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(blog_post)
        
        print(f"Blog post saved to {output_filename}")
    else:
        print("Failed to generate blog post.")
        sys.exit(1)


if __name__ == "__main__":
    main_logic() 