# SQLite Database Generator with Faker

A complex Python application that generates SQLite databases with realistic fake data using the Faker library. The application creates multiple tables with randomized schemas, multilingual column names, and configurable data generation parameters.

## Features

### Core Functionality
- **Multiple Tables**: Generates 5-10 tables per database with randomized names (table1, table2, etc.)
- **Variable Row Counts**: Each table contains 1,000-10,000 randomly generated rows
- **Mixed Data Types**: Supports TEXT, INTEGER, and REAL column types
- **NULL Values**: Configurable probability (default 15%) for NULL value generation
- **Multilingual Support**: English and Hungarian locale support via Faker

### Advanced Column Name Generation
- **Multilingual Column Names**: Extensive collection of column names in both English and Hungarian
- **Name Variations**: Each generator has multiple possible column name variants
- **Character Modifications**: Optional character-level modifications to column names including:
  - Character flipping (swapping adjacent characters)
  - Character addition (inserting random characters)
  - Character removal (removing characters)
  - Character replacement (substituting characters)
- **Configurable Modification**: Adjustable probability and intensity of name modifications

### Data Types and Generators

#### TEXT Columns
- Names (full names, first names, last names)
- Contact information (email, phone, address)
- Location data (city, country)
- Company information (company names, job titles)
- Descriptive text (descriptions, comments, notes)
- Web-related (URLs, usernames)
- Miscellaneous (license plates, colors)

#### INTEGER Columns
- Demographics (age, employee IDs)
- Financial (salary, counts, quantities)
- Temporal (years, active days)
- Metrics (scores, ratings, views)

#### REAL Columns
- Measurements (weight, height, temperature)
- Financial (prices, discounts, tax rates)
- Geographic (latitude, longitude)
- Percentages and ratios
- Exchange rates

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd feladat2
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

### Basic Usage
```bash
python main.py my_database
```

### Advanced Usage
```bash
python main.py my_database --info --modify-probability 0.5 --modify-intensity 0.8
```

### Command Line Arguments

- `database_name`: Name of the SQLite database file to create (required)
- `--info`: Show detailed database information after creation
- `--modify-probability`: Probability of modifying column names (0.0-1.0, default: 0.2)
- `--modify-intensity`: Intensity of column name modifications (0.0-1.0, default: 0.3)

### Examples

1. **Create a basic database:**
```bash
python main.py company_data.sqlite
```

2. **Create database with info display:**
```bash
python main.py company_data --info
```

3. **Create database with high name modification:**
```bash
python main.py messy_data --modify-probability 0.8 --modify-intensity 0.9 --info
```

## Configuration

### Constants (in main.py)
- `MIN_TABLES`: Minimum number of tables (default: 5)
- `MAX_TABLES`: Maximum number of tables (default: 10)
- `MIN_ROWS_PER_TABLE`: Minimum rows per table (default: 1,000)
- `MAX_ROWS_PER_TABLE`: Maximum rows per table (default: 10,000)
- `NULL_PROBABILITY`: Probability of NULL values (default: 0.15)
- `LANGUAGES`: Faker locales (default: ["en", "hu"])

### Column Name Modification Settings
- `modification_probability`: Chance of modifying column names
- `modification_intensity`: How aggressively to modify names
- Character modification weights for different types of changes

## File Structure

- `main.py`: Main database generator application
- `column_names.py`: Advanced column name generation with multilingual support
- `pyproject.toml`: Project dependencies and configuration
- `uv.lock`: Dependency lock file

## Architecture

### DatabaseGenerator Class
- Manages SQLite database connections
- Handles table creation and data insertion
- Integrates with column name generator
- Provides batch processing for performance

### ColumnNameGenerator Class
- Manages multilingual column name collections
- Applies configurable character modifications
- Supports custom name additions
- Provides type-safe name generation

### ColumnNameConfig Class
- Configuration dataclass for modification settings
- Customizable probability and intensity settings
- Flexible modification type weights

## Example Output

```
Generating SQLite database: sample.sqlite
Configuration:
  - Tables: 5-10
  - Rows per table: 1000-10000
  - NULL probability: 15.0%
  - Languages: ['en', 'hu']

Creating table: table1
Table schema: CREATE TABLE table1 (id INTEGER PRIMARY KEY AUTOINCREMENT, heaviness REAL, sterket_address TEXT)
Generating 3410 rows...

Database Information for: sample.sqlite
==================================================

Table: table1
  Rows: 3410
  Columns: 3
    - id (INTEGER)
    - heaviness (REAL) 
    - sterket_address (TEXT)
```

## Performance

- Batch insertion (1,000 rows per batch) for optimal performance
- Efficient memory usage through streaming data generation
- Configurable batch sizes for different system capabilities

## Requirements

- Python 3.10+
- faker>=37.4.0
- sqlite3 (built-in)

## License

This project is provided as-is for educational and development purposes.
