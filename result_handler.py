import shutil
from pathlib import Path
from typing import Any, List, Tuple


class ResultHandler:
    """Handles the creation of result folders and tracking of generator information"""

    def __init__(self, database_name: str):
        """Initialize with database name (without extension)"""
        self.database_name = database_name.replace(".sqlite", "")
        self.results_base_path = Path("results")
        self.result_folder_path = self.results_base_path / self.database_name
        self.generator_log: List[
            Tuple[str, str, str, str]
        ] = []  # (generator_name, generator_label, table_name, column_name)

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
        self,
        generator_name: str,
        generator_label: str,
        table_name: str,
        column_name: str,
    ) -> None:
        """Log which generator created which column"""
        self.generator_log.append(
            (generator_name, generator_label, table_name, column_name)
        )

    def save_generator_log(self) -> None:
        """Save the generator log to a text file"""
        log_file_path = self.result_folder_path / f"{self.database_name}_generators.txt"

        with open(log_file_path, "w", encoding="utf-8") as f:
            # Write using generator_label if available, otherwise skip
            for _generator_name, generator_label, table_name, column_name in sorted(
                self.generator_log
            ):
                if (
                    generator_label and generator_label.strip()
                ):  # Only log if label is not empty
                    f.write(f"{generator_label}: {table_name}.{column_name}\n")

        print(f"Generator log saved to: {log_file_path}")

        # Print summary of all generators and their labels
        self._print_generator_summary()

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

    def _print_generator_summary(self) -> None:
        """Print a summary of all generators, their labels, and column usage"""
        print("\n" + "=" * 80)
        print("GENERATOR SUMMARY")
        print("=" * 80)

        # Group by generator name
        generator_usage: dict[str, dict[str, Any]] = {}
        for generator_name, generator_label, table_name, column_name in sorted(
            self.generator_log
        ):
            if generator_name not in generator_usage:
                generator_usage[generator_name] = {
                    "label": generator_label,
                    "columns": [],
                }
            generator_usage[generator_name]["columns"].append(
                f"{table_name}.{column_name}"
            )

        # Print summary for each generator
        for generator_name in sorted(generator_usage.keys()):
            info = generator_usage[generator_name]
            label = (
                info["label"] if info["label"] and info["label"].strip() else "No label"
            )
            columns = info["columns"]

            print(f"\nGenerator: {generator_name}")
            print(f"Label: {label}")
            print(f"Used in {len(columns)} column(s):")
            for column in sorted(columns):
                print(f"  - {column}")

        print(f"\nTotal generators used: {len(generator_usage)}")
        print(f"Total columns generated: {len(self.generator_log)}")
        print("=" * 80)
