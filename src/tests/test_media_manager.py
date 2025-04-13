import unittest
from main.models.media_manager import MediaManager

class TestMediaManager(unittest.TestCase):

    def setUp(self):
        self.manager = MediaManager()

    def test_select_directory(self):
        # Simule la sélection d'un répertoire
        self.manager.media_path = "/path/to/test/media"
        self.assertTrue(self.manager.select_directory())

    def test_get_media_info(self):
        # Simule la sélection d'un répertoire
        self.manager.media_path = "/path/to/test/media"
        media_info = self.manager.get_media_info()
        self.assertIsInstance(media_info, list)
        self.assertTrue(all(isinstance(media, dict) for media in media_info))

if __name__ == "__main__":
    unittest.main()
