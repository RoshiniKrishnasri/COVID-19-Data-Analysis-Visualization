import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
)

from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# =============================================================================
# FLASK APP CONFIGURATION
# =============================================================================

app = Flask(__name__)

# -----------------------------------------------------------------------------
# SECRET KEY
# -----------------------------------------------------------------------------

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "covid-dashboard-secret-key"
)

# -----------------------------------------------------------------------------
# ENABLE CORS
# -----------------------------------------------------------------------------

CORS(app)

# -----------------------------------------------------------------------------
# PROXY FIX
# -----------------------------------------------------------------------------

app.wsgi_app = ProxyFix(app.wsgi_app)

# -----------------------------------------------------------------------------
# BASE DIRECTORY
# -----------------------------------------------------------------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =============================================================================
# PATH CONFIGURATIONS
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

LOGS_DIR = os.path.join(BASE_DIR, "logs")

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

file_handler = RotatingFileHandler(
    os.path.join(LOGS_DIR, "app.log"),
    maxBytes=10240,
    backupCount=10
)

file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s "
        "[in %(pathname)s:%(lineno)d]"
    )
)

file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)

app.logger.info("COVID Flask Dashboard Startup")

# =============================================================================
# GLOBAL DATAFRAME CACHE
# =============================================================================

covid_df = pd.DataFrame()

# =============================================================================
# DATASET COLUMN MAPPING
# =============================================================================

COLUMN_MAPPING = {
    "country": [
        "country",
        "location",
        "entity"
    ],
    "date": [
        "date",
        "day"
    ],
    "new_cases": [
        "new_cases",
        "cases",
        "daily_cases"
    ],
    "new_deaths": [
        "new_deaths",
        "deaths",
        "daily_deaths"
    ],
    "new_tests": [
        "new_tests",
        "tests",
        "daily_tests"
    ],
    "total_tests": [
        "total_tests",
        "cumulative_tests"
    ]
}

# =============================================================================
# DATA LOADING FUNCTION
# =============================================================================


def find_matching_column(df_columns, possible_names):
    """
    Find matching dataset column.
    """

    for col in possible_names:
        if col in df_columns:
            return col

    return None


