"""
Generator definitions with column names and data generation functions.
Each generator inherits from BaseGenerator and defines its own column names and data generation logic.
"""

import random
from abc import ABC, abstractmethod
from typing import Any, List

from faker import Faker

# Initialize Faker with multiple locales
fake = Faker(["en", "hu"])


class BaseGenerator(ABC):
    """Base class for all data generators"""

    def __init__(self):
        self.sql_type = self.get_sql_type()
        self.column_names = self.get_column_names()

    @abstractmethod
    def get_sql_type(self) -> str:
        """Return the SQL data type for this generator"""
        pass

    @abstractmethod
    def get_column_names(self) -> List[str]:
        """Return list of possible column names in multiple languages"""
        pass

    @abstractmethod
    def generate_data(self) -> Any:
        """Generate a single data value"""
        pass

    def get_random_column_name(self) -> str:
        """Get a random column name from the available options"""
        return random.choice(self.column_names)


# TEXT Generators
class NameGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "name",
            "full_name",
            "person_name",
            "user_name",
            "customer_name",
            "client_name",
            "display_name",
            "screen_name",
            # Hungarian
            "nev",
            "teljes_nev",
            "szemely_nev",
            "felhasznalo_nev",
            "ugyfel_nev",
            "kliens_nev",
            "megjelenito_nev",
        ]

    def generate_data(self) -> str:
        return fake.name()


class FirstNameGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "first_name",
            "given_name",
            "forename",
            "christian_name",
            # Hungarian
            "keresztnev",
            "elso_nev",
            "vezeteknev_elott",
        ]

    def generate_data(self) -> str:
        return fake.first_name()


class LastNameGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "last_name",
            "surname",
            "family_name",
            "lastname",
            # Hungarian
            "vezeteknev",
            "csaladi_nev",
            "utolso_nev",
        ]

    def generate_data(self) -> str:
        return fake.last_name()


class CompanyGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "company",
            "corporation",
            "business",
            "enterprise",
            "firm",
            "organization",
            "workplace",
            "employer",
            # Hungarian
            "ceg",
            "vallalat",
            "uzlet",
            "vallalkozas",
            "cegek",
            "szervezet",
            "munkahely",
            "munkaado",
        ]

    def generate_data(self) -> str:
        return fake.company()


class JobTitleGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "job_title",
            "position",
            "role",
            "occupation",
            "profession",
            "title",
            "job_role",
            "work_position",
            # Hungarian
            "munkakor",
            "pozicio",
            "szerep",
            "foglalkozas",
            "szakma",
            "beosztas",
            "munka_pozicio",
            "allasi_hely",
        ]

    def generate_data(self) -> str:
        return fake.job()


class EmailGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "email",
            "email_address",
            "mail",
            "e_mail",
            "electronic_mail",
            "contact_email",
            "user_email",
            # Hungarian
            "email_cim",
            "levelezes",
            "elektronikus_lev",
            "kapcsolat_email",
        ]

    def generate_data(self) -> str:
        return fake.email()


class PhoneGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "phone",
            "phone_number",
            "telephone",
            "mobile",
            "cell_phone",
            "contact_number",
            "tel_number",
            # Hungarian
            "telefon",
            "telefonszam",
            "mobil",
            "mobil_telefon",
            "kapcsolat_szam",
            "tel_szam",
        ]

    def generate_data(self) -> str:
        return fake.phone_number()


class AddressGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "address",
            "street_address",
            "home_address",
            "location",
            "residence",
            "postal_address",
            # Hungarian
            "cim",
            "utca_cim",
            "lakcim",
            "hely",
            "lakhely",
            "postai_cim",
        ]

    def generate_data(self) -> str:
        return fake.address()


class CityGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "city",
            "town",
            "municipality",
            "urban_area",
            "settlement",
            # Hungarian
            "varos",
            "telepules",
            "onkormanyzat",
            "varosi_terulet",
        ]

    def generate_data(self) -> str:
        return fake.city()


class CountryGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "country",
            "nation",
            "state",
            "homeland",
            "territory",
            # Hungarian
            "orszag",
            "nemzet",
            "allam",
            "haza",
            "terulet",
        ]

    def generate_data(self) -> str:
        return fake.country()


class DescriptionGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "description",
            "details",
            "info",
            "information",
            "summary",
            "notes",
            "comments",
            "remarks",
            # Hungarian
            "leiras",
            "reszletek",
            "informacio",
            "osszefoglalas",
            "megjegyzesek",
            "kommentek",
            "eszrevetelek",
        ]

    def generate_data(self) -> str:
        return fake.text(max_nb_chars=200)


class WebsiteGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "website",
            "url",
            "web_address",
            "homepage",
            "site",
            "web_url",
            "link",
            # Hungarian
            "weboldal",
            "url_cim",
            "web_cim",
            "fooldal",
            "oldal",
            "link",
        ]

    def generate_data(self) -> str:
        return fake.url()


class UsernameGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "username",
            "login",
            "user_id",
            "account_name",
            "handle",
            # Hungarian
            "felhasznalo_nev",
            "bejelentkezes",
            "felhasznalo_id",
            "fiok_nev",
        ]

    def generate_data(self) -> str:
        return fake.user_name()


class LicensePlateGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "license_plate",
            "plate_number",
            "registration",
            "car_plate",
            # Hungarian
            "rendszam",
            "auto_rendszam",
            "jarmu_rendszam",
            "regisztracio",
        ]

    def generate_data(self) -> str:
        return fake.license_plate()


class ColorGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "color",
            "colour",
            "hue",
            "shade",
            "tint",
            # Hungarian
            "szin",
            "arnyalat",
            "tonalitas",
            "szinezes",
        ]

    def generate_data(self) -> str:
        return fake.color_name()


# INTEGER Generators
class AgeGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "age",
            "years_old",
            "birth_age",
            "current_age",
            # Hungarian
            "kor",
            "eletkor",
            "szuletesi_kor",
            "jelenlegi_kor",
        ]

    def generate_data(self) -> int:
        return random.randint(18, 90)


class SalaryGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "salary",
            "wage",
            "income",
            "pay",
            "earnings",
            "compensation",
            "remuneration",
            "stipend",
            # Hungarian
            "fizetes",
            "ber",
            "jovedelem",
            "kereset",
            "dijazas",
            "kompenzacio",
            "juttatas",
        ]

    def generate_data(self) -> int:
        return random.randint(30000, 150000)


class EmployeeIdGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "employee_id",
            "staff_id",
            "worker_id",
            "emp_number",
            "personnel_id",
            "team_member_id",
            # Hungarian
            "alkalmazott_id",
            "dolgozoi_id",
            "munkatars_id",
            "szemelyzeti_szam",
        ]

    def generate_data(self) -> int:
        return random.randint(1000, 9999)


class QuantityGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "quantity",
            "amount",
            "count",
            "number",
            "total",
            "sum",
            # Hungarian
            "mennyiseg",
            "osszeg",
            "darab",
            "szam",
            "osszesen",
        ]

    def generate_data(self) -> int:
        return random.randint(1, 1000)


class YearGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "year",
            "birth_year",
            "creation_year",
            "start_year",
            # Hungarian
            "ev",
            "szuletesi_ev",
            "letrehozas_eve",
            "kezdo_ev",
        ]

    def generate_data(self) -> int:
        return random.randint(1950, 2024)


class ScoreGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "score",
            "points",
            "rating_points",
            "grade",
            "mark",
            # Hungarian
            "pontszam",
            "pontok",
            "ertekeles_pont",
            "jegy",
            "osztályzat",
        ]

    def generate_data(self) -> int:
        return random.randint(0, 100)


class RatingGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "rating",
            "rank",
            "level",
            "grade",
            "classification",
            # Hungarian
            "ertekeles",
            "rang",
            "szint",
            "besorogas",
            "minosites",
        ]

    def generate_data(self) -> int:
        return random.randint(1, 5)


class OrderCountGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "order_count",
            "orders",
            "purchase_count",
            "buy_count",
            # Hungarian
            "rendeles_szam",
            "rendelesek",
            "vasarlas_szam",
            "vetel_szam",
        ]

    def generate_data(self) -> int:
        return random.randint(0, 50)


class DaysActiveGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "days_active",
            "active_days",
            "usage_days",
            "login_days",
            # Hungarian
            "aktiv_napok",
            "hasznalati_napok",
            "bejelentkezesi_napok",
        ]

    def generate_data(self) -> int:
        return random.randint(0, 365)


class ViewsGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "views",
            "page_views",
            "visits",
            "hits",
            "impressions",
            # Hungarian
            "megtekintesek",
            "oldal_nezetek",
            "latogatasok",
            "talalatok",
        ]

    def generate_data(self) -> int:
        return random.randint(0, 1000000)


# REAL Generators
class PriceGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "price",
            "cost",
            "amount",
            "value",
            "rate",
            "fee",
            # Hungarian
            "ar",
            "koltseg",
            "osszeg",
            "ertek",
            "tarifa",
            "dij",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(10.0, 1000.0), 2)


class WeightGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "weight",
            "mass",
            "heaviness",
            "load",
            # Hungarian
            "suly",
            "tomeg",
            "sulya",
            "teher",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(0.1, 100.0), 2)


class HeightGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "height",
            "elevation",
            "altitude",
            "tallness",
            # Hungarian
            "magassag",
            "emelkedes",
            "tenger_feletti_magassag",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(1.50, 2.10), 2)


class TemperatureGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "temperature",
            "temp",
            "degrees",
            "thermal_reading",
            # Hungarian
            "homerseklet",
            "fok",
            "hoszam",
            "termikus_ertek",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(-10.0, 40.0), 1)


class PercentageGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "percentage",
            "percent",
            "rate",
            "ratio",
            "proportion",
            # Hungarian
            "szazalek",
            "arany",
            "viszonyszam",
            "hanyad",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(0.0, 100.0), 2)


class LatitudeGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "latitude",
            "lat",
            "north_south",
            "parallel",
            # Hungarian
            "szelesseg",
            "eszaki_deli",
            "szelessegi_fok",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(-90.0, 90.0), 6)


class LongitudeGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "longitude",
            "lng",
            "lon",
            "east_west",
            "meridian",
            # Hungarian
            "hosszusag",
            "keleti_nyugati",
            "hosszusagi_fok",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(-180.0, 180.0), 6)


class DiscountGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "discount",
            "reduction",
            "markdown",
            "rebate",
            "deduction",
            # Hungarian
            "kedvezmeny",
            "csokkentes",
            "arleszallitas",
            "engedmeny",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(0.0, 0.5), 3)


class TaxRateGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "tax_rate",
            "tax_percentage",
            "levy_rate",
            "duty_rate",
            # Hungarian
            "ado_kulcs",
            "ado_szazalek",
            "adozasi_rata",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(0.05, 0.25), 3)


class ExchangeRateGenerator(BaseGenerator):
    def get_sql_type(self) -> str:
        return "REAL"

    def get_column_names(self) -> List[str]:
        return [
            # English
            "exchange_rate",
            "conversion_rate",
            "currency_rate",
            "forex_rate",
            # Hungarian
            "valtasi_arfolyam",
            "konverziós_rata",
            "deviza_arfolyam",
        ]

    def generate_data(self) -> float:
        return round(random.uniform(0.1, 5.0), 4)


# Registry of all available generators
AVAILABLE_GENERATORS = {
    # TEXT generators
    "name": NameGenerator,
    "first_name": FirstNameGenerator,
    "last_name": LastNameGenerator,
    "company": CompanyGenerator,
    "job_title": JobTitleGenerator,
    "email": EmailGenerator,
    "phone": PhoneGenerator,
    "address": AddressGenerator,
    "city": CityGenerator,
    "country": CountryGenerator,
    "description": DescriptionGenerator,
    "website": WebsiteGenerator,
    "username": UsernameGenerator,
    "license_plate": LicensePlateGenerator,
    "color": ColorGenerator,
    # INTEGER generators
    "age": AgeGenerator,
    "salary": SalaryGenerator,
    "employee_id": EmployeeIdGenerator,
    "quantity": QuantityGenerator,
    "year": YearGenerator,
    "score": ScoreGenerator,
    "rating": RatingGenerator,
    "order_count": OrderCountGenerator,
    "days_active": DaysActiveGenerator,
    "views": ViewsGenerator,
    # REAL generators
    "price": PriceGenerator,
    "weight": WeightGenerator,
    "height": HeightGenerator,
    "temperature": TemperatureGenerator,
    "percentage": PercentageGenerator,
    "latitude": LatitudeGenerator,
    "longitude": LongitudeGenerator,
    "discount": DiscountGenerator,
    "tax_rate": TaxRateGenerator,
    "exchange_rate": ExchangeRateGenerator,
}


def get_generator_by_name(generator_name: str) -> BaseGenerator:
    """Get a generator instance by its name"""
    if generator_name not in AVAILABLE_GENERATORS:
        raise ValueError(f"Unknown generator: {generator_name}")

    generator_class = AVAILABLE_GENERATORS[generator_name]
    return generator_class()


def get_generators_by_type(sql_type: str) -> List[str]:
    """Get all generator names for a specific SQL type"""
    generators = []
    for name, generator_class in AVAILABLE_GENERATORS.items():
        instance = generator_class()
        if instance.get_sql_type() == sql_type:
            generators.append(name)
    return generators


def get_all_generator_names() -> List[str]:
    """Get all available generator names"""
    return list(AVAILABLE_GENERATORS.keys())


# Example usage and testing
if __name__ == "__main__":
    print("=== Generator Definitions Demo ===\n")

    # Test each SQL type
    for sql_type in ["TEXT", "INTEGER", "REAL"]:
        print(f"SQL Type: {sql_type}")
        print("-" * 30)

        generators = get_generators_by_type(sql_type)
        for gen_name in generators[:3]:  # Show first 3 generators
            gen = get_generator_by_name(gen_name)
            print(f"Generator: {gen_name}")
            print(f"  Column names: {', '.join(gen.get_column_names()[:5])}...")
            print(f"  Sample data: {[gen.generate_data() for _ in range(3)]}")
        print()
