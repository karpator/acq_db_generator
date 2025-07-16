import random
import string
from typing import List
from config import CONFIG

from generator_definitions import BaseGenerator, get_all_generator_names


class ColumnNameGenerator:
    """Generates column names with multi-language support and optional character modifications"""

    def get_random_column_name(self, generator: BaseGenerator) -> str:
        """Get a random column name for the specified generator"""
        try:
            base_name = generator.get_random_column_name()

            # Apply modifications based on probability
            if random.random() < CONFIG.COLUMN_NAME.MODIFICATION_PROBABILITY:
                return self._modify_column_name(base_name)

            return base_name
        except ValueError:
            # Fallback for unknown generators
            return f"unknown_{generator.get_name()}"

    def _modify_column_name(self, name: str) -> str:
        """Apply random modifications to a column name"""
        if not name or len(name) < 2:
            return name

        # Determine how many modifications to apply based on intensity
        num_modifications = max(
            1, int(len(name) * CONFIG.COLUMN_NAME.MODIFICATION_INTENSITY * 0.3)
        )

        modified_name = name
        for _ in range(num_modifications):
            modification_type = self._choose_modification_type()
            modified_name = self._apply_modification(modified_name, modification_type)

        return modified_name

    def _choose_modification_type(self) -> str:
        """Choose a random modification type based on weights"""
        choices = [
            ("flip", CONFIG.COLUMN_NAME.CHAR_FLIP_WEIGHT),
            ("add", CONFIG.COLUMN_NAME.CHAR_ADD_WEIGHT),
            ("remove", CONFIG.COLUMN_NAME.CHAR_REMOVE_WEIGHT),
            ("replace", CONFIG.COLUMN_NAME.CHAR_REPLACE_WEIGHT),
        ]

        # Weighted random choice
        total_weight = sum(weight for _, weight in choices)
        if total_weight == 0:
            return "flip"

        rand_val = random.uniform(0, total_weight)
        current_weight = 0

        for choice, weight in choices:
            current_weight += weight
            if rand_val <= current_weight:
                return choice

        return "flip"  # fallback

    def _apply_modification(self, name: str, modification_type: str) -> str:
        """Apply a specific type of modification to the name"""
        if not name:
            return name

        name_list = list(name)

        if modification_type == "flip" and len(name_list) > 1:
            # Flip two adjacent characters
            pos = random.randint(0, len(name_list) - 2)
            name_list[pos], name_list[pos + 1] = name_list[pos + 1], name_list[pos]

        elif modification_type == "add":
            # Add a random character at a random position
            pos = random.randint(0, len(name_list))
            char_type = random.choice(["letter", "digit", "underscore"])

            if char_type == "letter":
                new_char = random.choice(string.ascii_lowercase)
            elif char_type == "digit":
                new_char = random.choice(string.digits)
            else:
                new_char = "_"

            name_list.insert(pos, new_char)

        elif modification_type == "remove" and len(name_list) > 2:
            # Remove a random character (but not the first or last)
            pos = random.randint(1, len(name_list) - 2)
            name_list.pop(pos)

        elif modification_type == "replace" and len(name_list) > 0:
            # Replace a random character
            pos = random.randint(0, len(name_list) - 1)
            char_type = random.choice(["letter", "digit"])

            if char_type == "letter":
                new_char = random.choice(string.ascii_lowercase)
            else:
                new_char = random.choice(string.digits)

            name_list[pos] = new_char

        return "".join(name_list)

    def get_all_generator_names(self) -> List[str]:
        """Get all available generator names"""
        return get_all_generator_names()

