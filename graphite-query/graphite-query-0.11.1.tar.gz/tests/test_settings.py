import os
from __setup import TestCase
from __setup import DATA_DIR

def join(path):
    return os.path.join(DATA_DIR, path)

class TestLogger(TestCase):

    def test_setup_storage_variables(self):
        from graphite import settings
        settings.setup_storage_variables(DATA_DIR)
        self.assertEqual(settings.INDEX_FILE, join("index"))
        if settings.CERES_DIR is not None:
            self.assertEqual(settings.CERES_DIR, join("ceres"))
        self.assertEqual(settings.WHISPER_DIR, join("whisper"))
        self.assertEqual(settings.STANDARD_DIRS, [join("whisper")])

    def test_creating_directories(self):
        import os
        from graphite import settings

        settings.CREATE_DIRECTORIES = False

        # Test non-creation of directories
        self.assertFalse(os.path.exists(DATA_DIR))
        settings.setup_storage_variables(DATA_DIR)

        self.assertFalse(os.path.exists(DATA_DIR))
        self.assertFalse(os.path.exists(settings.WHISPER_DIR))
        if settings.CERES_DIR is not None:
            self.assertFalse(os.path.exists(settings.CERES_DIR))

        # Test creating directories
        settings.setup_storage_variables(DATA_DIR, create_directories=True)
        self.assertFalse(settings.CREATE_DIRECTORIES)

        self.assertTrue(os.path.exists(DATA_DIR))
        self.assertTrue(os.path.exists(settings.WHISPER_DIR))
        if settings.CERES_DIR is not None:
            self.assertTrue(os.path.exists(settings.CERES_DIR))


