import argparse
import random
import sqlite3
import sys
from typing import Any, List, Tuple

from faker import Faker

from column_names import ColumnNameConfig, ColumnNameGenerator
from generator_definitions import get_all_generator_names, get_generator_by_name

# Constants for easy configuration
MIN_TABLES = 5
MAX_TABLES = 10
MIN_COLUMNS_PER_TABLE = 4
MAX_COLUMNS_PER_TABLE = 12
MIN_ROWS_PER_TABLE = 1000
MAX_ROWS_PER_TABLE = 10000
NULL_PROBABILITY = 0.15  # 15% chance of NULL values
LANGUAGES = ["en", "hu"]

# Initialize Faker
fake = Faker(LANGUAGES)


class DatabaseGenerator:
    def __init__(
        self, db_name: str, column_name_config: ColumnNameConfig | None = None
    ):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

        # Initialize column name generator
        self.column_name_generator = ColumnNameGenerator(column_name_config)

        # Get all available generator names
        self.available_generators = get_all_generator_names()

    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def generate_column_name_variant(self, generator_name: str) -> str:
        """Generate a column name using the column name generator"""
        return self.column_name_generator.get_random_column_name(generator_name)

    def generate_table_schema(
        self, table_name: str
    ) -> Tuple[str, List[Tuple[str, str, Any]]]:
        """Generate a random table schema with column names and types"""
        num_columns = random.randint(3, 8)
        columns = []
        column_definitions = []

        # Always add an ID column
        columns.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
        column_definitions.append(("id", "id", lambda: None))  # ID is auto-generated

        used_names = set(["id"])

        for _ in range(num_columns - 1):  # -1 because we already added ID
            # Choose random generator
            generator_name = random.choice(self.available_generators)
            generator = get_generator_by_name(generator_name)

            # Generate variant name and ensure uniqueness
            col_name = self.generate_column_name_variant(generator_name)
            counter = 1
            while col_name in used_names:
                col_name = (
                    f"{self.generate_column_name_variant(generator_name)}_{counter}"
                )
                counter += 1

            used_names.add(col_name)
            columns.append(f"{col_name} {generator.sql_type}")
            column_definitions.append((col_name, generator_name, generator))

        schema = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        return schema, column_definitions

    def should_be_null(self) -> bool:
        """Determine if a value should be NULL based on probability"""
        return random.random() < NULL_PROBABILITY

    def generate_row_data(
        self, column_definitions: List[Tuple[str, str, Any]]
    ) -> List[Any]:
        """Generate data for a single row"""
        row_data = []
        for col_name, generator_name, generator in column_definitions:
            if col_name == "id":
                continue  # Skip ID as it's auto-generated

            if self.should_be_null():
                row_data.append(None)
            else:
                try:
                    value = generator.generate_data()
                    row_data.append(value)
                except Exception as e:
                    print(f"Error generating data for {col_name}: {e}")
                    row_data.append(None)

        return row_data

    def create_table(self, table_name: str) -> None:
        """Create a single table with random data"""
        print(f"\nCreating table: {table_name}")

        # Generate schema
        schema, column_definitions = self.generate_table_schema(table_name)

        # Create table
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cursor.execute(schema)
            print(f"Table schema: {schema}")
        except sqlite3.Error as e:
            print(f"Error creating table {table_name}: {e}")
            return

        # Generate random number of rows
        num_rows = random.randint(MIN_ROWS_PER_TABLE, MAX_ROWS_PER_TABLE)
        print(f"Generating {num_rows} rows...")

        # Prepare INSERT statement
        non_id_columns = [col for col, _, _ in column_definitions if col != "id"]
        placeholders = ", ".join(["?" for _ in non_id_columns])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(non_id_columns)}) VALUES ({placeholders})"

        # Generate and insert data in batches for better performance
        batch_size = 1000
        batch_data = []

        for i in range(num_rows):
            row_data = self.generate_row_data(column_definitions)
            batch_data.append(row_data)

            if len(batch_data) >= batch_size or i == num_rows - 1:
                try:
                    self.cursor.executemany(insert_sql, batch_data)
                    self.connection.commit()
                    print(
                        f"Inserted {len(batch_data)} rows (Total: {i + 1}/{num_rows})"
                    )
                    batch_data = []
                except sqlite3.Error as e:
                    print(f"Error inserting data into {table_name}: {e}")
                    break

        # Get final row count
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        final_count = self.cursor.fetchone()[0]
        print(f"Table {table_name} created successfully with {final_count} rows")

    def generate_database(self) -> None:
        """Generate the complete database with multiple tables"""
        print(f"Generating SQLite database: {self.db_name}")
        print("Configuration:")
        print(f"  - Tables: {MIN_TABLES}-{MAX_TABLES}")
        print(f"  - Rows per table: {MIN_ROWS_PER_TABLE}-{MAX_ROWS_PER_TABLE}")
        print(f"  - NULL probability: {NULL_PROBABILITY * 100}%")
        print(f"  - Languages: {LANGUAGES}")

        self.connect()

        # Generate random number of tables
        num_tables = random.randint(MIN_TABLES, MAX_TABLES)
        print(f"\nGenerating {num_tables} tables...")

        for i in range(1, num_tables + 1):
            table_name = f"table{i}"
            self.create_table(table_name)

        self.close()
        print("\nDatabase generation completed!")
        print(f"Database file: {self.db_name}")

    def show_database_info(self) -> None:
        """Display information about the generated database"""
        self.connect()

        print(f"\nDatabase Information for: {self.db_name}")
        print("=" * 50)

        # Get all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()

        total_rows = 0
        for (table_name,) in tables:
            # Get table info
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()

            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = self.cursor.fetchone()[0]
            total_rows += row_count

            print(f"\nTable: {table_name}")
            print(f"  Rows: {row_count}")
            print(f"  Columns: {len(columns)}")
            for col in columns:
                col_id, name, data_type, not_null, default, pk = col
                print(f"    - {name} ({data_type})")

        print(f"\nTotal tables: {len(tables)}")
        print(f"Total rows: {total_rows}")

        self.close()


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
    parser.add_argument(
        "--modify-probability",
        type=float,
        default=0.2,
        help="Probability of modifying column names (0.0-1.0, default: 0.2)",
    )
    parser.add_argument(
        "--modify-intensity",
        type=float,
        default=0.3,
        help="Intensity of column name modifications (0.0-1.0, default: 0.3)",
    )

    args = parser.parse_args()

    # Ensure .sqlite extension
    db_name = args.database_name
    if not db_name.endswith(".sqlite"):
        db_name += ".sqlite"

    # Create column name configuration
    column_config = ColumnNameConfig(
        modification_probability=args.modify_probability,
        modification_intensity=args.modify_intensity,
    )

    # Generate database
    generator = DatabaseGenerator(db_name, column_config)
    generator.generate_database()

    # Show info if requested
    if args.info:
        generator.show_database_info()


if __name__ == "__main__":
    main()
