#!/usr/bin/env python3
"""
Test script to verify that the manipulator system is working correctly.
"""

from generator_definitions import NameGenerator


def test_manipulators():
    """Test the manipulator system"""
    print("Testing manipulator system...")

    # Create a name generator (which uses the test manipulators)
    name_gen = NameGenerator()

    print(f"Generator SQL type: {name_gen.sql_type}")
    print(f"Number of manipulators: {len(name_gen.manipulator_applier.manipulators)}")

    # Generate 20 test values to see the manipulations in action
    print("\nGenerating 20 test values:")
    print("-" * 70)
    print("Raw Value           -> Manipulated Value   [Status]")
    print("-" * 70)

    for _ in range(20):
        raw_value = name_gen.generate_raw_data()
        manipulated_value = name_gen.manipulator_applier.apply_manipulations(
            raw_value, name_gen.sql_type
        )

        status = "UNCHANGED"
        if manipulated_value is None:
            status = "NULL"
            display_value = "None"
        elif manipulated_value != raw_value:
            display_value = manipulated_value
            if manipulated_value == raw_value.upper():
                status = "UPPERCASE"
            elif manipulated_value == raw_value.lower():
                status = "LOWERCASE"
            else:
                status = "OTHER"
        else:
            display_value = manipulated_value

        print(f"{raw_value:<20} -> {display_value:<20} [{status}]")


if __name__ == "__main__":
    test_manipulators()
