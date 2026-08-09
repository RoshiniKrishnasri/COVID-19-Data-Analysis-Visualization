# =============================================================================
# src/analysis.py
# Production-Level COVID Analysis Module
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

FEATURED_DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "featured_covid_data.csv"
)

# =============================================================================
# ANALYSIS CLASS
# =============================================================================


class CovidAnalysis:
    """
    Production-level COVID analysis engine
    for Flask analytics dashboard.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(
        self,
        dataset_path=FEATURED_DATASET_PATH
    ):

        self.dataset_path = dataset_path

        self.df = pd.DataFrame()

        logger.info(
            "CovidAnalysis Initialized"
        )

    # =========================================================================
    # LOAD DATASET
    # =========================================================================

    def load_dataset(self):
        """
        Load feature-engineered dataset.
        """

        try:

            if not os.path.exists(
                self.dataset_path
            ):

                raise FileNotFoundError(
                    f"Dataset not found: "
                    f"{self.dataset_path}"
                )

            logger.info(
                f"Loading Dataset: "
                f"{self.dataset_path}"
            )

            self.df = pd.read_csv(
                self.dataset_path
            )

            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
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
    # GLOBAL SUMMARY ANALYSIS
    # =========================================================================

    def global_summary_analysis(self):
        """
        Generate global COVID summary.
        """

        try:

            logger.info(
                "Generating Global Summary"
            )

            latest_date = (
                self.df["date"].max()
            )

            latest_df = self.df[
                self.df["date"] == latest_date
            ]

            summary = {
                "latest_date": str(
                    latest_date.date()
                ),

                "total_cases": int(
                    latest_df[
                        "new_cases"
                    ].sum()
                ),

                "total_deaths": int(
                    latest_df[
                        "new_deaths"
                    ].sum()
                ),

                "countries_affected": int(
                    latest_df[
                        "country"
                    ].nunique()
                )
            }

            logger.info(
                "Global Summary Generated"
            )

            return summary

        except Exception as error:

            logger.error(
                f"Global Summary Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # GLOBAL TREND ANALYSIS
    # =========================================================================

    def global_trend_analysis(self):
        """
        Generate global trend analysis.
        """

        try:

            logger.info(
                "Generating Global Trend Analysis"
            )

            trend_df = (
                self.df.groupby("date")[
                    [
                        "new_cases",
                        "new_deaths"
                    ]
                ]
                .sum()
                .reset_index()
            )

            logger.info(
                "Global Trend Analysis Completed"
            )

            return trend_df

        except Exception as error:

            logger.error(
                f"Trend Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # COUNTRY ANALYSIS
    # =========================================================================

    def country_analysis(
        self,
        country_name
    ):
        """
        Generate country-specific analysis.
        """

        try:

            logger.info(
                f"Generating Analysis for: "
                f"{country_name}"
            )

            country_df = self.df[
                self.df["country"]
                .str.lower()
                ==
                country_name.lower()
            ]

            if country_df.empty:

                raise ValueError(
                    f"No data available for "
                    f"{country_name}"
                )

            analysis = {
                "country": country_name,

                "total_cases": int(
                    country_df[
                        "new_cases"
                    ].sum()
                ),

                "total_deaths": int(
                    country_df[
                        "new_deaths"
                    ].sum()
                ),

                "peak_cases": int(
                    country_df[
                        "new_cases"
                    ].max()
                ),

                "peak_deaths": int(
                    country_df[
                        "new_deaths"
                    ].max()
                ),

                "mortality_rate": round(
                    (
                        country_df[
                            "new_deaths"
                        ].sum()
                        /
                        max(
                            country_df[
                                "new_cases"
                            ].sum(),
                            1
                        )
                    ) * 100,
                    2
                )
            }

            logger.info(
                f"{country_name} Analysis Completed"
            )

            return analysis

        except Exception as error:

            logger.error(
                f"Country Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # TOP HOTSPOTS ANALYSIS
    # =========================================================================

    def hotspot_analysis(self):
        """
        Identify COVID hotspots.
        """

        try:

            logger.info(
                "Generating Hotspot Analysis"
            )

            latest_date = (
                self.df["date"].max()
            )

            latest_df = self.df[
                self.df["date"] == latest_date
            ]

            hotspot_df = (
                latest_df.sort_values(
                    by="new_cases",
                    ascending=False
                )
                .head(10)
            )

            hotspot_data = hotspot_df[
                [
                    "country",
                    "new_cases",
                    "new_deaths"
                ]
            ]

            logger.info(
                "Hotspot Analysis Completed"
            )

            return hotspot_data

        except Exception as error:

            logger.error(
                f"Hotspot Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # MORTALITY RATE ANALYSIS
    # =========================================================================

    def mortality_rate_analysis(self):
        """
        Analyze mortality rate by country.
        """

        try:

            logger.info(
                "Generating Mortality Analysis"
            )

            mortality_df = (
                self.df.groupby("country")[
                    [
                        "new_cases",
                        "new_deaths"
                    ]
                ]
                .sum()
                .reset_index()
            )

            mortality_df[
                "mortality_rate"
            ] = np.where(
                mortality_df[
                    "new_cases"
                ] > 0,

                (
                    mortality_df[
                        "new_deaths"
                    ]
                    /
                    mortality_df[
                        "new_cases"
                    ]
                ) * 100,

                0
            )

            top_mortality = (
                mortality_df.sort_values(
                    by="mortality_rate",
                    ascending=False
                )
                .head(10)
            )

            logger.info(
                "Mortality Analysis Completed"
            )

            return top_mortality

        except Exception as error:

            logger.error(
                f"Mortality Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # VACCINATION ANALYSIS
    # =========================================================================

    def vaccination_analysis(self):
        """
        Analyze vaccination progress.
        Note: vaccination columns not available in this dataset.
        """

        logger.info(
            "Vaccination Analysis: Not available in this dataset"
        )

        return pd.DataFrame(
            columns=["country"]
        )

    # =========================================================================
    # SEVERITY ANALYSIS
    # =========================================================================

    def severity_analysis(self):
        """
        Analyze severity distribution.
        """

        try:

            logger.info(
                "Generating Severity Analysis"
            )

            severity_counts = (
                self.df[
                    "severity_level"
                ]
                .value_counts()
                .to_dict()
            )

            logger.info(
                "Severity Analysis Completed"
            )

            return severity_counts

        except Exception as error:

            logger.error(
                f"Severity Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # ROLLING AVERAGE ANALYSIS
    # =========================================================================

    def rolling_average_analysis(self):
        """
        Analyze rolling case averages.
        """

        try:

            logger.info(
                "Generating Rolling Average Analysis"
            )

            rolling_df = (
                self.df.groupby("date")[
                    "rolling_avg_cases"
                ]
                .mean()
                .reset_index()
            )

            logger.info(
                "Rolling Average Analysis Completed"
            )

            return rolling_df

        except Exception as error:

            logger.error(
                f"Rolling Average Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # MONTHLY ANALYSIS
    # =========================================================================

    def monthly_analysis(self):
        """
        Generate monthly COVID statistics.
        """

        try:

            logger.info(
                "Generating Monthly Analysis"
            )

            monthly_df = (
                self.df.groupby(
                    [
                        "year",
                        "month"
                    ]
                )[
                    [
                        "new_cases",
                        "new_deaths"
                    ]
                ]
                .sum()
                .reset_index()
            )

            logger.info(
                "Monthly Analysis Completed"
            )

            return monthly_df

        except Exception as error:

            logger.error(
                f"Monthly Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # WEEKDAY ANALYSIS
    # =========================================================================

    def weekday_analysis(self):
        """
        Analyze weekday patterns.
        """

        try:

            logger.info(
                "Generating Weekday Analysis"
            )

            weekday_df = (
                self.df.groupby("weekday")[
                    [
                        "new_cases",
                        "new_deaths"
                    ]
                ]
                .mean()
                .reset_index()
            )

            logger.info(
                "Weekday Analysis Completed"
            )

            return weekday_df

        except Exception as error:

            logger.error(
                f"Weekday Analysis Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # COUNTRY COMPARISON ANALYSIS
    # =========================================================================

    def compare_countries(
        self,
        countries_list
    ):
        """
        Compare multiple countries.
        """

        try:

            logger.info(
                "Generating Country Comparison"
            )

            comparison_df = self.df[
                self.df["country"]
                .isin(countries_list)
            ]

            comparison_result = (
                comparison_df.groupby(
                    "country"
                )[
                    [
                        "new_cases",
                        "new_deaths"
                    ]
                ]
                .sum()
                .reset_index()
            )

            logger.info(
                "Country Comparison Completed"
            )

            return comparison_result

        except Exception as error:

            logger.error(
                f"Country Comparison Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # DATASET STATISTICS
    # =========================================================================

    def dataset_statistics(self):
        """
        Generate overall dataset statistics.
        """

        try:

            logger.info(
                "Generating Dataset Statistics"
            )

            statistics = {
                "rows": int(
                    self.df.shape[0]
                ),

                "columns": int(
                    self.df.shape[1]
                ),

                "countries": int(
                    self.df[
                        "country"
                    ].nunique()
                ),

                "start_date": str(
                    self.df[
                        "date"
                    ].min()
                ),

                "end_date": str(
                    self.df[
                        "date"
                    ].max()
                ),

                "missing_values": int(
                    self.df
                    .isnull()
                    .sum()
                    .sum()
                )
            }

            logger.info(
                "Dataset Statistics Generated"
            )

            return statistics

        except Exception as error:

            logger.error(
                f"Dataset Statistics Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # COMPLETE ANALYSIS PIPELINE
    # =========================================================================

    def run_analysis_pipeline(self):
        """
        Execute complete analysis pipeline.
        """

        try:

            logger.info(
                "COVID Analysis Pipeline Started"
            )

            self.load_dataset()

            results = {

                "global_summary":
                self.global_summary_analysis(),

                "global_trend":
                self.global_trend_analysis(),

                "hotspots":
                self.hotspot_analysis(),

                "mortality_analysis":
                self.mortality_rate_analysis(),


                "severity_analysis":
                self.severity_analysis(),

                "rolling_average":
                self.rolling_average_analysis(),

                "monthly_analysis":
                self.monthly_analysis(),

                "weekday_analysis":
                self.weekday_analysis(),

                "dataset_statistics":
                self.dataset_statistics()
            }

            logger.info(
                "COVID Analysis Pipeline Completed"
            )

            return results

        except Exception as error:

            logger.error(
                f"Analysis Pipeline Failed: "
                f"{error}"
            )

            raise

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    analyzer = CovidAnalysis()

    analysis_results = (
        analyzer.run_analysis_pipeline()
    )

    print("\nCOVID Analysis Completed")

    print("\nGlobal Summary:")
    print(
        analysis_results[
            "global_summary"
        ]
    )

    print("\nDataset Statistics:")
    print(
        analysis_results[
            "dataset_statistics"
        ]
    )

    print("\nSeverity Analysis:")
    print(
        analysis_results[
            "severity_analysis"
        ]
    )

    print("\nTop Hotspots:")
    print(
        analysis_results[
            "hotspots"
        ].head()
    )