def load_dataset():
    """
    Load and clean COVID dataset.
    """

    global covid_df

    try:

        dataset_path = (
            PROCESSED_DATA_PATH
            if os.path.exists(PROCESSED_DATA_PATH)
            else RAW_DATA_PATH
        )

        if not os.path.exists(dataset_path):

            raise FileNotFoundError(
                f"Dataset not found at: {dataset_path}"
            )

        app.logger.info(
            f"Loading dataset from: {dataset_path}"
        )

        covid_df = pd.read_csv(dataset_path)

        # ---------------------------------------------------------------------
        # LOWERCASE COLUMN NAMES
        # ---------------------------------------------------------------------

        covid_df.columns = [
            col.strip().lower()
            for col in covid_df.columns
        ]

        app.logger.info(
            f"Dataset Columns: {covid_df.columns.tolist()}"
        )

        # ---------------------------------------------------------------------
        # STANDARDIZE COLUMN NAMES
        # ---------------------------------------------------------------------

        standardized_columns = {}

        for standard_name, possible_names in COLUMN_MAPPING.items():

            matched_column = find_matching_column(
                covid_df.columns,
                possible_names
            )

            if matched_column:
                standardized_columns[matched_column] = standard_name

        covid_df.rename(
            columns=standardized_columns,
            inplace=True
        )

        # ---------------------------------------------------------------------
        # CREATE MISSING COLUMNS
        # ---------------------------------------------------------------------

        required_columns = [
            "country",
            "date",
            "new_cases",
            "new_deaths",
            "new_tests",
            "total_tests"
        ]

        for col in required_columns:

            if col not in covid_df.columns:

                app.logger.warning(
                    f"Missing column created: {col}"
                )

                if col == "date":
                    covid_df[col] = pd.NaT
                elif col == "country":
                    covid_df[col] = "Unknown"
                else:
                    covid_df[col] = 0

        # ---------------------------------------------------------------------
        # CONVERT DATE COLUMN
        # ---------------------------------------------------------------------

        covid_df["date"] = pd.to_datetime(
            covid_df["date"],
            errors="coerce"
        )

        # ---------------------------------------------------------------------
        # REMOVE DUPLICATES
        # ---------------------------------------------------------------------

        covid_df.drop_duplicates(inplace=True)

        # ---------------------------------------------------------------------
        # HANDLE MISSING VALUES
        # ---------------------------------------------------------------------

        covid_df["country"] = (
            covid_df["country"]
            .astype(str)
            .fillna("Unknown")
        )

        numeric_columns = [
            "new_cases",
            "new_deaths",
            "new_tests",
            "total_tests"
        ]

        for col in numeric_columns:

            covid_df[col] = pd.to_numeric(
                covid_df[col],
                errors="coerce"
            ).fillna(0)

        # ---------------------------------------------------------------------
        # REMOVE INVALID DATES
        # ---------------------------------------------------------------------

        covid_df = covid_df[
            covid_df["date"].notna()
        ]

        # ---------------------------------------------------------------------
        # SORT DATA
        # ---------------------------------------------------------------------

        covid_df.sort_values(
            by="date",
            inplace=True
        )

        covid_df.reset_index(
            drop=True,
            inplace=True
        )

        app.logger.info(
            f"Dataset loaded successfully. "
            f"Shape: {covid_df.shape}"
        )

    except Exception as e:

        app.logger.error(
            f"Error loading dataset: {e}"
        )

        covid_df = pd.DataFrame()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_latest_global_summary(df):
    """
    Get latest global summary metrics.
    """

    try:

        if df.empty:

            return {
                "latest_date": "N/A",
                "total_cases": 0,
                "total_deaths": 0,
                "total_tests": 0,
                "countries": 0,
            }

        latest_date = df["date"].max()

        latest_df = df[
            df["date"] == latest_date
        ]

        total_cases = int(
            latest_df["new_cases"].sum()
        )

        total_deaths = int(
            latest_df["new_deaths"].sum()
        )

        total_tests = int(df["total_tests"].sum())

        countries = latest_df[
            "country"
        ].nunique()

        return {
            "latest_date": latest_date.strftime("%Y-%m-%d"),
            "total_cases": total_cases,
            "total_deaths": total_deaths,
            "total_tests": total_tests,
            "countries": countries,
        }

    except Exception as e:

        app.logger.error(
            f"Summary calculation error: {e}"
        )

        return {
            "latest_date": "N/A",
            "total_cases": 0,
            "total_deaths": 0,
            "total_tests": 0,
            "countries": 0,
        }

# =============================================================================
# HOME ROUTE
# =============================================================================


@app.route("/")
def home():
    """
    Homepage route.
    """

    summary = get_latest_global_summary(covid_df)

    return render_template(
        "index.html",
        summary=summary,
        current_year=datetime.now().year,
    )

# =============================================================================
# DASHBOARD ROUTE
# =============================================================================


