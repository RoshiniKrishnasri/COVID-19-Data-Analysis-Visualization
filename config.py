import os
from datetime import timedelta

# =============================================================================
# BASE DIRECTORY
# =============================================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

class Config:
    """
    Base configuration class.
    """

    # -------------------------------------------------------------------------
    # GENERAL SETTINGS
    # -------------------------------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "covid-dashboard-secret-key"
    )

    DEBUG = False

    TESTING = False

    # -------------------------------------------------------------------------
    # SERVER SETTINGS
    # -------------------------------------------------------------------------

    HOST = os.getenv("FLASK_HOST", "0.0.0.0")

    PORT = int(
        os.getenv("FLASK_PORT", 5000)
    )

    # -------------------------------------------------------------------------
    # SESSION CONFIGURATION
    # -------------------------------------------------------------------------

    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=2
    )

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_SAMESITE = "Lax"

    # -------------------------------------------------------------------------
    # JSON CONFIGURATION
    # -------------------------------------------------------------------------

    JSON_SORT_KEYS = False

    JSONIFY_PRETTYPRINT_REGULAR = True

    # -------------------------------------------------------------------------
    # DATASET CONFIGURATION
    # -------------------------------------------------------------------------

    DATASET_URL = (
        "https://catalog.ourworldindata.org/"
        "garden/covid/latest/compact/compact.csv"
    )

    RAW_DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "owid-covid-data (1).csv"
    )

    PROCESSED_DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "cleaned_covid_data.csv"
    )

    # -------------------------------------------------------------------------
    # DATA REFRESH SETTINGS
    # -------------------------------------------------------------------------

    AUTO_REFRESH_DATASET = True

    DATA_REFRESH_INTERVAL_HOURS = 24

    # -------------------------------------------------------------------------
    # LOGGING CONFIGURATION
    # -------------------------------------------------------------------------

    LOG_LEVEL = "INFO"

    LOG_DIR = os.path.join(
        BASE_DIR,
        "logs"
    )

    LOG_FILE = os.path.join(
        LOG_DIR,
        "app.log"
    )

    LOG_MAX_BYTES = 10240

    LOG_BACKUP_COUNT = 10

    # -------------------------------------------------------------------------
    # CACHE CONFIGURATION
    # -------------------------------------------------------------------------

    CACHE_TYPE = "simple"

    CACHE_DEFAULT_TIMEOUT = 300

    # -------------------------------------------------------------------------
    # API CONFIGURATION
    # -------------------------------------------------------------------------

    API_TITLE = "COVID-19 Analytics API"

    API_VERSION = "v1"

    API_PREFIX = "/api"

    # -------------------------------------------------------------------------
    # CORS CONFIGURATION
    # -------------------------------------------------------------------------

    CORS_HEADERS = "Content-Type"

    # -------------------------------------------------------------------------
    # PAGINATION SETTINGS
    # -------------------------------------------------------------------------

    DEFAULT_PAGE_SIZE = 20

    MAX_PAGE_SIZE = 100

    # -------------------------------------------------------------------------
    # DASHBOARD SETTINGS
    # -------------------------------------------------------------------------

    DEFAULT_COUNTRY = "India"

    TOP_HOTSPOT_LIMIT = 10

    DEFAULT_CHART_DAYS = 30

    # -------------------------------------------------------------------------
    # PLOT SETTINGS
    # -------------------------------------------------------------------------

    CHART_HEIGHT = 500

    CHART_WIDTH = 1000

    ENABLE_ANIMATIONS = True

    # -------------------------------------------------------------------------
    # SECURITY SETTINGS
    # -------------------------------------------------------------------------

    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
    }

    # -------------------------------------------------------------------------
    # FILE UPLOAD CONFIGURATION
    # -------------------------------------------------------------------------

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"csv"}

    # -------------------------------------------------------------------------
    # PERFORMANCE SETTINGS
    # -------------------------------------------------------------------------

    ENABLE_COMPRESSION = True

    THREADS_PER_PAGE = 2

    # -------------------------------------------------------------------------
    # ANALYTICS SETTINGS
    # -------------------------------------------------------------------------

    ENABLE_ADVANCED_ANALYTICS = True

    ENABLE_FORECASTING = False

    ENABLE_HEATMAP_ANALYSIS = True

    ENABLE_TIME_SERIES_ANALYSIS = True

    # -------------------------------------------------------------------------
    # FEATURE FLAGS
    # -------------------------------------------------------------------------

    FEATURES = {
        "global_dashboard": True,
        "country_analysis": True,
        "vaccination_analysis": True,
        "hotspot_detection": True,
        "trend_analysis": True,
        "download_reports": True,
    }


# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

class DevelopmentConfig(Config):
    """
    Development environment configuration.
    """

    DEBUG = True

    ENV = "development"

    SESSION_COOKIE_SECURE = False

    LOG_LEVEL = "DEBUG"


# =============================================================================
# TESTING CONFIGURATION
# =============================================================================

class TestingConfig(Config):
    """
    Testing environment configuration.
    """

    TESTING = True

    DEBUG = True

    ENV = "testing"

    WTF_CSRF_ENABLED = False


# =============================================================================
# PRODUCTION CONFIGURATION
# =============================================================================

class ProductionConfig(Config):
    """
    Production environment configuration.
    """

    DEBUG = False

    ENV = "production"

    SESSION_COOKIE_SECURE = True

    LOG_LEVEL = "WARNING"


# =============================================================================
# CONFIGURATION MAPPING
# =============================================================================

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

# =============================================================================
# ACTIVE CONFIGURATION
# =============================================================================

ACTIVE_CONFIG = os.getenv(
    "FLASK_ENV",
    "development"
)

CurrentConfig = config_by_name.get(
    ACTIVE_CONFIG,
    DevelopmentConfig
)

# =============================================================================
# DIRECTORY INITIALIZATION
# =============================================================================

required_directories = [
    os.path.join(BASE_DIR, "logs"),
    os.path.join(BASE_DIR, "data"),
    os.path.join(BASE_DIR, "data", "raw"),
    os.path.join(BASE_DIR, "data", "processed"),
]

for directory in required_directories:

    if not os.path.exists(directory):

        os.makedirs(directory)

# =============================================================================
# CONFIG VALIDATION
# =============================================================================

def validate_config():
    """
    Validate critical configuration values.
    """

    errors = []

    if not Config.SECRET_KEY:
        errors.append(
            "SECRET_KEY is missing."
        )

    if not isinstance(
        Config.PORT,
        int
    ):
        errors.append(
            "PORT must be an integer."
        )

    if Config.DEFAULT_PAGE_SIZE <= 0:
        errors.append(
            "DEFAULT_PAGE_SIZE must be positive."
        )

    if errors:

        raise ValueError(
            "Configuration Validation Failed:\n"
            + "\n".join(errors)
        )

# =============================================================================
# RUN CONFIG VALIDATION
# =============================================================================

validate_config()