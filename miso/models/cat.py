from dataclasses import asdict, dataclass
from typing import Any

from virtual_pet.models.food_opts import FOOD_OPTIONS
from virtual_pet.models.play_opts import PLAY_OPTIONS

@dataclass
class Cat:
    name: str = 'Miso'
    fullness: int = 70
    hydration: int = 70
    happiness: int = 70
    affection: int = 50
    cleanliness: int = 70
    energy: int = 70

    def feed(self, food_name: str) -> str:

        choice = food_name.strip().lower()

        if choice not in FOOD_OPTIONS:
            return f"{food_name} is not an availiable food option"
        
        if self.fullness == MAX_STAT:
            return f"{self.name} is already full!"
        
        effects = FOOD_OPTIONS[choice]

        self.fullness = self._clamp(
            self.fullness + effects["fullness"]
        )

        self.hydration = self._clamp(
            self.hydration + effects["hydration"]
        )

        self.happiness = self._clamp(
            self.happiness + effects["happiness"]
        )

        return f"{self.name} happily ate the {choice}!"

    def drink(self) -> str:
        """Give the cat water."""

        if self.hydration == MAX_STAT:
            return f"{self.name} is not thirsty right now."

        self.hydration = self._clamp(self.hydration + 25)
        self.happiness = self._clamp(self.happiness + 1)

        return f"{self.name} drank some fresh water!"

    def pet(self) -> str:
        """Pet the cat and increase affection and happiness."""

        self.affection = self._clamp(self.affection + 10)
        self.happiness = self._clamp(self.happiness + 5)

        return f"{self.name} purrs while you pet them."

    def play(self, activity_name: str) -> str:
        """Play one of the available games with the cat."""

        choice = activity_name.strip().lower()

        if choice not in PLAY_OPTIONS:
            return f"{activity_name} is not an available play option."

        effects = PLAY_OPTIONS[choice]

        energy_needed = abs(effects["energy"])

        if self.fullness < 15:
            return f"{self.name} is too hungry to play."

        if self.hydration < 15:
            return f"{self.name} is too thirsty to play."

        if self.energy < energy_needed:
            return f"{self.name} is too tired to play {choice}."

        self.happiness = self._clamp(
            self.happiness + effects["happiness"]
        )

        self.affection = self._clamp(
            self.affection + effects["affection"]
        )

        self.energy = self._clamp(
            self.energy + effects["energy"]
        )

        self.fullness = self._clamp(
            self.fullness + effects["fullness"]
        )

        self.hydration = self._clamp(
            self.hydration + effects["hydration"]
        )

        return f"{self.name} had fun playing with the {choice}!"

    def groom(self) -> str:
        """Groom the cat and increase cleanliness."""

        if self.cleanliness == MAX_STAT:
            return f"{self.name} is already perfectly clean!"

        self.cleanliness = self._clamp(self.cleanliness + 20)
        self.affection = self._clamp(self.affection + 2)

        return f"{self.name} looks clean and fluffy!"

    def pass_time(self) -> None:
        """Change the cat's needs as time passes."""

        self.fullness = self._clamp(self.fullness - 1)
        self.hydration = self._clamp(self.hydration - 1)
        self.happiness = self._clamp(self.happiness - 1)
        self.cleanliness = self._clamp(self.cleanliness - 1)
        self.energy = self._clamp(self.energy + 1)

    def rename(self, new_name: str) -> str:
        """Give the cat a new non-empty name."""

        cleaned_name = new_name.strip()

        if not cleaned_name:
            return "The cat's name cannot be empty."

        self.name = cleaned_name

        return f"Your cat's name is now {self.name}!"

    @property
    def mood(self) -> str:
        """Return a simple mood based on the cat's current needs."""

        if self.fullness < 20:
            return "hungry"

        if self.hydration < 20:
            return "thirsty"

        if self.energy < 20:
            return "sleepy"

        if self.cleanliness < 20:
            return "dirty"

        if self.happiness >= 80 and self.affection >= 70:
            return "very happy"

        if self.happiness < 30:
            return "sad"

        return "content"

    @staticmethod
    def available_foods() -> list[str]:
        """Return the names of all food choices."""

        return list(FOOD_OPTIONS.keys())

    @staticmethod
    def available_play_options() -> list[str]:
        """Return the names of all play choices."""

        return list(PLAY_OPTIONS.keys())

    def to_dictionary(self) -> dict[str, Any]:
        """Convert the cat into a dictionary that JSON can save."""

        return asdict(self)

    @classmethod
    def from_dictionary(cls, data: dict[str, Any]) -> "Cat":
        """Create a Cat object from previously saved data."""

        return cls(
            name=str(data.get("name", "Miso")),
            fullness=cls._clamp(
                int(data.get("fullness", 70))
            ),
            hydration=cls._clamp(
                int(data.get("hydration", 70))
            ),
            happiness=cls._clamp(
                int(data.get("happiness", 70))
            ),
            affection=cls._clamp(
                int(data.get("affection", 50))
            ),
            cleanliness=cls._clamp(
                int(data.get("cleanliness", 70))
            ),
            energy=cls._clamp(
                int(data.get("energy", 70))
            ),
        )

    @staticmethod
    def _clamp(value: int) -> int:
        """Keep a stat between 0 and 100."""

        return max(MIN_STAT, min(MAX_STAT, value))