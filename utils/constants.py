# =============================================================================
# utils/constants.py
# Production-Level Constants Configuration
# COVID Data Analysis & Visualization Flask Application
# =============================================================================

import os

# =============================================================================
# APPLICATION INFORMATION
# =============================================================================

APP_NAME = "COVID-19 Data Analysis & Visualization"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "Production-Level Flask Application for "
    "COVID-19 Data Analysis, Visualization, "
    "Trend Analysis, and Dashboard Reporting"
)

AUTHOR_NAME = "OpenAI Project Template"

LICENSE_NAME = "MIT License"

# =============================================================================
# BASE DIRECTORY
# =============================================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# =============================================================================
# DATA DIRECTORIES
# =============================================================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

RAW_DATA_DIR = os.path.join(
    DATA_DIR,
    "raw"
)

PROCESSED_DATA_DIR = os.path.join(
    DATA_DIR,
    "processed"
)

REPORTS_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

LOGS_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

NOTEBOOKS_DIR = os.path.join(
    BASE_DIR,
    "notebooks"
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "static"
)

TEMPLATES_DIR = os.path.join(
    BASE_DIR,
    "templates"
)

VISUALIZATION_DIR = os.path.join(
    STATIC_DIR,
    "images",
    "visualizations"
)

# =============================================================================
# DATASET FILE PATHS
# =============================================================================

RAW_DATASET_PATH = os.path.join(
    RAW_DATA_DIR,
    "owid-covid-data (1).csv"
)

CLEANED_DATASET_PATH = os.path.join(
    PROCESSED_DATA_DIR,
    "cleaned_covid_data.csv"
)

FEATURED_DATASET_PATH = os.path.join(
    PROCESSED_DATA_DIR,
    "featured_covid_data.csv"
)

# =============================================================================
# DASHBOARD FILES
# =============================================================================

TABLEAU_LINKS_FILE = os.path.join(
    BASE_DIR,
    "dashboards",
    "tableau_dashboard_links.txt"
)

POWERBI_EXPORT_FILE = os.path.join(
    BASE_DIR,
    "dashboards",
    "powerbi_export.pdf"
)

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOG_FILE_PATH = os.path.join(
    LOGS_DIR,
    "app.log"
)

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

# =============================================================================
# FLASK CONFIGURATION
# =============================================================================

FLASK_HOST = "0.0.0.0"

FLASK_PORT = 5000

FLASK_DEBUG = True

SECRET_KEY = (
    "covid-analysis-secret-key"
)

JSON_SORT_KEYS = False

# =============================================================================
# API CONFIGURATION
# =============================================================================

API_VERSION = "v1"

API_PREFIX = "/api/v1"

DEFAULT_API_RESPONSE = {
    "status": "success",
    "message": "Request completed successfully"
}

ERROR_API_RESPONSE = {
    "status": "error",
    "message": "Something went wrong"
}

# =============================================================================
# DATASET REQUIRED COLUMNS
# =============================================================================

REQUIRED_COLUMNS = [

    "date",

    "country",

    "new_cases",

    "new_deaths"
]

# =============================================================================
# FEATURE ENGINEERING COLUMNS
# =============================================================================

ENGINEERED_FEATURE_COLUMNS = [

    "total_cases_country",

    "total_deaths_country",

    "total_vaccinations_country",

    "mortality_rate",

    "daily_growth_rate",

    "rolling_avg_cases",

    "rolling_avg_deaths",

    "rolling_avg_vaccinations",

    "severity_level",

    "is_hotspot",

    "year",

    "month",

    "day",

    "weekday",

    "quarter"
]

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================

FIGURE_WIDTH = 14

FIGURE_HEIGHT = 7

FIGURE_DPI = 120

IMAGE_FORMAT = "png"

CHART_STYLE = "default"

# =============================================================================
# TOP N SETTINGS
# =============================================================================

TOP_COUNTRIES_LIMIT = 10

TOP_HOTSPOTS_LIMIT = 10

TOP_VACCINATED_COUNTRIES = 10

# =============================================================================
# ROLLING WINDOW SETTINGS
# =============================================================================

ROLLING_WINDOW_DAYS = 7

MOVING_AVERAGE_WINDOW = 7

# =============================================================================
# HOTSPOT SETTINGS
# =============================================================================

HOTSPOT_PERCENTILE_THRESHOLD = 0.90

HOTSPOT_LABEL = "Hotspot"

NON_HOTSPOT_LABEL = "Normal"

# =============================================================================
# SEVERITY LEVEL SETTINGS
# =============================================================================

LOW_CASE_THRESHOLD = 1000

MEDIUM_CASE_THRESHOLD = 10000

