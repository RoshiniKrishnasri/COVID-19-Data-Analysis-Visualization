# =============================================================================
# src/feature_engineering.py
# Production-Level COVID Feature Engineering Module
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
# BASE DIRECTORY
# =============================================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# =============================================================================
# DATASET PATHS
# =============================================================================

INPUT_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_covid_data.csv"
)

FEATURE_ENGINEERED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "featured_covid_data.csv"
)

# =============================================================================
# FEATURE ENGINEERING CLASS
# =============================================================================


class CovidFeatureEngineering:
    """
    Production-level feature engineering
    pipeline for COVID analytics.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(
        self,
        input_path=INPUT_DATA_PATH,
        output_path=FEATURE_ENGINEERED_DATA_PATH
    ):

        self.input_path = input_path

        self.output_path = output_path

        self.df = pd.DataFrame()

        logger.info(
            "CovidFeatureEngineering Initialized"
        )

    # =========================================================================
    # LOAD CLEANED DATASET
    # =========================================================================

    def load_dataset(self):
        """
        Load cleaned COVID dataset.
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
    # PREPARE DATE COLUMN
    # =========================================================================

    def prepare_date_column(self):
        """
        Convert date column to datetime.
        """

        try:

            logger.info(
                "Preparing Date Column"
            )

            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
            )

            logger.info(
                "Date Preparation Completed"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Date Preparation Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE CUMULATIVE CASES FEATURE
    # =========================================================================

    def create_total_cases_feature(self):
        """
        Generate cumulative cases feature.
        """

        try:

            logger.info(
                "Creating Total Cases Feature"
            )

            self.df["total_cases_country"] = (
                self.df.groupby("country")[
                    "new_cases"
                ].cumsum()
            )

            logger.info(
                "Total Cases Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Total Cases Feature Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE CUMULATIVE DEATHS FEATURE
    # =========================================================================

    def create_total_deaths_feature(self):
        """
        Generate cumulative deaths feature.
        """

        try:

            logger.info(
                "Creating Total Deaths Feature"
            )

            self.df["total_deaths_country"] = (
                self.df.groupby("country")[
                    "new_deaths"
                ].cumsum()
            )

            logger.info(
                "Total Deaths Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Total Deaths Feature Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE CUMULATIVE VACCINATION FEATURE
    # =========================================================================

    def create_total_vaccination_feature(self):
        """
        Vaccination feature skipped:
        new_vaccinations not in this dataset.
        """

        logger.info(
            "Vaccination Feature Skipped: "
            "Column not available in dataset"
        )

        return self.df

    # =========================================================================
    # CREATE MORTALITY RATE FEATURE
    # =========================================================================

    def create_mortality_rate_feature(self):
        """
        Generate mortality rate feature.
        """

        try:

            logger.info(
                "Creating Mortality Rate Feature"
            )

            self.df["mortality_rate"] = np.where(
                self.df["total_cases_country"] > 0,
                (
                    self.df[
                        "total_deaths_country"
                    ]
                    /
                    self.df[
                        "total_cases_country"
                    ]
                ) * 100,
                0
            )

            logger.info(
                "Mortality Rate Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Mortality Feature Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE DAILY GROWTH RATE FEATURE
    # =========================================================================

    def create_growth_rate_feature(self):
        """
        Generate daily growth rate feature.
        """

        try:

            logger.info(
                "Creating Growth Rate Feature"
            )

            self.df["daily_growth_rate"] = (
                self.df.groupby("country")[
                    "new_cases"
                ]
                .pct_change()
                .fillna(0)
            ) * 100

            logger.info(
                "Growth Rate Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Growth Rate Feature Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE ROLLING AVERAGE FEATURE
    # =========================================================================

    def create_rolling_average_feature(self):
        """
        Generate rolling average feature.
        """

        try:

            logger.info(
                "Creating Rolling Average Feature"
            )

            self.df["rolling_avg_cases"] = (
                self.df.groupby("country")[
                    "new_cases"
                ]
                .transform(
                    lambda values:
                    values.rolling(
                        window=7,
                        min_periods=1
                    ).mean()
                )
            )

            logger.info(
                "Rolling Average Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Rolling Average Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE DEATH ROLLING AVERAGE FEATURE
    # =========================================================================

    def create_death_rolling_average(self):
        """
        Generate rolling death average.
        """

        try:

            logger.info(
                "Creating Death Rolling Average"
            )

            self.df["rolling_avg_deaths"] = (
                self.df.groupby("country")[
                    "new_deaths"
                ]
                .transform(
                    lambda values:
                    values.rolling(
                        window=7,
                        min_periods=1
                    ).mean()
                )
            )

            logger.info(
                "Death Rolling Average Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Death Rolling Average Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE VACCINATION ROLLING AVERAGE
    # =========================================================================

    def create_vaccination_rolling_average(self):
        """
        Vaccination rolling average skipped:
        new_vaccinations not in this dataset.
        """

        logger.info(
            "Vaccination Rolling Average Skipped: "
            "Column not available in dataset"
        )

        return self.df

    # =========================================================================
    # CREATE PANDEMIC SEVERITY FEATURE
    # =========================================================================

    def create_severity_feature(self):
        """
        Generate pandemic severity label.
        """

        try:

            logger.info(
                "Creating Severity Feature"
            )

            conditions = [
                self.df["new_cases"] < 1000,

                (
                    (self.df["new_cases"] >= 1000)
                    &
                    (self.df["new_cases"] < 10000)
                ),

                self.df["new_cases"] >= 10000
            ]

            severity_levels = [
                "Low",
                "Medium",
                "High"
            ]

            self.df["severity_level"] = np.select(
                conditions,
                severity_levels,
                default="Low"
            )

            logger.info(
                "Severity Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Severity Feature Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE TIME FEATURES
    # =========================================================================

    def create_time_features(self):
        """
        Generate time-based features.
        """

        try:

            logger.info(
                "Creating Time Features"
            )

            self.df["year"] = (
                self.df["date"].dt.year
            )

            self.df["month"] = (
                self.df["date"].dt.month
            )

            self.df["day"] = (
                self.df["date"].dt.day
            )

            self.df["weekday"] = (
                self.df["date"].dt.day_name()
            )

            self.df["quarter"] = (
                self.df["date"].dt.quarter
            )

            logger.info(
                "Time Features Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Time Features Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # CREATE HOTSPOT FEATURE
    # =========================================================================

    def create_hotspot_feature(self):
        """
        Generate hotspot classification.
        """

        try:

            logger.info(
                "Creating Hotspot Feature"
            )

            threshold = (
                self.df["new_cases"]
                .quantile(0.90)
            )

            self.df["is_hotspot"] = np.where(
                self.df["new_cases"] >= threshold,
                1,
                0
            )

            logger.info(
                "Hotspot Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Hotspot Feature Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # SORT FINAL DATASET
    # =========================================================================

    def sort_dataset(self):
        """
        Sort dataset chronologically.
        """

        try:

            logger.info(
                "Sorting Final Dataset"
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
                f"Sorting Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # SAVE FEATURED DATASET
    # =========================================================================

    def save_feature_engineered_dataset(self):
        """
        Save feature-engineered dataset.
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
                f"Feature Engineered Dataset Saved: "
                f"{self.output_path}"
            )

        except Exception as error:

            logger.error(
                f"Saving Dataset Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # FEATURE SUMMARY REPORT
    # =========================================================================

    def generate_feature_report(self):
        """
        Generate engineered feature summary.
        """

        try:

            logger.info(
                "Generating Feature Report"
            )

            report = {
                "total_rows": len(self.df),
                "total_columns": len(
                    self.df.columns
                ),
                "feature_columns": (
                    self.df.columns.tolist()
                ),
                "hotspot_records": int(
                    self.df["is_hotspot"].sum()
                ),
                "countries": int(
                    self.df["country"].nunique()
                ),
            }

            logger.info(
                "Feature Report Generated"
            )

            return report

        except Exception as error:

            logger.error(
                f"Feature Report Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # COMPLETE FEATURE ENGINEERING PIPELINE
    # =========================================================================

    def run_feature_engineering_pipeline(self):
        """
        Execute complete feature pipeline.
        """

        try:

            logger.info(
                "COVID Feature Engineering Started"
            )

            self.load_dataset()

            self.prepare_date_column()

            self.create_total_cases_feature()

            self.create_total_deaths_feature()

            self.create_total_vaccination_feature()

            self.create_mortality_rate_feature()

            self.create_growth_rate_feature()

            self.create_rolling_average_feature()

            self.create_death_rolling_average()

            self.create_vaccination_rolling_average()

            self.create_severity_feature()

            self.create_time_features()

            self.create_hotspot_feature()

            self.sort_dataset()

            report = (
                self.generate_feature_report()
            )

            self.save_feature_engineered_dataset()

            logger.info(
                "COVID Feature Engineering Completed"
            )

            return self.df, report

        except Exception as error:

            logger.error(
                f"Feature Pipeline Failed: "
                f"{error}"
            )

            raise

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    feature_engineer = (
        CovidFeatureEngineering()
    )

    featured_df, feature_report = (
        feature_engineer
        .run_feature_engineering_pipeline()
    )

    print("\nCOVID Feature Engineering Completed")

    print("\nDataset Shape:")
    print(featured_df.shape)

    print("\nFeature Columns:")
    print(featured_df.columns.tolist())

    print("\nFeature Report:")
    print(feature_report)

    print("\nFirst 5 Rows:")
    print(featured_df.head())