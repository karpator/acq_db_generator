import shutil
from pathlib import Path
from typing import List, Tuple


class ResultHandler:
    """Handles the creation of result folders and tracking of generator information"""

    def __init__(self, database_name: str):
        """Initialize with database name (without extension)"""
        self.database_name = database_name.replace(".sqlite", "")
        self.results_base_path = Path("results")
        self.result_folder_path = self.results_base_path / self.database_name
        self.generator_log: List[
            Tuple[str, str, str]
        ] = []  # (generator_name, table_name, column_name)

    def create_result_folder(self) -> None:
        """Create the results folder structure"""
        # Create base results directory if it doesn't exist
        self.results_base_path.mkdir(exist_ok=True)

        # Remove existing result folder if it exists
        if self.result_folder_path.exists():
            shutil.rmtree(self.result_folder_path)

        # Create new result folder
        self.result_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Created result folder: {self.result_folder_path}")

    def log_generator_usage(
        self, generator_name: str, table_name: str, column_name: str
    ) -> None:
        """Log which generator created which column"""
        self.generator_log.append((generator_name, table_name, column_name))

    def save_generator_log(self) -> None:
        """Save the generator log to a text file"""
        log_file_path = self.result_folder_path / f"{self.database_name}_generators.txt"

        with open(log_file_path, "w", encoding="utf-8") as f:
            # Write only the simple format: generator_name: table_name.column_name
            for generator_name, table_name, column_name in sorted(self.generator_log):
                f.write(f"{generator_name}: {table_name}.{column_name}\n")

        print(f"Generator log saved to: {log_file_path}")

    def finalize_results(self) -> None:
        """Finalize the results by saving logs"""
        self.save_generator_log()
        print(f"Results finalized in: {self.result_folder_path}")

    def get_database_path(self) -> str:
        """Get the full path where the database should be created"""
        return str(self.result_folder_path / f"{self.database_name}.sqlite")

    def get_result_folder_path(self) -> Path:
        """Get the path to the result folder"""
        return self.result_folder_path
