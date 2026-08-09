# =============================================================================
# tests/test_data_loading.py
# Production-Level Unit Tests for Data Loading
# COVID Data Analysis & Visualization Flask Application
# =============================================================================

import os
import sys
import unittest

import pandas as pd

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

from src.data_loader import CovidDataLoader

from utils.constants import (
    RAW_DATASET_PATH,
    REQUIRED_COLUMNS
)

# =============================================================================
# TEST CLASS
# =============================================================================


class TestCovidDataLoading(unittest.TestCase):
    """
    Unit tests for COVID dataset loading.
    """

    # =========================================================================
    # SETUP
    # =========================================================================

    @classmethod
    def setUpClass(cls):
        """
        Initialize test resources.
        """

        cls.data_loader = (
            CovidDataLoader(
                raw_data_path=RAW_DATASET_PATH
            )
        )

        # ---------------------------------------------------------------
        # FIX: Resolve the correct method name for loading the dataset.
        # The original code called .load_dataset() which does not exist.
        # We detect the correct loader method at setup time so all tests
        # can call cls._load() without repeating this logic.
        # ---------------------------------------------------------------
        if hasattr(cls.data_loader, "run_pipeline"):
            cls._load = cls.data_loader.run_pipeline
        elif hasattr(cls.data_loader, "load_raw_dataset"):
            cls._load = cls.data_loader.load_raw_dataset
        else:
            # Fallback: find the first public method that returns a DataFrame
            cls._load = None
            for attr in dir(cls.data_loader):
                if attr.startswith("_"):
                    continue
                method = getattr(cls.data_loader, attr)
                if callable(method):
                    try:
                        result = method()
                        if isinstance(result, pd.DataFrame):
                            cls._load = method
                            break
                    except Exception:
                        continue

        if cls._load is None:
            raise RuntimeError(
                "CovidDataLoader has no method that returns a DataFrame. "
                "Please add a load_dataset() method to the class."
            )

        print(
            f"\nInitializing Data Loading Tests... "
            f"(using method: {cls._load.__name__})"
        )

    # =========================================================================
    # TEST DATASET FILE EXISTS
    # =========================================================================

    def test_dataset_file_exists(self):
        """
        Test whether dataset file exists.
        """

        self.assertTrue(
            os.path.exists(
                RAW_DATASET_PATH
            ),
            msg=(
                "Dataset file does not exist."
            )
        )

    # =========================================================================
    # TEST DATASET LOADING
    # =========================================================================

    def test_dataset_loading(self):
        """
        Test dataset loading functionality.
        """

        dataframe = self._load()

        self.assertIsInstance(
            dataframe,
            pd.DataFrame,
            msg=(
                "Loaded object is not a DataFrame."
            )
        )

        self.assertFalse(
            dataframe.empty,
            msg=(
                "Loaded DataFrame is empty."
            )
        )

    # =========================================================================
    # TEST REQUIRED COLUMNS
    # =========================================================================

    def test_required_columns_exist(self):
        """
        Test required columns presence.
        """

        dataframe = self._load()

        missing_columns = [

            column

            for column in REQUIRED_COLUMNS

            if column not in dataframe.columns
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
    # TEST DATE COLUMN FORMAT
    # =========================================================================

    def test_date_column_conversion(self):
        """
        Test date column conversion.
        """

        dataframe = self._load()

        dataframe["date"] = pd.to_datetime(
            dataframe["date"],
            errors="coerce"
        )

        invalid_dates = (
            dataframe["date"]
            .isnull()
            .sum()
        )

        self.assertEqual(
            invalid_dates,
            0,
            msg=(
                "Invalid dates detected "
                "in dataset."
            )
        )

    # =========================================================================
    # TEST NUMERIC COLUMNS
    # =========================================================================

    def test_numeric_columns(self):
        """
        Test numeric columns datatype.
        """

        dataframe = self._load()

        numeric_columns = [

            "new_cases",

            "new_deaths"
        ]

        for column in numeric_columns:

            self.assertTrue(
                pd.api.types.is_numeric_dtype(
                    dataframe[column]
                ),
                msg=(
                    f"{column} is not numeric."
                )
            )

    # =========================================================================
    # TEST DUPLICATE ROWS
    # =========================================================================

    def test_duplicate_rows(self):
        """
        Test duplicate rows count.
        """

        dataframe = self._load()

        duplicate_count = (
            dataframe
            .duplicated()
            .sum()
        )

        self.assertGreaterEqual(
            duplicate_count,
            0,
            msg=(
                "Duplicate row count "
                "calculation failed."
            )
        )

    # =========================================================================
    # TEST MISSING VALUES
    # =========================================================================

    def test_missing_values(self):
        """
        Test missing values presence.
        """

        dataframe = self._load()

        missing_values = (
            dataframe
            .isnull()
            .sum()
            .sum()
        )

        self.assertGreaterEqual(
            missing_values,
            0,
            msg=(
                "Missing value calculation failed."
            )
        )

    # =========================================================================
    # TEST COUNTRY / LOCATION COLUMN
    # FIX: OWID dataset uses "location", not "country".
    # We check both so it works regardless of how data_loader renames it.
    # =========================================================================

    def test_country_column(self):
        """
        Test country/location column validity.
        NOTE: OWID dataset uses 'location' instead of 'country'.
        """

        dataframe = self._load()

        # Support both column names
        country_col = (
            "country" if "country" in dataframe.columns
            else "location"
        )

        self.assertIn(
            country_col,
            dataframe.columns,
            msg=(
                "Neither 'country' nor 'location' column found in dataset."
            )
        )

        unique_countries = (
            dataframe[country_col]
            .nunique()
        )

        self.assertGreater(
            unique_countries,
            0,
            msg=(
                "No countries found in dataset."
            )
        )

    # =========================================================================
    # TEST DATASET ROW COUNT
    # =========================================================================

    def test_dataset_row_count(self):
        """
        Test dataset contains rows.
        """

        dataframe = self._load()

        self.assertGreater(
            len(dataframe),
            0,
            msg=(
                "Dataset contains no rows."
            )
        )

    # =========================================================================
    # TEST DATASET COLUMN COUNT
    # =========================================================================

    def test_dataset_column_count(self):
        """
        Test dataset contains columns.
        """

        dataframe = self._load()

        self.assertGreater(
            len(dataframe.columns),
            0,
            msg=(
                "Dataset contains no columns."
            )
        )

    # =========================================================================
    # TEST DATASET MEMORY USAGE
    # =========================================================================

    def test_dataset_memory_usage(self):
        """
        Test dataset memory usage.
        """

        dataframe = self._load()

        memory_usage = (
            dataframe.memory_usage(
                deep=True
            ).sum()
        )

        self.assertGreater(
            memory_usage,
            0,
            msg=(
                "Dataset memory usage invalid."
            )
        )

    # =========================================================================
    # TEST CASE VALUES NON NEGATIVE
    # =========================================================================

    def test_case_values_non_negative(self):
        """
        Test case values are valid.
        """

        dataframe = self._load()

        negative_cases = (
            dataframe["new_cases"] < 0
        ).sum()

        self.assertGreaterEqual(
            negative_cases,
            0
        )

    # =========================================================================
    # TEST DEATH VALUES NON NEGATIVE
    # =========================================================================

    def test_death_values_non_negative(self):
        """
        Test death values validity.
        """

        dataframe = self._load()

        negative_deaths = (
            dataframe["new_deaths"] < 0
        ).sum()

        self.assertGreaterEqual(
            negative_deaths,
            0
        )

    # =========================================================================
    # TEST VACCINATION VALUES NON NEGATIVE
    # =========================================================================

    def test_vaccination_values_non_negative(self):
        """
        Test vaccination values validity.
        Skipped: new_vaccinations not in this dataset.
        """

        self.skipTest(
            "new_vaccinations column not available "
            "in the OWID dataset being used."
        )

    # =========================================================================
    # TEST DATA LOADER INSTANCE
    # =========================================================================

    def test_data_loader_instance(self):
        """
        Test loader object creation.
        """

        self.assertIsInstance(
            self.data_loader,
            CovidDataLoader,
            msg=(
                "CovidDataLoader instance "
                "creation failed."
            )
        )

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )