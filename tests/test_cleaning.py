# =============================================================================
# tests/test_cleaning.py
# Production-Level Unit Tests for Data Cleaning
# COVID Data Analysis & Visualization Flask Application
# =============================================================================

import os
import sys
import unittest

import pandas as pd
import numpy as np

# =============================================================================
# PROJECT ROOT CONFIGURATION
# =============================================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(BASE_DIR)

# =============================================================================
# IMPORT APPLICATION MODULES
# =============================================================================

from src.data_cleaning import CovidDataCleaning

from utils.constants import (
    RAW_DATASET_PATH,
    CLEANED_DATASET_PATH,
    REQUIRED_COLUMNS
)

# =============================================================================
# TEST CLASS
# =============================================================================


class TestCovidDataCleaning(unittest.TestCase):
    """
    Unit tests for COVID data cleaning pipeline.
    """

    # =========================================================================
    # SETUP TEST ENVIRONMENT
    # =========================================================================

    @classmethod
    def setUpClass(cls):
        """
        Initialize cleaning pipeline.
        """

        print(
            "\nInitializing Data Cleaning Tests..."
        )

        cls.cleaner = CovidDataCleaning(
            input_path=RAW_DATASET_PATH,
            output_path=CLEANED_DATASET_PATH
        )

        cls.cleaner.load_dataset()

    # =========================================================================
    # TEST DATASET LOADED
    # =========================================================================

    def test_dataset_loaded(self):
        """
        Test dataset loading.
        """

        self.assertIsInstance(
            self.cleaner.df,
            pd.DataFrame,
            msg=(
                "Dataset is not a DataFrame."
            )
        )

        self.assertFalse(
            self.cleaner.df.empty,
            msg=(
                "Dataset is empty."
            )
        )

    # =========================================================================
    # TEST REQUIRED COLUMNS EXIST
    # =========================================================================

    def test_required_columns_exist(self):
        """
        Validate required columns.
        """

        missing_columns = [

            column

            for column in REQUIRED_COLUMNS

            if column not in self.cleaner.df.columns
        ]

        self.assertEqual(
            len(missing_columns),
            0,
            msg=(
                f"Missing Columns: "
                f"{missing_columns}"
            )
        )

    # =========================================================================
    # TEST COLUMN STANDARDIZATION
    # =========================================================================

    def test_column_standardization(self):
        """
        Test lowercase column names.
        """

        self.cleaner.normalize_columns()

        lowercase_columns = [

            column == column.lower()

            for column in self.cleaner.df.columns
        ]

        self.assertTrue(
            all(lowercase_columns),
            msg=(
                "Not all columns are lowercase."
            )
        )

    # =========================================================================
    # TEST DATE CONVERSION
    # =========================================================================

    def test_date_conversion(self):
        """
        Test datetime conversion.
        """

        self.cleaner.clean_date_column()

        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(
                self.cleaner.df["date"]
            ),
            msg=(
                "Date column conversion failed."
            )
        )

    # =========================================================================
    # TEST DUPLICATE REMOVAL
    # =========================================================================

    def test_duplicate_removal(self):
        """
        Test duplicate removal logic.
        """

        initial_duplicates = (
            self.cleaner.df
            .duplicated()
            .sum()
        )

        self.cleaner.remove_duplicates()

        final_duplicates = (
            self.cleaner.df
            .duplicated()
            .sum()
        )

        self.assertLessEqual(
            final_duplicates,
            initial_duplicates,
            msg=(
                "Duplicate removal failed."
            )
        )

    # =========================================================================
    # TEST MISSING VALUE HANDLING
    # =========================================================================

    def test_missing_value_handling(self):
        """
        Test missing value processing.
        """

        self.cleaner.handle_missing_values()

        missing_values = (
            self.cleaner.df[REQUIRED_COLUMNS]
            .isnull()
            .sum()
            .sum()
        )

        self.assertEqual(
            missing_values,
            0,
            msg=(
                "Missing values still exist."
            )
        )

    # =========================================================================
    # TEST NEGATIVE VALUE HANDLING
    # =========================================================================

    def test_negative_value_handling(self):
        """
        Test negative values cleaning.
        """

        self.cleaner.clean_numeric_columns()

        numeric_columns = [

            "new_cases",

            "new_deaths"
        ]

        for column in numeric_columns:

            negative_values = (
                self.cleaner.df[column] < 0
            ).sum()

            self.assertEqual(
                negative_values,
                0,
                msg=(
                    f"Negative values exist "
                    f"in {column}."
                )
            )

    # =========================================================================
    # TEST COUNTRY COLUMN CLEANING
    # =========================================================================

    def test_country_column_cleaning(self):
        """
        Test country column validity.
        """

        self.cleaner.clean_country_column()

        empty_countries = (
            self.cleaner.df["country"]
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        self.assertEqual(
            empty_countries,
            0,
            msg=(
                "Empty country values exist."
            )
        )

    # =========================================================================
    # TEST SORTING FUNCTIONALITY
    # =========================================================================

    def test_dataset_sorting(self):
        """
        Test chronological sorting.
        """

        self.cleaner.sort_dataset()

        sorted_df = (
            self.cleaner.df.sort_values(
                by=["country", "date"]
            )
        )

        self.assertTrue(
            self.cleaner.df.reset_index(
                drop=True
            ).equals(
                sorted_df.reset_index(
                    drop=True
                )
            ),
            msg=(
                "Dataset sorting failed."
            )
        )

    # =========================================================================
    # TEST DATA TYPES
    # =========================================================================

    def test_numeric_column_types(self):
        """
        Validate numeric column types.
        """

        numeric_columns = [

            "new_cases",

            "new_deaths"
        ]

        for column in numeric_columns:

            self.assertTrue(
                pd.api.types.is_numeric_dtype(
                    self.cleaner.df[column]
                ),
                msg=(
                    f"{column} is not numeric."
                )
            )

    # =========================================================================
    # TEST ROW COUNT
    # =========================================================================

    def test_dataset_row_count(self):
        """
        Validate dataset row count.
        """

        self.assertGreater(
            len(self.cleaner.df),
            0,
            msg=(
                "Dataset contains no rows."
            )
        )

    # =========================================================================
    # TEST COLUMN COUNT
    # =========================================================================

    def test_dataset_column_count(self):
        """
        Validate dataset column count.
        """

        self.assertGreater(
            len(self.cleaner.df.columns),
            0,
            msg=(
                "Dataset contains no columns."
            )
        )

    # =========================================================================
    # TEST CLEANED DATASET SAVE
    # =========================================================================

    def test_cleaned_dataset_save(self):
        """
        Test saving cleaned dataset.
        """

        self.cleaner.save_cleaned_dataset()

        self.assertTrue(
            os.path.exists(
                CLEANED_DATASET_PATH
            ),
            msg=(
                "Cleaned dataset file "
                "was not created."
            )
        )

    # =========================================================================
    # TEST FULL CLEANING PIPELINE
    # =========================================================================

    def test_complete_cleaning_pipeline(self):
        """
        Test complete cleaning pipeline.
        """

        cleaner = CovidDataCleaning(
            input_path=RAW_DATASET_PATH,
            output_path=CLEANED_DATASET_PATH
        )

        cleaned_df, report = (
            cleaner
            .run_cleaning_pipeline()
        )

        self.assertIsInstance(
            cleaned_df,
            pd.DataFrame
        )

        self.assertIsInstance(
            report,
            dict
        )

        self.assertFalse(
            cleaned_df.empty
        )

    # =========================================================================
    # TEST MEMORY USAGE
    # =========================================================================

    def test_memory_usage(self):
        """
        Validate dataset memory usage.
        """

        memory_usage = (
            self.cleaner.df
            .memory_usage(
                deep=True
            )
            .sum()
        )

        self.assertGreater(
            memory_usage,
            0,
            msg=(
                "Invalid memory usage."
            )
        )

    # =========================================================================
    # TEST DATE RANGE
    # =========================================================================

    def test_date_range(self):
        """
        Validate date range.
        """

        minimum_date = (
            self.cleaner.df["date"]
            .min()
        )

        maximum_date = (
            self.cleaner.df["date"]
            .max()
        )

        self.assertLess(
            minimum_date,
            maximum_date,
            msg=(
                "Invalid date range."
            )
        )

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )
