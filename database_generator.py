import random
import sqlite3
import sys
from typing import Any, List, Tuple

from faker import Faker

from column_names import ColumnNameGenerator
from config import CONFIG
from generator_definitions import get_random_generator_weighted
from result_handler import ResultHandler

fake = Faker(CONFIG.LANGUAGES)


class DatabaseGenerator:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

        # Initialize column name generator
        self.column_name_generator = ColumnNameGenerator()

        # Initialize result handler
        self.result_handler = ResultHandler(db_name)

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

    def generate_table_schema(
        self, table_name: str
    ) -> Tuple[str, List[Tuple[str, str, Any]]]:
        """Generate a random table schema with column names and types"""
        num_columns = random.randint(3, 8)
        columns: list[str] = []
        column_definitions: list[Tuple[str, str, Any]] = []

        # Always add an ID column
        columns.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
        column_definitions.append(("id", "id", lambda: None))  # ID is auto-generated

        used_names = set(["id"])

        for _ in range(num_columns - 1):  # -1 because we already added ID
            # Choose weighted random generator based on type preferences
            generator = get_random_generator_weighted()
            generator_name = generator.get_name()

            # Generate variant name and ensure uniqueness
            col_name = self.column_name_generator.get_random_column_name(generator)
            counter = 1
            while col_name in used_names:
                col_name = f"{self.column_name_generator.get_random_column_name(generator)}_{counter}"
                counter += 1

            used_names.add(col_name)
            columns.append(f"{col_name} {generator.sql_type}")
            column_definitions.append((col_name, generator_name, generator))

        schema = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        return schema, column_definitions

    def generate_row_data(
        self, column_definitions: list[Tuple[str, str, Any]]
    ) -> list[Any]:
        """Generate data for a single row"""
        row_data: list[Any] = []
        for col_name, _generator_name, generator in column_definitions:
            if col_name == "id":
                continue  # Skip ID as it's auto-generated

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

        # Log generator usage for each column (except ID)
        for col_name, generator_name, _ in column_definitions:
            if col_name != "id":  # Skip ID column
                self.result_handler.log_generator_usage(
                    generator_name, table_name, col_name
                )

        # Create table
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # type: ignore
            self.cursor.execute(schema)  # type: ignore
            print(f"Table schema: {schema}")
        except sqlite3.Error as e:
            print(f"Error creating table {table_name}: {e}")
            return

        # Generate random number of rows
        num_rows = random.randint(CONFIG.MIN_ROWS_PER_TABLE, CONFIG.MAX_ROWS_PER_TABLE)
        print(f"Generating {num_rows} rows...")

        # Prepare INSERT statement
        non_id_columns = [col for col, _, _ in column_definitions if col != "id"]
        placeholders = ", ".join(["?" for _ in non_id_columns])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(non_id_columns)}) VALUES ({placeholders})"

        # Generate and insert data in batches for better performance
        batch_size = 1000
        batch_data: list[list[Any]] = []

        for i in range(num_rows):
            row_data = self.generate_row_data(column_definitions)
            batch_data.append(row_data)

            if len(batch_data) >= batch_size or i == num_rows - 1:
                try:
                    self.cursor.executemany(insert_sql, batch_data)  # type: ignore
                    self.connection.commit()  # type: ignore
                    print(
                        f"Inserted {len(batch_data)} rows (Total: {i + 1}/{num_rows})"
                    )
                    batch_data = []
                except sqlite3.Error as e:
                    print(f"Error inserting data into {table_name}: {e}")
                    break

        # Get final row count
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")  # type: ignore
        final_count = self.cursor.fetchone()[0]  # type: ignore
        print(f"Table {table_name} created successfully with {final_count} rows")

    def generate_database(self) -> None:
        """Generate the complete database with multiple tables"""
        print(f"Generating SQLite database: {self.db_name}")
        print("Configuration:")
        print(f"  - Tables: {CONFIG.MIN_TABLES}-{CONFIG.MAX_TABLES}")
        print(
            f"  - Rows per table: {CONFIG.MIN_ROWS_PER_TABLE}-{CONFIG.MAX_ROWS_PER_TABLE}"
        )
        print(f"  - Languages: {CONFIG.LANGUAGES}")

        # Create result folder structure
        self.result_handler.create_result_folder()

        self.connect()

        # Generate random number of tables
        num_tables = random.randint(CONFIG.MIN_TABLES, CONFIG.MAX_TABLES)
        print(f"\nGenerating {num_tables} tables...")

        for i in range(1, num_tables + 1):
            table_name = f"table{i}"
            self.create_table(table_name)

        self.close()

        # Finalize results - copy database and save generator log
        self.result_handler.finalize_results(self.db_name)

        print("\nDatabase generation completed!")
        print(f"Database file: {self.db_name}")
        print(f"Results saved in: {self.result_handler.get_result_folder_path()}")

    def show_database_info(self) -> None:
        """Display information about the generated database"""
        self.connect()

        print(f"\nDatabase Information for: {self.db_name}")
        print("=" * 50)

        # Get all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")  # type: ignore
        tables = self.cursor.fetchall()  # type: ignore

        total_rows = 0
        for (table_name,) in tables:
            # Get table info
            self.cursor.execute(f"PRAGMA table_info({table_name})")  # type: ignore
            columns = self.cursor.fetchall()  # type: ignore

            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")  # type: ignore
            row_count = self.cursor.fetchone()[0]  # type: ignore
            total_rows += row_count

            print(f"\nTable: {table_name}")
            print(f"  Rows: {row_count}")
            print(f"  Columns: {len(columns)}")
            for col in columns:
                _col_id, name, data_type, _not_null, _default, _pk = col
                print(f"    - {name} ({data_type})")

        print(f"\nTotal tables: {len(tables)}")
        print(f"Total rows: {total_rows}")

        self.close()
