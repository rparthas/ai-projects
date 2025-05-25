import unittest
from unittest.mock import patch
from main import extract_video_id, get_youtube_transcript
from youtube_transcript_api._errors import NoTranscriptFound


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


if __name__ == "__main__":
    unittest.main() 