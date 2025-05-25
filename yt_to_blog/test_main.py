import unittest
from unittest.mock import patch
from main import extract_video_id, get_youtube_transcript, generate_blog_post_with_ollama, extract_title_from_blog_post
from youtube_transcript_api._errors import NoTranscriptFound
import ollama


class TestExtractVideoId(unittest.TestCase):
    """Unit tests for the extract_video_id function."""
    
    def test_standard_watch_url(self):
        """Test standard youtube.com/watch?v= URL format."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_shortened_youtu_be_url(self):
        """Test shortened youtu.be/ URL format."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_embed_url(self):
        """Test youtube.com/embed/ URL format."""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_shorts_url(self):
        """Test youtube.com/shorts/ URL format."""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_url_with_extra_parameters(self):
        """Test URL with additional parameters like timestamps."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s&list=PLrAXtmRdnEQy8VJqQzNhyD2QM8g5cREEJ"
        result = extract_video_id(url)
        self.assertEqual(result, "dQw4w9WgXcQ")
    
    def test_invalid_non_youtube_url(self):
        """Test invalid/non-YouTube URL should return None."""
        url = "https://www.example.com/video/123"
        result = extract_video_id(url)
        self.assertIsNone(result)
    
    def test_url_without_video_id(self):
        """Test YouTube URL without a video ID should return None."""
        url = "https://www.youtube.com/watch?v="
        result = extract_video_id(url)
        self.assertIsNone(result)
    
    def test_malformed_url(self):
        """Test completely malformed URL should return None."""
        url = "not a url at all"
        result = extract_video_id(url)
        self.assertIsNone(result)
    
    def test_youtube_homepage(self):
        """Test YouTube homepage URL should return None."""
        url = "https://www.youtube.com/"
        result = extract_video_id(url)
        self.assertIsNone(result)


class TestGetYoutubeTranscript(unittest.TestCase):
    """Unit tests for the get_youtube_transcript function."""
    
    @patch('main.YouTubeTranscriptApi.get_transcript')
    def test_successful_transcript_retrieval(self, mock_get_transcript):
        """Test successful transcript retrieval with mocked API call."""
        # Configure mock to return sample transcript data
        mock_transcript_data = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'world', 'start': 1.0, 'duration': 1.0},
            {'text': 'this', 'start': 2.0, 'duration': 1.0},
            {'text': 'is', 'start': 3.0, 'duration': 1.0},
            {'text': 'a', 'start': 4.0, 'duration': 1.0},
            {'text': 'test', 'start': 5.0, 'duration': 1.0}
        ]
        mock_get_transcript.return_value = mock_transcript_data
        
        # Call the function
        result = get_youtube_transcript("test_video_id")
        
        # Assert the result is correctly concatenated
        expected_result = "Hello world this is a test"
        self.assertEqual(result, expected_result)
        
        # Verify the API was called with correct video ID
        mock_get_transcript.assert_called_once_with("test_video_id")
    
    @patch('main.YouTubeTranscriptApi.get_transcript')
    def test_transcript_not_found(self, mock_get_transcript):
        """Test transcript not found exception handling."""
        # Configure mock to raise NoTranscriptFound exception
        mock_get_transcript.side_effect = NoTranscriptFound("test_video_id", [], None)
        
        # Call the function
        result = get_youtube_transcript("test_video_id")
        
        # Assert None is returned
        self.assertIsNone(result)
        
        # Verify the API was called
        mock_get_transcript.assert_called_once_with("test_video_id")
    
    @patch('main.YouTubeTranscriptApi.get_transcript')
    def test_generic_api_error(self, mock_get_transcript):
        """Test generic API error exception handling."""
        # Configure mock to raise a generic exception
        mock_get_transcript.side_effect = Exception("Test Generic Error")
        
        # Call the function
        result = get_youtube_transcript("test_video_id")
        
        # Assert None is returned
        self.assertIsNone(result)
        
        # Verify the API was called
        mock_get_transcript.assert_called_once_with("test_video_id")


class TestGenerateBlogPostWithOllama(unittest.TestCase):
    """Unit tests for the generate_blog_post_with_ollama function."""
    
    @patch('main.ollama.chat')
    def test_successful_blog_post_generation(self, mock_ollama_chat):
        """Test successful blog post generation with mocked API call."""
        # Configure mock to return a successful API response
        mock_response = {
            'message': {
                'content': "Title: Test Blog Post\n\nThis is a mocked blog post content generated from the transcript."
            }
        }
        mock_ollama_chat.return_value = mock_response
        
        # Call the function
        result = generate_blog_post_with_ollama("Test prompt", "test_model_name")
        
        # Assert the result matches the mocked content
        expected_result = "Title: Test Blog Post\n\nThis is a mocked blog post content generated from the transcript."
        self.assertEqual(result, expected_result)
        
        # Verify the API was called with correct parameters
        mock_ollama_chat.assert_called_once_with(
            model="test_model_name",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts video transcripts into engaging blog posts."},
                {"role": "user", "content": "Test prompt"}
            ]
        )
    
    @patch('main.ollama.chat')
    def test_ollama_api_error(self, mock_ollama_chat):
        """Test Ollama API error exception handling."""
        # Configure mock to raise ollama.ResponseError
        mock_ollama_chat.side_effect = ollama.ResponseError("Test API Error")
        
        # Call the function
        result = generate_blog_post_with_ollama("Test prompt", "test_model_name")
        
        # Assert None is returned
        self.assertIsNone(result)
        
        # Verify the API was called
        mock_ollama_chat.assert_called_once_with(
            model="test_model_name",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts video transcripts into engaging blog posts."},
                {"role": "user", "content": "Test prompt"}
            ]
        )
    
    @patch('main.ollama.chat')
    def test_connection_error(self, mock_ollama_chat):
        """Test connection error exception handling."""
        # Configure mock to raise a generic connection error
        mock_ollama_chat.side_effect = ConnectionError("Test Connection Error")
        
        # Call the function
        result = generate_blog_post_with_ollama("Test prompt", "test_model_name")
        
        # Assert None is returned
        self.assertIsNone(result)
        
        # Verify the API was called
        mock_ollama_chat.assert_called_once_with(
            model="test_model_name",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts video transcripts into engaging blog posts."},
                {"role": "user", "content": "Test prompt"}
            ]
        )


class TestExtractTitleFromBlogPost(unittest.TestCase):
    """Unit tests for the extract_title_from_blog_post function."""
    
    def test_extract_title_with_title_prefix(self):
        """Test extracting title when 'Title: ' prefix is present."""
        blog_post = "Title: How to Build Amazing Applications\n\nThis is the content of the blog post..."
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "How_to_Build_Amazing_Applications")
    
    def test_extract_title_case_insensitive(self):
        """Test extracting title with different case variations."""
        blog_post = "TITLE: Machine Learning Fundamentals\n\nContent here..."
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "Machine_Learning_Fundamentals")
    
    def test_extract_title_fallback_to_first_line(self):
        """Test fallback to first line when no 'Title: ' prefix found."""
        blog_post = "Understanding Python Programming\n\nThis is a blog post about Python..."
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "Understanding_Python_Programming")
    
    def test_extract_title_with_markdown_header(self):
        """Test extracting title from markdown header."""
        blog_post = "# The Future of AI Technology\n\nContent about AI..."
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "The_Future_of_AI_Technology")
    
    def test_sanitize_invalid_characters(self):
        """Test sanitizing invalid filename characters."""
        blog_post = 'Title: How to Use "Quotes" and <Tags> in Code?\n\nContent...'
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "How_to_Use_Quotes_and_Tags_in_Code")
    
    def test_long_title_truncation(self):
        """Test that very long titles are truncated."""
        long_title = "A" * 150  # 150 characters
        blog_post = f"Title: {long_title}\n\nContent..."
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(len(result), 100)  # Should be truncated to 100 chars
        self.assertTrue(result.startswith("A"))
    
    def test_empty_or_whitespace_title_fallback(self):
        """Test fallback when title is empty or whitespace."""
        blog_post = "Title:   \n\n\n\n"  # Empty content
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "blog_post")
    
    def test_title_with_spaces_converted_to_underscores(self):
        """Test that spaces in titles are converted to underscores."""
        blog_post = "Title: This Is A Test Title With Spaces\n\nContent..."
        result = extract_title_from_blog_post(blog_post)
        self.assertEqual(result, "This_Is_A_Test_Title_With_Spaces")


if __name__ == "__main__":
    unittest.main() 