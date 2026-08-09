# =============================================================================
# utils/helpers.py
# Production-Level Helper Utility Functions
# COVID Data Analysis & Visualization Flask Application
# =============================================================================

import os
import json
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
# BASE DIRECTORY
# =============================================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def create_directory(directory_path):
    """
    Create directory if it does not exist.
    """

    try:

        os.makedirs(
            directory_path,
            exist_ok=True
        )

        logger.info(
            f"Directory Ready: "
            f"{directory_path}"
        )

    except Exception as error:

        logger.error(
            f"Directory Creation Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# DATASET VALIDATION
# =============================================================================


def validate_dataset_columns(
    dataframe,
    required_columns
):
    """
    Validate required dataset columns.
    """

    try:

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:

            logger.warning(
                f"Missing Columns: "
                f"{missing_columns}"
            )

            return False

        logger.info(
            "Dataset Validation Successful"
        )

        return True

    except Exception as error:

        logger.error(
            f"Dataset Validation Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# LOAD CSV DATASET
# =============================================================================


def load_csv_dataset(file_path):
    """
    Load CSV dataset safely.
    """

    try:

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"Dataset not found: "
                f"{file_path}"
            )

        logger.info(
            f"Loading Dataset: "
            f"{file_path}"
        )

        dataframe = pd.read_csv(
            file_path
        )

        logger.info(
            f"Dataset Loaded Successfully | "
            f"Shape: {dataframe.shape}"
        )

        return dataframe

    except Exception as error:

        logger.error(
            f"CSV Loading Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# SAVE DATAFRAME TO CSV
# =============================================================================


def save_dataframe_to_csv(
    dataframe,
    output_path
):
    """
    Save dataframe as CSV.
    """

    try:

        output_directory = os.path.dirname(
            output_path
        )

        create_directory(
            output_directory
        )

        dataframe.to_csv(
            output_path,
            index=False
        )

        logger.info(
            f"Dataset Saved: "
            f"{output_path}"
        )

    except Exception as error:

        logger.error(
            f"Saving CSV Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# CONVERT DATE COLUMN
# =============================================================================


def convert_date_column(
    dataframe,
    column_name="date"
):
    """
    Convert date column to datetime.
    """

    try:

        if column_name in dataframe.columns:

            dataframe[column_name] = (
                pd.to_datetime(
                    dataframe[column_name],
                    errors="coerce"
                )
            )

            logger.info(
                f"Converted Date Column: "
                f"{column_name}"
            )

        return dataframe

    except Exception as error:

        logger.error(
            f"Date Conversion Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# REMOVE DUPLICATE RECORDS
# =============================================================================


def remove_duplicates(dataframe):
    """
    Remove duplicate rows.
    """

    try:

        initial_rows = len(dataframe)

        dataframe = dataframe.drop_duplicates()

        final_rows = len(dataframe)

        logger.info(
            f"Duplicates Removed: "
            f"{initial_rows - final_rows}"
        )

        return dataframe

    except Exception as error:

        logger.error(
            f"Duplicate Removal Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# HANDLE MISSING VALUES
# =============================================================================


def handle_missing_values(
    dataframe,
    fill_value=0
):
    """
    Fill missing values safely.
    """

    try:

        missing_before = (
            dataframe
            .isnull()
            .sum()
            .sum()
        )

        dataframe.fillna(
            fill_value,
            inplace=True
        )

        missing_after = (
            dataframe
            .isnull()
            .sum()
            .sum()
        )

        logger.info(
            f"Missing Values Filled | "
            f"Before: {missing_before} | "
            f"After: {missing_after}"
        )

        return dataframe

    except Exception as error:

        logger.error(
            f"Missing Value Handling Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# LOWERCASE COLUMN NAMES
# =============================================================================


def standardize_column_names(dataframe):
    """
    Convert column names to lowercase.
    """

    try:

        dataframe.columns = [
            column.lower().strip()
            for column in dataframe.columns
        ]

        logger.info(
            "Column Names Standardized"
        )

        return dataframe

    except Exception as error:

        logger.error(
            f"Column Standardization Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# FORMAT LARGE NUMBERS
# =============================================================================


def format_large_number(value):
    """
    Format large numeric values.
    """

    try:

        if value >= 1_000_000_000:

            return (
                f"{value / 1_000_000_000:.2f}B"
            )

        if value >= 1_000_000:

            return (
                f"{value / 1_000_000:.2f}M"
            )

        if value >= 1_000:

            return (
                f"{value / 1_000:.2f}K"
            )

        return str(value)

    except Exception as error:

        logger.error(
            f"Number Formatting Failed: "
            f"{error}"
        )

        return str(value)


# =============================================================================
# GENERATE DATASET SUMMARY
# =============================================================================


def generate_dataset_summary(dataframe):
    """
    Generate dataset summary statistics.
    """

    try:

        summary = {

            "rows":
            int(dataframe.shape[0]),

            "columns":
            int(dataframe.shape[1]),

            "missing_values":
            int(
                dataframe
                .isnull()
                .sum()
                .sum()
            ),

            "duplicate_rows":
            int(
                dataframe
                .duplicated()
                .sum()
            ),

            "memory_usage_mb":
            round(
                dataframe.memory_usage(
                    deep=True
                ).sum() / (1024 ** 2),
                2
            )
        }

        logger.info(
            "Dataset Summary Generated"
        )

        return summary

    except Exception as error:

        logger.error(
            f"Dataset Summary Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# FILTER COUNTRY DATA
# =============================================================================


def filter_country_data(
    dataframe,
    country_name
):
    """
    Filter data for a specific country.
    """

    try:

        filtered_df = dataframe[
            dataframe["country"]
            .str.lower()
            ==
            country_name.lower()
        ]

        logger.info(
            f"Country Data Filtered: "
            f"{country_name}"
        )

        return filtered_df

    except Exception as error:

        logger.error(
            f"Country Filter Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# GET TOP COUNTRIES BY CASES
# =============================================================================


def get_top_countries_by_cases(
    dataframe,
    top_n=10
):
    """
    Get top countries by total cases.
    """

    try:

        top_countries = (
            dataframe.groupby("country")[
                "new_cases"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(top_n)
            .reset_index()
        )

        logger.info(
            "Top Countries Retrieved"
        )

        return top_countries

    except Exception as error:

        logger.error(
            f"Top Countries Analysis Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# CALCULATE MORTALITY RATE
# =============================================================================


def calculate_mortality_rate(
    total_cases,
    total_deaths
):
    """
    Calculate mortality rate safely.
    """

    try:

        if total_cases <= 0:

            return 0

        mortality_rate = (
            total_deaths / total_cases
        ) * 100

        return round(
            mortality_rate,
            2
        )

    except Exception as error:

        logger.error(
            f"Mortality Calculation Failed: "
            f"{error}"
        )

        return 0


# =============================================================================
# EXPORT JSON FILE
# =============================================================================


def export_json(
    data,
    output_path
):
    """
    Export data as JSON file.
    """

    try:

        output_directory = os.path.dirname(
            output_path
        )

        create_directory(
            output_directory
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as json_file:

            json.dump(
                data,
                json_file,
                indent=4,
                default=str
            )

        logger.info(
            f"JSON Exported: "
            f"{output_path}"
        )

    except Exception as error:

        logger.error(
            f"JSON Export Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# GENERATE TIMESTAMP
# =============================================================================


def generate_timestamp():
    """
    Generate formatted timestamp.
    """

    return datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =============================================================================
# CHECK DATAFRAME EMPTY
# =============================================================================


def is_dataframe_empty(dataframe):
    """
    Check if dataframe is empty.
    """

    try:

        return dataframe.empty

    except Exception as error:

        logger.error(
            f"DataFrame Empty Check Failed: "
            f"{error}"
        )

        return True


# =============================================================================
# CONVERT DATAFRAME TO API RESPONSE
# =============================================================================


def dataframe_to_api_response(
    dataframe
):
    """
    Convert dataframe to API-friendly JSON.
    """

    try:

        response = dataframe.to_dict(
            orient="records"
        )

        logger.info(
            "DataFrame Converted to API Response"
        )

        return response

    except Exception as error:

        logger.error(
            f"API Response Conversion Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# CREATE ANALYSIS REPORT
# =============================================================================


def create_analysis_report(
    summary_data,
    output_path
):
    """
    Create text-based analysis report.
    """

    try:

        output_directory = os.path.dirname(
            output_path
        )

        create_directory(
            output_directory
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as report_file:

            report_file.write(
                "COVID-19 Analysis Report\n"
            )

            report_file.write(
                "=" * 50 + "\n\n"
            )

            for key, value in (
                summary_data.items()
            ):

                report_file.write(
                    f"{key}: {value}\n"
                )

        logger.info(
            f"Analysis Report Created: "
            f"{output_path}"
        )

    except Exception as error:

        logger.error(
            f"Report Generation Failed: "
            f"{error}"
        )

        raise


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    print(
        "\nCOVID Helper Utilities Module Loaded Successfully"
    )

    print(
        "\nTimestamp:"
    )

    print(
        generate_timestamp()
    )

    print(
        "\nFormatted Number Examples:"
    )

    print(
        format_large_number(1500)
    )

    print(
        format_large_number(2500000)
    )

    print(
        format_large_number(7200000000)
    )

    print(
        "\nMortality Rate Example:"
    )

    print(
        calculate_mortality_rate(
            total_cases=100000,
            total_deaths=2500
        )
    )