# =============================================================================
# src/data_loader.py
# Production-Level COVID Dataset Loader
# =============================================================================

import os
import logging
from datetime import datetime

import pandas as pd
import numpy as np

# =============================================================================
# LOGGER CONFIGURATION
# =============================================================================

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)

# =============================================================================
# BASE DIRECTORY CONFIGURATION
# =============================================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# =============================================================================
# DATA PATHS
# =============================================================================

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

# =============================================================================
# REQUIRED DATASET COLUMNS
# =============================================================================

REQUIRED_COLUMNS = [
    "country",
    "date",
    "new_cases",
    "new_deaths"
]

# =============================================================================
# COLUMN STANDARDIZATION MAPPING
# =============================================================================

COLUMN_MAPPING = {
    "location": "country",
    "entity": "country",
    "day": "date",
    "cases": "new_cases",
    "deaths": "new_deaths"
}

# =============================================================================
# COVID DATA LOADER CLASS
# =============================================================================


class CovidDataLoader:
    """
    Production-level data loader for
    COVID-19 analytics application.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(
        self,
        raw_data_path=RAW_DATA_PATH,
        processed_data_path=PROCESSED_DATA_PATH
    ):

        self.raw_data_path = raw_data_path

        self.processed_data_path = processed_data_path

        self.df = pd.DataFrame()

        logger.info(
            "CovidDataLoader Initialized"
        )

    # =========================================================================
    # LOAD RAW DATASET
    # =========================================================================

    def load_raw_dataset(self):
        """
        Load raw COVID dataset.
        """

        try:

            if not os.path.exists(
                self.raw_data_path
            ):

                raise FileNotFoundError(
                    f"Raw dataset not found: "
                    f"{self.raw_data_path}"
                )

            logger.info(
                f"Loading Raw Dataset: "
                f"{self.raw_data_path}"
            )

            self.df = pd.read_csv(
                self.raw_data_path
            )

            logger.info(
                f"Raw Dataset Loaded Successfully | "
                f"Shape: {self.df.shape}"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Error Loading Raw Dataset: "
                f"{error}"
            )

            raise

    # =========================================================================
    # LOAD PROCESSED DATASET
    # =========================================================================

    def load_processed_dataset(self):
        """
        Load processed COVID dataset.
        """

        try:

            if not os.path.exists(
                self.processed_data_path
            ):

                raise FileNotFoundError(
                    f"Processed dataset not found: "
                    f"{self.processed_data_path}"
                )

            logger.info(
                f"Loading Processed Dataset: "
                f"{self.processed_data_path}"
            )

            self.df = pd.read_csv(
                self.processed_data_path
            )

            logger.info(
                f"Processed Dataset Loaded Successfully | "
                f"Shape: {self.df.shape}"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Error Loading Processed Dataset: "
                f"{error}"
            )

            raise

    # =========================================================================
    # STANDARDIZE COLUMN NAMES
    # =========================================================================

    def standardize_columns(self):
        """
        Standardize dataset column names.
        """

        try:

            logger.info(
                "Standardizing Dataset Columns"
            )

            self.df.columns = [
                column.strip().lower()
                for column in self.df.columns
            ]

            for old_column, new_column in COLUMN_MAPPING.items():

                if old_column in self.df.columns:

                    self.df.rename(
                        columns={
                            old_column: new_column
                        },
                        inplace=True
                    )

            logger.info(
                "Column Standardization Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Column Standardization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # VALIDATE REQUIRED COLUMNS
    # =========================================================================

    def validate_columns(self):
        """
        Validate required dataset columns.
        """

        try:

            missing_columns = []

            for column in REQUIRED_COLUMNS:

                if column not in self.df.columns:

                    missing_columns.append(column)

            if missing_columns:

                logger.warning(
                    f"Missing Columns Found: "
                    f"{missing_columns}"
                )

                self.create_missing_columns(
                    missing_columns
                )

            logger.info(
                "Dataset Column Validation Completed"
            )

            return True

        except Exception as error:

            logger.error(
                f"Column Validation Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE MISSING COLUMNS
    # =========================================================================

    def create_missing_columns(
        self,
        missing_columns
    ):
        """
        Create missing dataset columns.
        """

        try:

            for column in missing_columns:

                if column == "country":

                    self.df[column] = "Unknown"

                elif column == "date":

                    self.df[column] = pd.NaT

                else:

                    self.df[column] = 0

            logger.info(
                "Missing Columns Created Successfully"
            )

        except Exception as error:

            logger.error(
                f"Failed To Create Missing Columns: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CONVERT DATE COLUMN
    # =========================================================================

    def convert_date_column(self):
        """
        Convert date column to datetime.
        """

        try:

            logger.info(
                "Converting Date Column"
            )

            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
            )

            logger.info(
                "Date Conversion Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Date Conversion Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # HANDLE NUMERIC COLUMNS
    # =========================================================================

    def clean_numeric_columns(self):
        """
        Clean numeric dataset columns.
        """

        try:

            numeric_columns = [
                "new_cases",
                "new_deaths"
            ]

            for column in numeric_columns:

                self.df[column] = pd.to_numeric(
                    self.df[column],
                    errors="coerce"
                ).fillna(0)

                self.df[column] = np.where(
                    self.df[column] < 0,
                    0,
                    self.df[column]
                )

            logger.info(
                "Numeric Columns Cleaned Successfully"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Numeric Cleaning Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # REMOVE DUPLICATES
    # =========================================================================

    def remove_duplicates(self):
        """
        Remove duplicate dataset rows.
        """

        try:

            initial_shape = self.df.shape

            self.df.drop_duplicates(
                inplace=True
            )

            final_shape = self.df.shape

            logger.info(
                f"Duplicates Removed | "
                f"Before: {initial_shape} | "
                f"After: {final_shape}"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Duplicate Removal Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # HANDLE COUNTRY COLUMN
    # =========================================================================

    def clean_country_column(self):
        """
        Clean country column values.
        """

        try:

            self.df["country"] = (
                self.df["country"]
                .astype(str)
                .replace("nan", "Unknown")
                .fillna("Unknown")
                .str.strip()
                .str.title()
            )

            logger.info(
                "Country Column Cleaned Successfully"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Country Cleaning Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # SORT DATASET
    # =========================================================================

    def sort_dataset(self):
        """
        Sort dataset by date.
        """

        try:

            self.df.sort_values(
                by="date",
                inplace=True
            )

            self.df.reset_index(
                drop=True,
                inplace=True
            )

            logger.info(
                "Dataset Sorted Successfully"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Dataset Sorting Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # SAVE PROCESSED DATASET
    # =========================================================================

    def save_processed_dataset(self):
        """
        Save cleaned dataset.
        """

        try:

            processed_dir = os.path.dirname(
                self.processed_data_path
            )

            os.makedirs(
                processed_dir,
                exist_ok=True
            )

            self.df.to_csv(
                self.processed_data_path,
                index=False
            )

            logger.info(
                f"Processed Dataset Saved: "
                f"{self.processed_data_path}"
            )

        except Exception as error:

            logger.error(
                f"Dataset Saving Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # COMPLETE DATA LOADING PIPELINE
    # =========================================================================

    def run_pipeline(self):
        """
        Execute complete dataset loading pipeline.
        """

        try:

            logger.info(
                "COVID Data Loading Pipeline Started"
            )

            self.load_raw_dataset()

            self.standardize_columns()

            self.validate_columns()

            self.convert_date_column()

            self.clean_numeric_columns()

            self.remove_duplicates()

            self.clean_country_column()

            self.sort_dataset()

            self.save_processed_dataset()

            logger.info(
                "COVID Data Loading Pipeline Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Pipeline Execution Failed: "
                f"{error}"
            )

            raise

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    loader = CovidDataLoader()

    covid_df = loader.run_pipeline()

    print("\nDataset Loaded Successfully")

    print("\nDataset Shape:")
    print(covid_df.shape)

    print("\nDataset Columns:")
    print(covid_df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(covid_df.head())