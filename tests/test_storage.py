import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from miso.models.cat import Cat
from miso.services.storage import load_cat, save_cat


class TestStorage(unittest.TestCase):

    def setUp(self):
        """Create a temporary folder before each test."""

        self.temporary_folder = tempfile.TemporaryDirectory()

        self.test_save_file = (
            Path(self.temporary_folder.name) / "cat_save.json"
        )

        # Replace storage.py's normal save path with the temporary path.
        self.save_file_patch = patch(
            "miso.services.storage.SAVE_FILE",
            self.test_save_file
        )

        self.save_file_patch.start()

    def tearDown(self):
        """Remove the temporary folder after each test."""

        self.save_file_patch.stop()
        self.temporary_folder.cleanup()

    def test_save_creates_file(self):
        """Saving a cat should create a JSON file."""

        cat = Cat(name="Miso")

        save_cat(cat)

        self.assertTrue(self.test_save_file.exists())

    def test_saved_file_contains_cat_data(self):
        """The JSON file should contain the cat's information."""

        cat = Cat(name="Miso")
        cat.fullness = 25

        save_cat(cat)

        with self.test_save_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data["name"], "Miso")
        self.assertEqual(saved_data["fullness"], 25)

    def test_load_returns_saved_cat(self):
        """Loading should restore the saved values."""

        cat = Cat(name="Miso")
        cat.fullness = 25
        cat.hydration = 40
        cat.happiness = 85
        cat.energy = 60

        save_cat(cat)

        loaded_cat = load_cat()

        self.assertIsInstance(loaded_cat, Cat)
        self.assertEqual(loaded_cat.name, "Miso")
        self.assertEqual(loaded_cat.fullness, 25)
        self.assertEqual(loaded_cat.hydration, 40)
        self.assertEqual(loaded_cat.happiness, 85)
        self.assertEqual(loaded_cat.energy, 60)

    def test_missing_file_returns_new_cat(self):
        """A new cat should be returned when no save exists."""

        loaded_cat = load_cat()

        self.assertIsInstance(loaded_cat, Cat)

    def test_damaged_file_returns_new_cat(self):
        """Invalid JSON should not crash the game."""

        self.test_save_file.write_text(
            "this is not valid JSON",
            encoding="utf-8"
        )

        loaded_cat = load_cat()

        self.assertIsInstance(loaded_cat, Cat)

    def test_new_save_overwrites_old_save(self):
        """The newest save should replace the previous save."""

        first_cat = Cat(name="Miso")
        first_cat.fullness = 80
        save_cat(first_cat)

        updated_cat = Cat(name="Miso")
        updated_cat.fullness = 30
        save_cat(updated_cat)

        loaded_cat = load_cat()

        self.assertEqual(loaded_cat.fullness, 30)


if __name__ == "__main__":
    unittest.main()