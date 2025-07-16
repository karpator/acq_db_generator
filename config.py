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
class GENERATOR_TYPE_WEIGHTS:
    """Configuration for generator type selection weights"""

    TEXT_WEIGHT: float = 4.0  # Weight for TEXT generators
    INTEGER_WEIGHT: float = 3.0  # Weight for INTEGER generators (higher = more likely)
    REAL_WEIGHT: float = 1.0  # Weight for REAL generators


@dataclass
class CONFIG:
    MIN_TABLES: int = 6
    MAX_TABLES: int = 8
    MIN_COLUMNS_PER_TABLE: int = 5
    MAX_COLUMNS_PER_TABLE: int = 20
    MIN_ROWS_PER_TABLE: int = 6000
    MAX_ROWS_PER_TABLE: int = 6000
    LANGUAGES: tuple[str, ...] = ("hu", "en")
    COLUMN_NAME = COLUMN_NAME_CONFIG()
    GENERATOR_WEIGHTS = GENERATOR_TYPE_WEIGHTS()


fake = Faker(CONFIG.LANGUAGES)
