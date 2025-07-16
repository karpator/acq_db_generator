"""
Manipulator system for data generators.
Each manipulator implements a specific data transformation with its own probability.
"""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, TypeVar

# TypeVar for the BaseManipulator and its subclasses
T = TypeVar("T", bound="BaseManipulator")


class BaseManipulator(ABC):
    @dataclass
    class Config:
        """Configuration for a manipulator including its probability"""

        probability: float = 0.0  # 0.0 to 1.0 - chance this manipulator will be applied
        params: Dict[str, Any] = field(default_factory=dict)  # type: ignore

    """Abstract base class for all data manipulators"""

    def __init__(self, config: Config):
        self.config = config

    @classmethod
    def create(
        cls: type[T], probability: float = 0.0, params: dict[str, Any] | None = None
    ) -> T:
        """Factory method to create a manipulator instance with given probability and parameters"""
        if params is None:
            params = {}
        config = BaseManipulator.Config(probability=probability, params=params)
        return cls(config)

    @abstractmethod
    def can_apply_to_type(self, sql_type: str) -> bool:
        """Check if this manipulator can be applied to the given SQL type"""
        pass

    @abstractmethod
    def apply(self, value: Any) -> Any:
        """Apply the manipulation to the value"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this manipulator"""
        pass

    def should_apply(self) -> bool:
        """Check if this manipulator should be applied based on probability"""
        return random.random() < self.config.probability


class ManipulatorFactory:
    @staticmethod
    def create(
        manipulator_with_probs: list[tuple[BaseManipulator, float]],
    ) -> list[BaseManipulator]:
        """
        Create a manipulator instance based on the provided type and probability

        Args:
            manipulator_with_probs: List of tuples containing a manipulator instance and its probability

        Returns:
            List of manipulator instances that should be applied based on their probabilities

        Example:
        ```python
        manipulators = ManipulatorFactory.create([
            (UppercaseManipulator.create(probability=0.05), 0.05),
            (LowercaseManipulator.create(probability=0.05), 0.05),
            (NullManipulator.create(probability=0.02), 0.02),
        ])
        ```
        """
        instances: list[BaseManipulator] = []
        for manipulator, probability in manipulator_with_probs:
            if random.random() < probability:
                instances.append(manipulator)  # Use the already created instance
        return instances


# NULL Manipulator - Works with all types
class NullManipulator(BaseManipulator):
    """Returns None (NULL) value"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return True  # NULL can be applied to any type

    def apply(self, value: Any) -> Any:
        return None

    def get_name(self) -> str:
        return "NULL"


# Text Manipulators
class UppercaseManipulator(BaseManipulator):
    """Converts text to uppercase"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type == "TEXT"

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.upper()
        return value

    def get_name(self) -> str:
        return "UPPERCASE"


class LowercaseManipulator(BaseManipulator):
    """Converts text to lowercase"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type == "TEXT"

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()
        return value

    def get_name(self) -> str:
        return "LOWERCASE"


class TruncateManipulator(BaseManipulator):
    """Truncates text to a maximum length"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type == "TEXT"

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            max_length = self.config.params.get("max_length", 10)
            return value[:max_length]
        return value

    def get_name(self) -> str:
        return "TRUNCATE"


class PrefixManipulator(BaseManipulator):
    """Adds a prefix to text"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type == "TEXT"

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            prefix = self.config.params.get("prefix", "PREFIX_")
            return prefix + value
        return value

    def get_name(self) -> str:
        return "PREFIX"


class SuffixManipulator(BaseManipulator):
    """Adds a suffix to text"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type == "TEXT"

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            suffix = self.config.params.get("suffix", "_SUFFIX")
            return value + suffix
        return value

    def get_name(self) -> str:
        return "SUFFIX"


# Numeric Manipulators
class MultiplyManipulator(BaseManipulator):
    """Multiplies numeric values"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type in ["INTEGER", "REAL"]

    def apply(self, value: Any) -> Any:
        if isinstance(value, (int, float)):
            multiplier = self.config.params.get("multiplier", 1.0)
            result = value * multiplier
            # Preserve integer type if input was integer and result is whole number
            if (
                isinstance(value, int)
                and isinstance(result, float)
                and result.is_integer()
            ):
                return int(result)
            return result
        return value

    def get_name(self) -> str:
        return "MULTIPLY"


class AddOffsetManipulator(BaseManipulator):
    """Adds an offset to numeric values"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type in ["INTEGER", "REAL"]

    def apply(self, value: Any) -> Any:
        if isinstance(value, (int, float)):
            offset = self.config.params.get("offset", 0)
            return value + offset
        return value

    def get_name(self) -> str:
        return "ADD_OFFSET"


class RoundDecimalsManipulator(BaseManipulator):
    """Rounds decimal values to specified number of places"""

    def can_apply_to_type(self, sql_type: str) -> bool:
        return sql_type == "REAL"

    def apply(self, value: Any) -> Any:
        if isinstance(value, float):
            decimals = self.config.params.get("decimals", 2)
            return round(value, decimals)
        return value

    def get_name(self) -> str:
        return "ROUND_DECIMALS"


class ManipulatorApplier:
    """Applies a list of manipulators to data values"""

    def __init__(self, manipulators: list[BaseManipulator]):
        self.manipulators = manipulators

    def apply_manipulations(self, value: Any, sql_type: str) -> Any:
        """Apply manipulations to a value in order, respecting probabilities"""

        # Filter manipulators that can apply to this type
        applicable_manipulators = [
            m for m in self.manipulators if m.can_apply_to_type(sql_type)
        ]

        # Check for NULL manipulator first (special case)
        null_manipulators = [
            m
            for m in applicable_manipulators
            if isinstance(m, NullManipulator) and m.should_apply()
        ]

        # If a NULL manipulator should apply, return None immediately
        if null_manipulators:
            return None

        # Check which non-NULL manipulators should apply based on their probability
        eligible_manipulators = [
            m
            for m in applicable_manipulators
            if not isinstance(m, NullManipulator) and m.should_apply()
        ]

        # If multiple manipulators are eligible, randomly select one to make it fair
        if eligible_manipulators:
            selected_manipulator = random.choice(eligible_manipulators)
            value = selected_manipulator.apply(value)

        return value
