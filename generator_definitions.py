"""
Generator definitions with column names and data generation functions.
Each generator inherits from BaseGenerator and defines its own column names and data generation logic.
"""

import random
from abc import ABC, abstractmethod
from typing import Any, List

from config import CONFIG, fake
from manipulators import (
    BaseManipulator,
    LowercaseManipulator,
    ManipulatorApplier,
    ManipulatorFactory,
    NullManipulator,
    TrashManipulator,
    UppercaseManipulator,
)


class BaseGenerator(ABC):
    """Base class for all data generators"""

    def __init__(self):
        self.sql_type = self.get_sql_type()
        self.column_names = self.get_column_names()
        self.manipulator_applier = ManipulatorApplier(self.get_manipulators())

    @abstractmethod
    def get_name(self) -> str:
        """Return the unique name identifier for this generator"""
        pass

    @abstractmethod
    def get_sql_type(self) -> str:
        """Return the SQL data type for this generator"""
        pass

    @abstractmethod
    def get_column_names(self) -> List[str]:
        """Return list of possible column names in multiple languages"""
        pass

    @abstractmethod
    def generate_raw_data(self) -> Any:
        """Generate a single raw data value (before manipulations)"""
        pass

    def get_manipulators(self) -> List[BaseManipulator]:
        """
        Return a list of manipulators to be applied to the generated data.
        Override this method in subclasses to define specific manipulators.
        """
        return []

    def generate_data(self) -> Any:
        """Generate data with manipulations applied"""
        raw_value = self.generate_raw_data()
        return self.manipulator_applier.apply_manipulations(raw_value, self.sql_type)

    def get_random_column_name(self) -> str:
        """Get a random column name from the available options"""
        return random.choice(self.column_names)


def create_test_manipulator() -> list[BaseManipulator]:
    """Create a test manipulator for demonstration purposes"""
    return ManipulatorFactory.create(
        [
            (
                NullManipulator.create(probability=0.3),
                0.75,
            ),
            (
                TrashManipulator.create(probability=0.3),
                1.0,
            ),
            (
                UppercaseManipulator.create(probability=0.1),
                1.0,
            ),
            (
                LowercaseManipulator.create(probability=0.05),
                1.0,
            ),
        ]
    )


# TEXT Generators
class NameGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "name"

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

    def generate_raw_data(self) -> str:
        return fake.name()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class FirstNameGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "first_name"

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

    def generate_raw_data(self) -> str:
        return fake.first_name()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class LastNameGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "last_name"

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

    def generate_raw_data(self) -> str:
        return fake.last_name()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class CompanyGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "company"

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

    def generate_raw_data(self) -> str:
        return fake.company()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class JobTitleGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "job_title"

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

    def generate_raw_data(self) -> str:
        return fake.job()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class EmailGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "email"

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

    def generate_raw_data(self) -> str:
        return fake.email()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class PhoneGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "phone"

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

    def generate_raw_data(self) -> str:
        return fake.phone_number()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class AddressGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "address"

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

    def generate_raw_data(self) -> str:
        return fake.address()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class CityGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "city"

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

    def generate_raw_data(self) -> str:
        return fake.city()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class CountryGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "country"

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

    def generate_raw_data(self) -> str:
        return fake.country()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class DescriptionGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "description"

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

    def generate_raw_data(self) -> str:
        return fake.text(max_nb_chars=200)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class WebsiteGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "website"

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

    def generate_raw_data(self) -> str:
        return fake.url()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class UsernameGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "username"

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

    def generate_raw_data(self) -> str:
        return fake.user_name()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class LicensePlateGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "license_plate"

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

    def generate_raw_data(self) -> str:
        return fake.license_plate()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class ColorGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "color"

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

    def generate_raw_data(self) -> str:
        return fake.color_name()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


# INTEGER Generators
class AgeGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "age"

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

    def generate_raw_data(self) -> int:
        return random.randint(18, 90)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class SalaryGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "salary"

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

    def generate_raw_data(self) -> int:
        return random.randint(30000, 150000)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class EmployeeIdGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "employee_id"

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

    def generate_raw_data(self) -> int:
        return random.randint(1000, 9999)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class QuantityGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "quantity"

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

    def generate_raw_data(self) -> int:
        return random.randint(1, 1000)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class YearGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "year"

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

    def generate_raw_data(self) -> int:
        return random.randint(1950, 2024)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class ScoreGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "score"

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

    def generate_raw_data(self) -> int:
        return random.randint(0, 100)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class RatingGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "rating"

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

    def generate_raw_data(self) -> int:
        return random.randint(1, 5)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class OrderCountGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "order_count"

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

    def generate_raw_data(self) -> int:
        return random.randint(0, 50)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class DaysActiveGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "days_active"

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

    def generate_raw_data(self) -> int:
        return random.randint(0, 365)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class ViewsGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "views"

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

    def generate_raw_data(self) -> int:
        return random.randint(0, 1000000)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


# REAL Generators
class PriceGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "price"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(10.0, 1000.0), 2)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class WeightGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "weight"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(0.1, 100.0), 2)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class HeightGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "height"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(1.50, 2.10), 2)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class TemperatureGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "temperature"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(-10.0, 40.0), 1)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class PercentageGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "percentage"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(0.0, 100.0), 2)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class LatitudeGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "latitude"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(-90.0, 90.0), 6)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class LongitudeGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "longitude"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(-180.0, 180.0), 6)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class DiscountGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "discount"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(0.0, 0.5), 3)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class TaxRateGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "tax_rate"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(0.05, 0.25), 3)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class ExchangeRateGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "exchange_rate"

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

    def generate_raw_data(self) -> float:
        return round(random.uniform(0.1, 5.0), 4)

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()

class CustomerIDGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "customer_id"

    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            "customer_id",
            "customer_identifier",
            "customer_primary_id",
            "client_id",
            "client_identifier",
            "client_primary_id",
            "user_id",
            "user_identifier",
            "user_primary_id",
            "account_id",
            "account_identifier",
            "account_primary_id",
            "member_id",
            "member_identifier",
            # hungarian
            "ugyfel_id",
            "ugyfel_azonosito",
            "ugyfel_fo_id",
            "kliens_id",
            "kliens_azonosito",
            "kliens_fo_id",
            "felhasznalo_id",
            "felhasznalo_azonosito",
            "felhasznalo_fo_id",
        ]

    def generate_raw_data(self) -> int:
        prefix = random.choice([18, 72])
        suffix = random.randint(100000, 999999)
        return int(f"{prefix}{suffix}") 

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()


class OrderIDGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "order_id"

    def get_sql_type(self) -> str:
        return "INTEGER"

    def get_column_names(self) -> List[str]:
        return [
            "order_id",
            "order_number",
            "purchase_id",
            "transaction_id",
            "sales_id",
            "order_reference",
            "order_primary_id",
            "purchase_reference",
            "transaction_reference",
            # hungarian
            "rendeles_id",
            "rendeles_szam",
            "vasarlas_id",
            "tranzakcio_id",
            "eladas_id",
            "rendeles_hivatkozas",
            "rendeles_fo_id",
        ]

    def generate_raw_data(self) -> int:
        prefix = random.choice([12, 92])
        suffix = random.randint(100000, 999999)
        return int(f"{prefix}{suffix}")

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()
    
class BankAccountNumberGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "bank_account_number"

    def get_sql_type(self) -> str:
        return "TEXT"

    def get_column_names(self) -> List[str]:
        return [
            "bank_account_number",
            "account_number",
            "iban",
            "bank_account",
            "financial_account",
            # Hungarian
            "bankszamla_szam",
            "szamlaszam",
            "iban_szam",
            "penzugyi_szamla",
        ]

    def generate_raw_data(self) -> str:
        return fake.bban()

    def get_manipulators(self) -> List[BaseManipulator]:
        return create_test_manipulator()

# Registry of all available generators
AVAILABLE_GENERATORS: List[type[BaseGenerator]] = [
    # TEXT generators
    NameGenerator,
    FirstNameGenerator,
    LastNameGenerator,
    CompanyGenerator,
    JobTitleGenerator,
    EmailGenerator,
    PhoneGenerator,
    AddressGenerator,
    CityGenerator,
    CountryGenerator,
    DescriptionGenerator,
    WebsiteGenerator,
    UsernameGenerator,
    LicensePlateGenerator,
    ColorGenerator,

    # INTEGER generators
    AgeGenerator,
    # SalaryGenerator,
    EmployeeIdGenerator,
    QuantityGenerator,
    YearGenerator,
    # ScoreGenerator,
    # RatingGenerator,
    # OrderCountGenerator,
    # DaysActiveGenerator,
    # ViewsGenerator,
    # CustomerIDGenerator,
    OrderIDGenerator,
    BankAccountNumberGenerator,

    # REAL generators
    # PriceGenerator,
    # WeightGenerator,
    # HeightGenerator,
    TemperatureGenerator,
    # PercentageGenerator,
    LatitudeGenerator,
    LongitudeGenerator,
    # DiscountGenerator,
    # TaxRateGenerator,
    # ExchangeRateGenerator,
]


def get_generator_by_name(generator_name: str) -> BaseGenerator:
    """Get a generator instance by its name"""
    for generator_class in AVAILABLE_GENERATORS:
        generator_instance = generator_class()
        if generator_instance.get_name() == generator_name:
            return generator_instance

    raise ValueError(f"Unknown generator: {generator_name}")


def get_generators_by_type(sql_type: str) -> List[BaseGenerator]:
    """Get all generator instances for a specific SQL type"""
    generators: List[BaseGenerator] = []
    for generator_class in AVAILABLE_GENERATORS:
        generator_instance = generator_class()
        if generator_instance.get_sql_type() == sql_type:
            generators.append(generator_instance)
    return generators


def get_all_generator_names() -> List[str]:
    """Get all available generator names"""
    names: List[str] = []
    for generator_class in AVAILABLE_GENERATORS:
        generator_instance = generator_class()
        names.append(generator_instance.get_name())
    return names


def get_random_generator_weighted() -> BaseGenerator:
    """Get a random generator instance based on SQL type weights"""
    # Define weights for each SQL type
    type_weights = {
        "TEXT": CONFIG.GENERATOR_WEIGHTS.TEXT_WEIGHT,
        "INTEGER": CONFIG.GENERATOR_WEIGHTS.INTEGER_WEIGHT,
        "REAL": CONFIG.GENERATOR_WEIGHTS.REAL_WEIGHT,
    }

    # Create a weighted list of types
    weighted_types: List[str] = []
    for sql_type, weight in type_weights.items():
        weighted_types.extend(
            [sql_type] * int(weight * 10)
        )  # Multiply by 10 for better distribution

    # Select a random type based on weights
    selected_type = random.choice(weighted_types)

    # Get all generators for that type
    generators_for_type = get_generators_by_type(selected_type)

    # Return a random generator from that list
    if not generators_for_type:
        raise ValueError(f"No generators found for SQL type: {selected_type}")

    return random.choice(generators_for_type)