SEVERITY_LOW = "Low"

SEVERITY_MEDIUM = "Medium"

SEVERITY_HIGH = "High"

# =============================================================================
# DATE SETTINGS
# =============================================================================

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

TIMEZONE = "UTC"

# =============================================================================
# REPORT SETTINGS
# =============================================================================

REPORT_TITLE = (
    "COVID-19 Analysis Report"
)

REPORT_ENCODING = "utf-8"

# =============================================================================
# FILE ENCODING SETTINGS
# =============================================================================

DEFAULT_ENCODING = "utf-8"

CSV_SEPARATOR = ","

# =============================================================================
# COUNTRY ANALYSIS DEFAULTS
# =============================================================================

DEFAULT_COUNTRY = "India"

COUNTRY_COLUMN = "country"

DATE_COLUMN = "date"

# =============================================================================
# NUMERIC COLUMNS
# =============================================================================

NUMERIC_COLUMNS = [

    "new_cases",

    "new_deaths"
]

# =============================================================================
# MISSING VALUE SETTINGS
# =============================================================================

DEFAULT_FILL_VALUE = 0

# =============================================================================
# HTTP STATUS CODES
# =============================================================================

HTTP_200_OK = 200

HTTP_400_BAD_REQUEST = 400

HTTP_404_NOT_FOUND = 404

HTTP_500_INTERNAL_SERVER_ERROR = 500

# =============================================================================
# TEMPLATE FILES
# =============================================================================

BASE_TEMPLATE = "base.html"

INDEX_TEMPLATE = "index.html"

DASHBOARD_TEMPLATE = "dashboard.html"

ANALYSIS_TEMPLATE = "analysis.html"

ABOUT_TEMPLATE = "about.html"

ERROR_404_TEMPLATE = "404.html"

ERROR_500_TEMPLATE = "500.html"

# =============================================================================
# STATIC FILE PATHS
# =============================================================================

CSS_FILE = os.path.join(
    STATIC_DIR,
    "css",
    "style.css"
)

JS_FILE = os.path.join(
    STATIC_DIR,
    "js",
    "dashboard.js"
)

LOGO_FILE = os.path.join(
    STATIC_DIR,
    "images",
    "logo.png"
)

# =============================================================================
# VISUALIZATION IMAGE FILES
# =============================================================================

GLOBAL_CASES_TREND_IMAGE = (
    "global_cases_trend.png"
)

GLOBAL_DEATHS_TREND_IMAGE = (
    "global_deaths_trend.png"
)

GLOBAL_VACCINATION_TREND_IMAGE = (
    "global_vaccination_trend.png"
)

TOP_COUNTRIES_CASES_IMAGE = (
    "top_countries_cases.png"
)

HOTSPOTS_IMAGE = (
    "covid_hotspots.png"
)

INDIA_TREND_IMAGE = (
    "india_cases_trend.png"
)

MORTALITY_RATE_IMAGE = (
    "mortality_rate_chart.png"
)

# =============================================================================
# TESTING CONFIGURATION
# =============================================================================

TEST_DATASET_PATH = os.path.join(
    RAW_DATA_DIR,
    "test_compact.csv"
)

TESTING_MODE = True

# =============================================================================
# CACHE SETTINGS
# =============================================================================

CACHE_TIMEOUT = 300

ENABLE_CACHE = True

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = False

# =============================================================================
# CREATE REQUIRED DIRECTORIES
# =============================================================================

REQUIRED_DIRECTORIES = [

    DATA_DIR,

    RAW_DATA_DIR,

    PROCESSED_DATA_DIR,

    REPORTS_DIR,

    LOGS_DIR,

    MODELS_DIR,

    NOTEBOOKS_DIR,

    STATIC_DIR,

    TEMPLATES_DIR,

    VISUALIZATION_DIR
]

# =============================================================================
# AUTO CREATE DIRECTORIES
# =============================================================================

for directory in REQUIRED_DIRECTORIES:

    os.makedirs(
        directory,
        exist_ok=True
    )

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    print(
        "\nCOVID Constants Module Loaded Successfully"
    )

    print(
        "\nApplication Name:"
    )

    print(
        APP_NAME
    )

    print(
        "\nApplication Version:"
    )

    print(
        APP_VERSION
    )

    print(
        "\nRaw Dataset Path:"
    )

    print(
        RAW_DATASET_PATH
    )

    print(
        "\nProcessed Dataset Path:"
    )

    print(
        CLEANED_DATASET_PATH
    )

    print(
        "\nVisualization Directory:"
    )

    print(
        VISUALIZATION_DIR
    )

    print(
        "\nRequired Columns:"
    )

    print(
        REQUIRED_COLUMNS
    )