@app.route("/dashboard")
def dashboard():
    """
    Main dashboard route.
    """

    countries = []

    if not covid_df.empty:

        countries = sorted(
            covid_df["country"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    summary = get_latest_global_summary(covid_df)

    return render_template(
        "dashboard.html",
        countries=countries,
        summary=summary,
        current_year=datetime.now().year,
    )

# =============================================================================
# ANALYSIS ROUTE
# =============================================================================


@app.route("/analysis")
def analysis():
    """
    Insights and analytical storytelling page.
    """

    return render_template("analysis.html")

# =============================================================================
# ABOUT ROUTE
# =============================================================================


@app.route("/about")
def about():
    """
    About project page.
    """

    return render_template("about.html")

# =============================================================================
# API: GLOBAL TREND DATA
# =============================================================================


@app.route("/api/global-trend")
def global_trend_api():
    """
    Returns global COVID trend data.
    """

    try:

        if covid_df.empty:

            return jsonify({
                "error": "Dataset unavailable"
            }), 500

        trend_df = covid_df.groupby(
            "date"
        ).agg({
            "new_cases": "sum",
            "new_deaths": "sum",
            "new_tests": "sum",
        }).reset_index()

        trend_df["date"] = (
            trend_df["date"]
            .astype(str)
        )

        response = {
            "dates": trend_df["date"].tolist(),
            "cases": trend_df[
                "new_cases"
            ].tolist(),
            "deaths": trend_df[
                "new_deaths"
            ].tolist(),
            "tests": trend_df[
                "new_tests"
            ].tolist(),
        }

        return jsonify(response)

    except Exception as e:

        app.logger.error(
            f"Global trend API error: {e}"
        )

        return jsonify({
            "error": "Unable to fetch trend data"
        }), 500

# =============================================================================
# API: COUNTRY ANALYSIS
# =============================================================================


@app.route("/api/country/<country_name>")
def country_analysis_api(country_name):
    """
    Country-specific COVID analysis.
    """

    try:

        if covid_df.empty:

            return jsonify({
                "error": "Dataset unavailable"
            }), 500

        country_df = covid_df[
            covid_df["country"]
            .astype(str)
            .str.lower() == country_name.lower()
        ]

        if country_df.empty:

            return jsonify({
                "error": f"No data found for {country_name}"
            }), 404

        country_df = country_df.sort_values(
            "date"
        )

        country_df["date"] = (
            country_df["date"]
            .astype(str)
        )

        response = {
            "country": country_name,
            "dates": country_df[
                "date"
            ].tolist(),
            "cases": country_df[
                "new_cases"
            ].tolist(),
            "deaths": country_df[
                "new_deaths"
            ].tolist(),
            "tests": country_df[
                "new_tests"
            ].tolist(),
        }

        return jsonify(response)

    except Exception as e:

        app.logger.error(
            f"Country analysis API error: {e}"
        )

        return jsonify({
            "error": "Unable to fetch country analysis"
        }), 500

# =============================================================================
# API: TOP HOTSPOTS
# =============================================================================


@app.route("/api/top-hotspots")
def top_hotspots_api():
    """
    Returns top COVID hotspot regions.
    """

    try:

        if covid_df.empty:

            return jsonify({
                "error": "Dataset unavailable"
            }), 500

        latest_date = covid_df["date"].max()

        latest_df = covid_df[
            covid_df["date"] == latest_date
        ]

        hotspot_df = latest_df.sort_values(
            by="new_cases",
            ascending=False
        ).head(10)

        response = {
            "countries": hotspot_df[
                "country"
            ].tolist(),
            "cases": hotspot_df[
                "new_cases"
            ].tolist(),
        }

        return jsonify(response)

    except Exception as e:

        app.logger.error(
            f"Hotspot API error: {e}"
        )

        return jsonify({
            "error": "Unable to fetch hotspots"
        }), 500

# =============================================================================
# API: K-MEANS CLUSTERING
# =============================================================================


@app.route("/api/kmeans")
def kmeans_api():
    """
    Perform K-Means clustering on daily COVID case and death records.
    """

    try:

        if covid_df.empty:

            return jsonify({
                "error": "Dataset unavailable"
            }), 500

        # Filter out records where new_cases and new_deaths are both 0 for cleaner clustering
        df_clean = covid_df[
            (covid_df["new_cases"] > 0) | (covid_df["new_deaths"] > 0)
        ].copy()

        if len(df_clean) < 10:
            df_clean = covid_df.copy()

        features = ["new_cases", "new_deaths"]
        X = df_clean[features].values

        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Run K-Means
        n_clusters = 5
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        df_clean["cluster"] = labels

        # Calculate centroids in original scale
        centroids_scaled = kmeans.cluster_centers_
        centroids = scaler.inverse_transform(centroids_scaled)

        # Calculate silhouette score on a sample of 2000 points for speed
        sample_size = min(2000, len(df_clean))
        df_sample_sil = df_clean.sample(n=sample_size, random_state=42)
        X_sil_scaled = scaler.transform(df_sample_sil[features].values)
        sil_score = float(
            silhouette_score(X_sil_scaled, df_sample_sil["cluster"].values)
        )

        # Prepare sample for visualization (max 5000 points)
        vis_sample_size = min(5000, len(df_clean))
        df_vis_sample = df_clean.sample(n=vis_sample_size, random_state=42)

        points = []
        for _, row in df_vis_sample.iterrows():
            points.append({
                "x": float(row["new_cases"]),
                "y": float(row["new_deaths"]),
                "cluster": int(row["cluster"]),
                "country": str(row["country"]),
                "date": row["date"].strftime("%Y-%m-%d")
            })

        centroid_points = []
        for i, center in enumerate(centroids):
            centroid_points.append({
                "x": float(center[0]),
                "y": float(center[1]),
                "cluster": i
            })

        # Cluster sizes and distribution
        cluster_counts = df_clean["cluster"].value_counts().to_dict()
        distribution = [
            {"cluster": int(k), "count": int(v)}
            for k, v in cluster_counts.items()
        ]
        # Sort by count descending
        distribution = sorted(
            distribution,
            key=lambda x: x["count"],
            reverse=True
        )

        # Summary statistics
        total_records = len(df_clean)
        largest_cluster = distribution[0]["count"] if distribution else 0

        # Insights generation
        largest_cluster_id = distribution[0]["cluster"] if distribution else 0
        smallest_cluster_id = distribution[-1]["cluster"] if distribution else 0

        smallest_count = (
            distribution[-1]["count"]
            if len(distribution) > 1
            else 1
        )
        is_imbalanced = (largest_cluster / smallest_count) > 3.0
        balance_status = "imbalanced" if is_imbalanced else "balanced"

        response = {
            "points": points,
            "centroids": centroid_points,
            "sil_score": round(sil_score, 4),
            "total_records": total_records,
            "n_clusters": n_clusters,
            "largest_cluster_size": largest_cluster,
            "distribution": distribution,
            "insights": {
                "largest_cluster": largest_cluster_id,
                "smallest_cluster": smallest_cluster_id,
                "balance": balance_status,
                "interpretation": (
                    f"The clustering highlights different pandemic phases. "
                    f"Cluster {largest_cluster_id} is the largest, capturing "
                    f"low-transmission periods/regions. Cluster {smallest_cluster_id} "
                    f"is the smallest, capturing extreme case-death spikes. "
                    f"The distribution is {balance_status}."
                )
            }
        }

        return jsonify(response)

    except Exception as e:

        app.logger.error(
            f"KMeans API error: {e}"
        )

        return jsonify({
            "error": "Unable to calculate KMeans clusters"
        }), 500


# =============================================================================
# API: 7-DAY MOVING AVERAGE TREND
# =============================================================================


@app.route("/api/moving-average")
def moving_average_api():
    """
    Returns 7-day moving average for global daily cases and deaths.
    """

    try:

        if covid_df.empty:
            return jsonify({"error": "Dataset unavailable"}), 500

        trend_df = covid_df.groupby("date").agg({
            "new_cases": "sum",
            "new_deaths": "sum"
        }).reset_index().sort_values("date")

        trend_df["ma_cases"]  = trend_df["new_cases"].rolling(window=7, min_periods=1).mean().round(1)
        trend_df["ma_deaths"] = trend_df["new_deaths"].rolling(window=7, min_periods=1).mean().round(1)

        trend_df["date"] = trend_df["date"].astype(str)

        return jsonify({
            "dates":     trend_df["date"].tolist(),
            "cases":     trend_df["new_cases"].tolist(),
            "deaths":    trend_df["new_deaths"].tolist(),
            "ma_cases":  trend_df["ma_cases"].tolist(),
            "ma_deaths": trend_df["ma_deaths"].tolist(),
        })

    except Exception as e:
        app.logger.error(f"Moving average API error: {e}")
        return jsonify({"error": "Unable to fetch moving average data"}), 500


# =============================================================================
# API: CORRELATION HEATMAP
# =============================================================================


@app.route("/api/correlation")
def correlation_api():
    """
    Returns Pearson correlation matrix for key COVID metrics.
    """

    try:

        if covid_df.empty:
            return jsonify({"error": "Dataset unavailable"}), 500

        cols = ["new_cases", "new_deaths", "new_tests"]
        df_corr = covid_df[cols].copy()

        # Compute positivity rate where tests > 0
        df_corr["positivity_rate"] = np.where(
            covid_df["new_tests"] > 0,
            (covid_df["new_cases"] / covid_df["new_tests"] * 100).clip(0, 100),
            np.nan
        )

        labels = ["Daily Cases", "Daily Deaths", "Daily Tests", "Positivity Rate"]
        corr_cols = ["new_cases", "new_deaths", "new_tests", "positivity_rate"]

        corr_matrix = df_corr[corr_cols].dropna().corr(method="pearson").round(3)

        matrix_values = corr_matrix.values.tolist()

        return jsonify({
            "labels": labels,
            "matrix": matrix_values
        })

    except Exception as e:
        app.logger.error(f"Correlation API error: {e}")
        return jsonify({"error": "Unable to compute correlation"}), 500


# =============================================================================
# API: BUBBLE CHART
# =============================================================================


@app.route("/api/bubble")
def bubble_api():
    """
    Returns sampled data for bubble chart:
    X = Daily Tests, Y = Daily Cases, Size = Daily Deaths, Color = K-Means Cluster.
    """

    try:

        if covid_df.empty:
            return jsonify({"error": "Dataset unavailable"}), 500

        df_b = covid_df[
            (covid_df["new_cases"] > 0) &
            (covid_df["new_tests"] > 0)
        ].copy()

        if len(df_b) < 10:
            return jsonify({"error": "Insufficient data"}), 500

        features = ["new_cases", "new_deaths"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_b[features].values)

        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df_b["cluster"] = kmeans.fit_predict(X_scaled)

        sample_size = min(2000, len(df_b))
        df_sample = df_b.sample(n=sample_size, random_state=42)

        points = []
        for _, row in df_sample.iterrows():
            points.append({
                "x":       float(row["new_tests"]),
                "y":       float(row["new_cases"]),
                "r":       float(max(row["new_deaths"], 0)),
                "cluster": int(row["cluster"]),
                "country": str(row["country"]),
                "date":    str(row["date"])[:10]
            })

        return jsonify({"points": points})

    except Exception as e:
        app.logger.error(f"Bubble API error: {e}")
        return jsonify({"error": "Unable to fetch bubble data"}), 500


# =============================================================================
# API: ANALYSIS - TOP COUNTRIES (TOTAL CASES)
# =============================================================================

@app.route("/api/analysis/top-countries")
def analysis_top_countries():
    """
    Returns the top 10 countries by total cases for the analysis bar chart.
    """
    try:
        if covid_df.empty:
            return jsonify({"error": "Dataset unavailable"}), 500

        top_df = covid_df.groupby("country")["new_cases"].sum().reset_index()
        top_df = top_df.sort_values(by="new_cases", ascending=False).head(10)

        return jsonify({
            "labels": top_df["country"].tolist(),
            "data": top_df["new_cases"].tolist(),
        })
    except Exception as e:
        app.logger.error(f"Top Countries API error: {e}")
        return jsonify({"error": "Unable to fetch top countries"}), 500


# =============================================================================
# API: ANALYSIS - MORTALITY RATE
# =============================================================================

@app.route("/api/analysis/mortality")
def analysis_mortality():
    """
    Returns the top 10 countries by Case Fatality Rate (CFR)
    for countries with at least 100,000 cases to avoid outliers.
    """
    try:
        if covid_df.empty:
            return jsonify({"error": "Dataset unavailable"}), 500

        mortality_df = covid_df.groupby("country").agg(
            total_cases=("new_cases", "sum"),
            total_deaths=("new_deaths", "sum")
        ).reset_index()

        # Filter out low-case countries to get meaningful mortality rates
        mortality_df = mortality_df[mortality_df["total_cases"] >= 100000].copy()
        
        # Calculate CFR
        mortality_df["cfr"] = (mortality_df["total_deaths"] / mortality_df["total_cases"] * 100).round(2)
        
        top_mortality = mortality_df.sort_values(by="cfr", ascending=False).head(10)

        return jsonify({
            "labels": top_mortality["country"].tolist(),
            "data": top_mortality["cfr"].tolist(),
            "cases": top_mortality["total_cases"].tolist(),
            "deaths": top_mortality["total_deaths"].tolist(),
        })
    except Exception as e:
        app.logger.error(f"Mortality Rate API error: {e}")
        return jsonify({"error": "Unable to fetch mortality rate data"}), 500


@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "500.html"
    ), 500

# =============================================================================
# HEALTH CHECK ROUTE
# =============================================================================


@app.route("/health")
def health_check():
    """
    Health check endpoint.
    """

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "dataset_loaded": not covid_df.empty,
        "records": len(covid_df),
    })

# =============================================================================
# APPLICATION INITIALIZATION
# =============================================================================


def initialize_application():
    """
    Initialize application resources.
    """

    load_dataset()


initialize_application()

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv(
            "FLASK_DEBUG",
            "False"
        ) == "True",
    )