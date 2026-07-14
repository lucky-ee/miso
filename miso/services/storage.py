import json

from miso.config import SAVE_FILE
from miso.models.cat import Cat


def save_cat(cat: Cat) -> None:
    """Save the cat's information to a JSON file."""

    # Create the data folder if it does not already exist.
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Convert the Cat object into a dictionary and save it.
    with SAVE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cat.to_dictionary(), file, indent=4)


def load_cat() -> Cat:
    """Load the saved cat or create a new cat."""

    # There is no saved game yet.
    if not SAVE_FILE.exists():
        return Cat()

    try:
        with SAVE_FILE.open("r", encoding="utf-8") as file:
            cat_data = json.load(file)

        return Cat.from_dictionary(cat_data)

    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        # Create a new cat if the save file is damaged.
        return Cat()