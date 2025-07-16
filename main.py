import argparse

from database_generator import DatabaseGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate SQLite database with fake data"
    )
    parser.add_argument(
        "database_name", help="Name of the SQLite database file to create"
    )
    parser.add_argument(
        "--info", action="store_true", help="Show database information after creation"
    )
    args = parser.parse_args()

    # Ensure .sqlite extension
    db_name = args.database_name
    if not db_name.endswith(".sqlite"):
        db_name += ".sqlite"

    # Generate database
    generator = DatabaseGenerator(db_name)
    generator.generate_database()

    # Show info if requested
    if args.info:
        generator.show_database_info()


if __name__ == "__main__":
    main()
