# =============================================================================
# src/visualization.py
# Production-Level COVID Visualization Module
# =============================================================================

import os
import logging

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

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
# DATASET PATHS
# =============================================================================

FEATURED_DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "featured_covid_data.csv"
)

# =============================================================================
# VISUALIZATION OUTPUT DIRECTORY
# =============================================================================

VISUALIZATION_OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "static",
    "images",
    "visualizations"
)

os.makedirs(
    VISUALIZATION_OUTPUT_DIR,
    exist_ok=True
)

# =============================================================================
# MATPLOTLIB CONFIGURATION
# =============================================================================

plt.rcParams["figure.figsize"] = (14, 7)

plt.rcParams["font.size"] = 12

# =============================================================================
# COVID VISUALIZATION CLASS
# =============================================================================


class CovidVisualization:
    """
    Production-level COVID visualization
    generation module.
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
            "CovidVisualization Initialized"
        )

    # =========================================================================
    # LOAD FEATURE ENGINEERED DATASET
    # =========================================================================

    def load_dataset(self):
        """
        Load feature engineered dataset.
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
    # GLOBAL CASE TREND VISUALIZATION
    # =========================================================================

    def generate_global_cases_trend(self):
        """
        Generate global cases trend chart.
        """

        try:

            logger.info(
                "Generating Global Cases Trend"
            )

            trend_df = (
                self.df.groupby("date")[
                    "new_cases"
                ]
                .sum()
                .reset_index()
            )

            plt.figure()

            plt.plot(
                trend_df["date"],
                trend_df["new_cases"]
            )

            plt.title(
                "Global COVID-19 Cases Trend"
            )

            plt.xlabel("Date")

            plt.ylabel("New Cases")

            plt.xticks(rotation=45)

            plt.tight_layout()

            output_path = os.path.join(
                VISUALIZATION_OUTPUT_DIR,
                "global_cases_trend.png"
            )

            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

            plt.close()

            logger.info(
                "Global Cases Trend Saved"
            )

            return output_path

        except Exception as error:

            logger.error(
                f"Cases Trend Visualization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # GLOBAL DEATH TREND VISUALIZATION
    # =========================================================================

    def generate_global_deaths_trend(self):
        """
        Generate global deaths trend chart.
        """

        try:

            logger.info(
                "Generating Global Death Trend"
            )

            death_df = (
                self.df.groupby("date")[
                    "new_deaths"
                ]
                .sum()
                .reset_index()
            )

            plt.figure()

            plt.plot(
                death_df["date"],
                death_df["new_deaths"]
            )

            plt.title(
                "Global COVID-19 Death Trend"
            )

            plt.xlabel("Date")

            plt.ylabel("Deaths")

            plt.xticks(rotation=45)

            plt.tight_layout()

            output_path = os.path.join(
                VISUALIZATION_OUTPUT_DIR,
                "global_deaths_trend.png"
            )

            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

            plt.close()

            logger.info(
                "Global Death Trend Saved"
            )

            return output_path

        except Exception as error:

            logger.error(
                f"Death Trend Visualization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # GLOBAL VACCINATION TREND
    # =========================================================================

    def generate_global_vaccination_trend(self):
        """
        Vaccination trend skipped:
        new_vaccinations column not available in this dataset.
        """

        logger.info(
            "Vaccination Trend Skipped: "
            "Column not available in dataset"
        )

        return None

    # =========================================================================
    # TOP COUNTRIES BY CASES
    # =========================================================================

    def generate_top_cases_countries_chart(self):
        """
        Generate top countries by cases chart.
        """

        try:

            logger.info(
                "Generating Top Countries Chart"
            )

            top_cases = (
                self.df.groupby("country")[
                    "new_cases"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(10)
            )

            plt.figure()

            top_cases.plot(
                kind="bar"
            )

            plt.title(
                "Top 10 Countries by Cases"
            )

            plt.xlabel("Country")

            plt.ylabel("Cases")

            plt.xticks(rotation=45)

            plt.tight_layout()

            output_path = os.path.join(
                VISUALIZATION_OUTPUT_DIR,
                "top_countries_cases.png"
            )

            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

            plt.close()

            logger.info(
                "Top Countries Chart Saved"
            )

            return output_path

        except Exception as error:

            logger.error(
                f"Top Countries Visualization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # HOTSPOT VISUALIZATION
    # =========================================================================

    def generate_hotspot_visualization(self):
        """
        Generate hotspot countries visualization.
        """

        try:

            logger.info(
                "Generating Hotspot Visualization"
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

            plt.figure()

            plt.bar(
                hotspot_df["country"],
                hotspot_df["new_cases"]
            )

            plt.title(
                "Top COVID-19 Hotspots"
            )

            plt.xlabel("Country")

            plt.ylabel("Cases")

            plt.xticks(rotation=45)

            plt.tight_layout()

            output_path = os.path.join(
                VISUALIZATION_OUTPUT_DIR,
                "covid_hotspots.png"
            )

            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

            plt.close()

            logger.info(
                "Hotspot Visualization Saved"
            )

            return output_path

        except Exception as error:

            logger.error(
                f"Hotspot Visualization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # INDIA CASE TREND
    # =========================================================================

    def generate_india_trend(self):
        """
        Generate India COVID trend chart.
        """

        try:

            logger.info(
                "Generating India Trend"
            )

            india_df = self.df[
                self.df["country"] == "India"
            ]

            plt.figure()

            plt.plot(
                india_df["date"],
                india_df["new_cases"]
            )

            plt.title(
                "India COVID-19 Trend"
            )

            plt.xlabel("Date")

            plt.ylabel("Cases")

            plt.xticks(rotation=45)

            plt.tight_layout()

            output_path = os.path.join(
                VISUALIZATION_OUTPUT_DIR,
                "india_cases_trend.png"
            )

            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

            plt.close()

            logger.info(
                "India Trend Saved"
            )

            return output_path

        except Exception as error:

            logger.error(
                f"India Trend Visualization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # MORTALITY RATE VISUALIZATION
    # =========================================================================

    def generate_mortality_rate_chart(self):
        """
        Generate mortality rate chart.
        """

        try:

            logger.info(
                "Generating Mortality Chart"
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
                mortality_df["new_cases"] > 0,
                (
                    mortality_df["new_deaths"]
                    /
                    mortality_df["new_cases"]
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

            plt.figure()

            plt.bar(
                top_mortality["country"],
                top_mortality[
                    "mortality_rate"
                ]
            )

            plt.title(
                "Top Mortality Rate Countries"
            )

            plt.xlabel("Country")

            plt.ylabel(
                "Mortality Rate (%)"
            )

            plt.xticks(rotation=45)

            plt.tight_layout()

            output_path = os.path.join(
                VISUALIZATION_OUTPUT_DIR,
                "mortality_rate_chart.png"
            )

            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

            plt.close()

            logger.info(
                "Mortality Chart Saved"
            )

            return output_path

        except Exception as error:

            logger.error(
                f"Mortality Visualization Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # GENERATE DASHBOARD SUMMARY
    # =========================================================================

    def generate_dashboard_summary(self):
        """
        Generate dashboard summary metrics.
        """

        try:

            logger.info(
                "Generating Dashboard Summary"
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

                "countries": int(
                    latest_df[
                        "country"
                    ].nunique()
                )
            }

            logger.info(
                "Dashboard Summary Generated"
            )

            return summary

        except Exception as error:

            logger.error(
                f"Dashboard Summary Failed: "
                f"{error}"
            )

            raise

    # =========================================================================
    # RUN COMPLETE VISUALIZATION PIPELINE
    # =========================================================================

    def run_visualization_pipeline(self):
        """
        Execute complete visualization pipeline.
        """

        try:

            logger.info(
                "Visualization Pipeline Started"
            )

            self.load_dataset()

            visualizations = {
                "cases_trend":
                self.generate_global_cases_trend(),

                "deaths_trend":
                self.generate_global_deaths_trend(),

                "top_cases_chart":
                self.generate_top_cases_countries_chart(),

                "hotspot_chart":
                self.generate_hotspot_visualization(),

                "india_trend":
                self.generate_india_trend(),

                "mortality_chart":
                self.generate_mortality_rate_chart()
            }

            summary = (
                self.generate_dashboard_summary()
            )

            logger.info(
                "Visualization Pipeline Completed"
            )

            return {
                "visualizations":
                visualizations,

                "summary":
                summary
            }

        except Exception as error:

            logger.error(
                f"Visualization Pipeline Failed: "
                f"{error}"
            )

            raise

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    visualizer = CovidVisualization()

    results = (
        visualizer
        .run_visualization_pipeline()
    )

    print("\nCOVID Visualization Completed")

    print("\nGenerated Visualizations:")
    print(
        results["visualizations"]
    )

    print("\nDashboard Summary:")
    print(
        results["summary"]
    )