# SQLite Database Generator

A modular Python application that generates SQLite databases with realistic fake data using the Faker library. Features multilingual column names, data manipulators, and configurable generation parameters.

## Features

- **Bulk Generation**: Creates 12-16 tables with 12-18 columns each, containing 6,000 rows per table
- **Multilingual Support**: Hungarian and English locale support via Faker
- **Data Manipulators**: Extensible system for applying data transformations with configurable probabilities
- **Smart Column Names**: Intelligent column name generation with character modifications
- **Result Tracking**: Automatically creates result folders and tracks generator usage
- **Configurable**: Centralized configuration system for easy customization

## Quick Start

```bash
# Install dependencies
uv sync

# Generate a database
uv run python main.py my_database

# Generate with info display
uv run python main.py my_database --info
```

## Architecture

### Core Components

- **`DatabaseGenerator`**: Manages SQLite operations and table creation
- **`ColumnNameGenerator`**: Generates multilingual column names with modifications
- **`BaseManipulator`**: Abstract base for data transformation manipulators
- **`ResultHandler`**: Creates result folders and tracks generator information
- **`CONFIG`**: Centralized configuration management

### File Structure

```text
├── main.py                 # Entry point and CLI interface
├── database_generator.py   # Core database generation logic
├── manipulators.py         # Data transformation system
├── column_names.py         # Multilingual column name generation
├── generator_definitions.py # Data type generators
├── result_handler.py       # Result folder and tracking
├── config.py              # Configuration constants
└── test_manipulators.py    # Tests for manipulator system
```

## Configuration

Key settings in `config.py`:

- **Tables**: 12-16 per database
- **Columns**: 12-18 per table  
- **Rows**: 6,000 per table
- **Languages**: Hungarian, English
- **Column Modifications**: 10% probability, 20% intensity

## Requirements

- Python 3.10+
- faker>=37.4.0
- uv (package manager)
