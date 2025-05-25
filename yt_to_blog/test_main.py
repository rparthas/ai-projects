import unittest
from main import extract_video_id


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


if __name__ == "__main__":
    unittest.main() 