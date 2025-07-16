# Constants for easy configuration
from dataclasses import dataclass

from faker import Faker


@dataclass
class COLUMN_NAME_CONFIG:
    """Configuration for column name generation and modification"""

    MODIFICATION_PROBABILITY: float = 0.1
    MODIFICATION_INTENSITY: float = 0.3

    # Character modification weights
    CHAR_FLIP_WEIGHT: float = 0.4  # Probability to flip a character
    CHAR_ADD_WEIGHT: float = 0.3  # Probability to add a random character
    CHAR_REMOVE_WEIGHT: float = 0.2  # Probability to remove a character
    CHAR_REPLACE_WEIGHT: float = 0.1  # Probability to replace a character


@dataclass
class CONFIG:
    MIN_TABLES: int = 6
    MAX_TABLES: int = 8
    MIN_COLUMNS_PER_TABLE: int = 3
    MAX_COLUMNS_PER_TABLE: int = 20
    MIN_ROWS_PER_TABLE: int = 1000
    MAX_ROWS_PER_TABLE: int = 10000
    NULL_PROBABILITY: float = 0.15
    LANGUAGES: tuple[str, ...] = ("hu", "en")
    COLUMN_NAME = COLUMN_NAME_CONFIG()


fake = Faker(CONFIG.LANGUAGES)