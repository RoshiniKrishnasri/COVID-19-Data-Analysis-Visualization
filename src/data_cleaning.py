# =============================================================================
# src/data_cleaning.py
# Production-Level COVID Data Cleaning Module
# =============================================================================

import os
import logging

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
# REQUIRED COLUMNS
# =============================================================================

REQUIRED_COLUMNS = [
    "country",
    "date",
    "new_cases",
    "new_deaths"
]

# =============================================================================
# DATA CLEANING CLASS
# =============================================================================


class CovidDataCleaning:
    """
    Production-level COVID dataset
    cleaning and preprocessing class.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(
        self,
        input_path=RAW_DATA_PATH,
        output_path=PROCESSED_DATA_PATH
    ):

        self.input_path = input_path

        self.output_path = output_path

        self.df = pd.DataFrame()

        logger.info(
            "CovidDataCleaning Initialized"
        )

    # =========================================================================
    # LOAD DATASET
    # =========================================================================

    def load_dataset(self):
        """
        Load dataset from CSV file.
        """

        try:

            if not os.path.exists(
                self.input_path
            ):

                raise FileNotFoundError(
                    f"Dataset not found: "
                    f"{self.input_path}"
                )

            logger.info(
                f"Loading Dataset: "
                f"{self.input_path}"
            )

            self.df = pd.read_csv(
                self.input_path
            )

            logger.info(
                f"Dataset Loaded Successfully | "
                f"Shape: {self.df.shape}"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Dataset Loading Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # NORMALIZE COLUMN NAMES
    # =========================================================================

    def normalize_columns(self):
        """
        Normalize dataset column names.
        """

        try:

            logger.info(
                "Normalizing Dataset Columns"
            )

            self.df.columns = [
                column.strip().lower()
                for column in self.df.columns
            ]

            column_mapping = {
                "location": "country",
                "entity": "country",
                "day": "date",
                "cases": "new_cases",
                "deaths": "new_deaths"
            }

            for old_col, new_col in column_mapping.items():

                if old_col in self.df.columns:

                    self.df.rename(
                        columns={
                            old_col: new_col
                        },
                        inplace=True
                    )

            logger.info(
                "Column Normalization Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Column Normalization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # VALIDATE DATASET STRUCTURE
    # =========================================================================

    def validate_dataset(self):
        """
        Validate dataset structure.
        """

        try:

            logger.info(
                "Validating Dataset Structure"
            )

            missing_columns = []

            for column in REQUIRED_COLUMNS:

                if column not in self.df.columns:

                    missing_columns.append(column)

            if missing_columns:

                logger.warning(
                    f"Missing Columns: "
                    f"{missing_columns}"
                )

                self.add_missing_columns(
                    missing_columns
                )

            logger.info(
                "Dataset Validation Completed"
            )

            return True

        except Exception as error:

            logger.error(
                f"Dataset Validation Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # ADD MISSING COLUMNS
    # =========================================================================

    def add_missing_columns(
        self,
        missing_columns
    ):
        """
        Add missing columns with default values.
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
                "Missing Columns Added Successfully"
            )

        except Exception as error:

            logger.error(
                f"Adding Missing Columns Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CLEAN DATE COLUMN
    # =========================================================================

    def clean_date_column(self):
        """
        Clean and convert date column.
        """

        try:

            logger.info(
                "Cleaning Date Column"
            )

            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
            )

            invalid_dates = (
                self.df["date"]
                .isnull()
                .sum()
            )

            logger.info(
                f"Invalid Dates Found: "
                f"{invalid_dates}"
            )

            self.df = self.df[
                self.df["date"].notna()
            ]

            logger.info(
                "Date Cleaning Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Date Cleaning Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CLEAN COUNTRY COLUMN
    # =========================================================================

    def clean_country_column(self):
        """
        Clean country column values.
        """

        try:

            logger.info(
                "Cleaning Country Column"
            )

            self.df["country"] = (
                self.df["country"]
                .astype(str)
                .replace("nan", "Unknown")
                .fillna("Unknown")
                .str.strip()
                .str.title()
            )

            logger.info(
                "Country Cleaning Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Country Cleaning Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CLEAN NUMERIC COLUMNS
    # =========================================================================

    def clean_numeric_columns(self):
        """
        Clean numeric dataset columns.
        """

        try:

            logger.info(
                "Cleaning Numeric Columns"
            )

            numeric_columns = [
                "new_cases",
                "new_deaths"
            ]

            for column in numeric_columns:

                self.df[column] = pd.to_numeric(
                    self.df[column],
                    errors="coerce"
                )

                self.df[column] = (
                    self.df[column]
                    .fillna(0)
                )

                self.df[column] = np.where(
                    self.df[column] < 0,
                    0,
                    self.df[column]
                )

            logger.info(
                "Numeric Cleaning Completed"
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

            logger.info(
                "Removing Duplicate Rows"
            )

            initial_rows = len(self.df)

            self.df.drop_duplicates(
                inplace=True
            )

            final_rows = len(self.df)

            removed_rows = (
                initial_rows - final_rows
            )

            logger.info(
                f"Duplicate Rows Removed: "
                f"{removed_rows}"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Duplicate Removal Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # HANDLE MISSING VALUES
    # =========================================================================

    def handle_missing_values(self):
        """
        Handle remaining missing values.
        """

        try:

            logger.info(
                "Handling Missing Values"
            )

            numeric_columns = [
                "new_cases",
                "new_deaths"
            ]

            self.df[numeric_columns] = (
                self.df[numeric_columns]
                .fillna(0)
            )

            self.df["country"] = (
                self.df["country"]
                .fillna("Unknown")
            )

            logger.info(
                "Missing Value Handling Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Missing Value Handling Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # SORT DATASET
    # =========================================================================

    def sort_dataset(self):
        """
        Sort dataset chronologically.
        """

        try:

            logger.info(
                "Sorting Dataset"
            )

            self.df.sort_values(
                by=["country", "date"],
                inplace=True
            )

            self.df.reset_index(
                drop=True,
                inplace=True
            )

            logger.info(
                "Dataset Sorting Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Dataset Sorting Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # FEATURE PREPARATION
    # =========================================================================

    def prepare_features(self):
        """
        Prepare analytical features.
        """

        try:

            logger.info(
                "Preparing Analytical Features"
            )

            self.df["year"] = (
                self.df["date"]
                .dt.year
            )

            self.df["month"] = (
                self.df["date"]
                .dt.month
            )

            self.df["day"] = (
                self.df["date"]
                .dt.day
            )

            self.df["day_name"] = (
                self.df["date"]
                .dt.day_name()
            )

            logger.info(
                "Feature Preparation Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Feature Preparation Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # DATA QUALITY REPORT
    # =========================================================================

    def generate_data_quality_report(self):
        """
        Generate data quality summary.
        """

        try:

            logger.info(
                "Generating Data Quality Report"
            )

            report = {
                "total_rows": len(self.df),
                "total_columns": len(
                    self.df.columns
                ),
                "missing_values": (
                    self.df.isnull()
                    .sum()
                    .to_dict()
                ),
                "duplicate_rows": (
                    self.df.duplicated()
                    .sum()
                ),
                "date_range": {
                    "start_date": str(
                        self.df["date"].min()
                    ),
                    "end_date": str(
                        self.df["date"].max()
                    ),
                },
                "countries": (
                    self.df["country"]
                    .nunique()
                ),
            }

            logger.info(
                "Data Quality Report Generated"
            )

            return report

        except Exception as error:

            logger.error(
                f"Quality Report Generation Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # SAVE CLEANED DATASET
    # =========================================================================

    def save_cleaned_dataset(self):
        """
        Save cleaned dataset to CSV.
        """

        try:

            output_directory = os.path.dirname(
                self.output_path
            )

            os.makedirs(
                output_directory,
                exist_ok=True
            )

            self.df.to_csv(
                self.output_path,
                index=False
            )

            logger.info(
                f"Cleaned Dataset Saved: "
                f"{self.output_path}"
            )

        except Exception as error:

            logger.error(
                f"Saving Dataset Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # COMPLETE CLEANING PIPELINE
    # =========================================================================

    def run_cleaning_pipeline(self):
        """
        Execute complete cleaning pipeline.
        """

        try:

            logger.info(
                "COVID Data Cleaning Pipeline Started"
            )

            self.load_dataset()

            self.normalize_columns()

            self.validate_dataset()

            self.clean_date_column()

            self.clean_country_column()

            self.clean_numeric_columns()

            self.remove_duplicates()

            self.handle_missing_values()

            self.sort_dataset()

            self.prepare_features()

            quality_report = (
                self.generate_data_quality_report()
            )

            self.save_cleaned_dataset()

            logger.info(
                "COVID Data Cleaning Pipeline Completed"
            )

            return (
                self.df,
                quality_report
            )

        except Exception as error:

            logger.error(
                f"Cleaning Pipeline Failed: "
                f"{error}"
            )

            raise

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    cleaner = CovidDataCleaning()

    cleaned_df, report = (
        cleaner.run_cleaning_pipeline()
    )

    print("\nCOVID Data Cleaning Completed")

    print("\nDataset Shape:")
    print(cleaned_df.shape)

    print("\nDataset Columns:")
    print(cleaned_df.columns.tolist())

    print("\nData Quality Report:")
    print(report)

    print("\nFirst 5 Rows:")
    print(cleaned_df.head())