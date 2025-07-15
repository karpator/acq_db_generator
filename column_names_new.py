import random
import string
from dataclasses import dataclass
from typing import List

from generator_definitions import get_all_generator_names, get_generator_by_name


@dataclass
class ColumnNameConfig:
    """Configuration for column name generation and modification"""

    modification_probability: float = 0.2  # 20% chance to modify column name
    modification_intensity: float = (
        0.3  # How much to modify (0.0 = minimal, 1.0 = heavy)
    )

    # Character modification weights
    char_flip_weight: float = 0.4  # Probability to flip a character
    char_add_weight: float = 0.3  # Probability to add a random character
    char_remove_weight: float = 0.2  # Probability to remove a character
    char_replace_weight: float = 0.1  # Probability to replace a character


class ColumnNameGenerator:
    """Generates column names with multi-language support and optional character modifications"""

    def __init__(self, config: ColumnNameConfig | None = None):
        self.config = config or ColumnNameConfig()

    def get_random_column_name(self, generator_name: str) -> str:
        """Get a random column name for the specified generator"""
        try:
            generator = get_generator_by_name(generator_name)
            base_name = generator.get_random_column_name()

            # Apply modifications based on probability
            if random.random() < self.config.modification_probability:
                return self._modify_column_name(base_name)

            return base_name
        except ValueError:
            # Fallback for unknown generators
            return f"unknown_{generator_name}"

    def _modify_column_name(self, name: str) -> str:
        """Apply random modifications to a column name"""
        if not name or len(name) < 2:
            return name

        # Determine how many modifications to apply based on intensity
        num_modifications = max(
            1, int(len(name) * self.config.modification_intensity * 0.3)
        )

        modified_name = name
        for _ in range(num_modifications):
            modification_type = self._choose_modification_type()
            modified_name = self._apply_modification(modified_name, modification_type)

        return modified_name

    def _choose_modification_type(self) -> str:
        """Choose a random modification type based on weights"""
        choices = [
            ("flip", self.config.char_flip_weight),
            ("add", self.config.char_add_weight),
            ("remove", self.config.char_remove_weight),
            ("replace", self.config.char_replace_weight),
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

    def set_modification_config(self, config: ColumnNameConfig) -> None:
        """Update the modification configuration"""
        self.config = config


# Factory function for easy usage
def create_column_name_generator(
    modification_probability: float = 0.2, modification_intensity: float = 0.3
) -> ColumnNameGenerator:
    """Create a ColumnNameGenerator with custom configuration"""
    config = ColumnNameConfig(
        modification_probability=modification_probability,
        modification_intensity=modification_intensity,
    )
    return ColumnNameGenerator(config)


# Example usage and testing
if __name__ == "__main__":
    # Create generator with default settings
    generator = ColumnNameGenerator()

    print("=== Column Name Generator Demo ===\n")

    # Test some generators
    test_generators = ["name", "age", "price", "company", "email"]

    for gen_name in test_generators:
        print(f"Generator: {gen_name}")
        names = []
        for _ in range(5):  # Generate 5 names for each generator
            name = generator.get_random_column_name(gen_name)
            names.append(name)
        print(f"  Generated names: {', '.join(names)}")
        print()

    # Test with high modification settings
    print("=== High Modification Demo ===\n")
    high_mod_generator = create_column_name_generator(
        modification_probability=0.8, modification_intensity=0.7
    )

    for _ in range(10):
        name = high_mod_generator.get_random_column_name("name")
        print(f"Modified name: {name}")
