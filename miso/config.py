from pathlib import Path


# The outer project folder:
# /Users/hayleyprince/Desktop/miso
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

# The folder containing images and GIFs.
ASSETS_FOLDER = PROJECT_FOLDER / "assets"

# The folder where saved game data will be stored.
DATA_FOLDER = PROJECT_FOLDER / "data"

# The file containing the saved cat information.
SAVE_FILE = DATA_FOLDER / "cat_save.json"