# =============================================================================
# tests/test_flask_routes.py
# Production-Level Flask Route Tests
# COVID Data Analysis & Visualization Flask Application
# =============================================================================

import os
import sys
import unittest
import json

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
# IMPORT FLASK APPLICATION
# =============================================================================

from app import app

# =============================================================================
# TEST CLASS
# =============================================================================


class TestFlaskRoutes(unittest.TestCase):
    """
    Unit tests for Flask routes and APIs.
    """

    # =========================================================================
    # SETUP TEST CLIENT
    # =========================================================================

    @classmethod
    def setUpClass(cls):
        """
        Configure Flask test client.
        """

        app.config["TESTING"] = True

        cls.client = app.test_client()

        print(
            "\nInitializing Flask Route Tests..."
        )

    # =========================================================================
    # TEST HOME ROUTE
    # =========================================================================

    def test_home_route(self):
        """
        Test homepage route.
        """

        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200,
            msg=(
                "Home route failed."
            )
        )

    # =========================================================================
    # TEST DASHBOARD ROUTE
    # =========================================================================

    def test_dashboard_route(self):
        """
        Test dashboard page route.
        """

        response = self.client.get("/dashboard")

        self.assertEqual(
            response.status_code,
            200,
            msg=(
                "Dashboard route failed."
            )
        )

    # =========================================================================
    # TEST ANALYSIS ROUTE
    # =========================================================================

    def test_analysis_route(self):
        """
        Test analysis page route.
        """

        response = self.client.get("/analysis")

        self.assertEqual(
            response.status_code,
            200,
            msg=(
                "Analysis route failed."
            )
        )

    # =========================================================================
    # TEST ABOUT ROUTE
    # =========================================================================

    def test_about_route(self):
        """
        Test about page route.
        """

        response = self.client.get("/about")

        self.assertEqual(
            response.status_code,
            200,
            msg=(
                "About route failed."
            )
        )

    # =========================================================================
    # TEST HEALTH CHECK ROUTE
    # =========================================================================

    def test_health_check_route(self):
        """
        Test health check endpoint.
        """

        response = self.client.get("/health")

        self.assertEqual(
            response.status_code,
            200
        )

        response_data = json.loads(
            response.data
        )

        self.assertIn(
            "status",
            response_data
        )

        self.assertIn(
            "dataset_loaded",
            response_data
        )

    # =========================================================================
    # TEST GLOBAL TREND API
    # =========================================================================

    def test_global_trend_api(self):
        """
        Test global trend API endpoint.
        """

        response = self.client.get(
            "/api/global-trend"
        )

        self.assertEqual(
            response.status_code,
            200,
            msg=(
                "Global trend API failed."
            )
        )

        response_data = json.loads(
            response.data
        )

        self.assertIn(
            "dates",
            response_data
        )

        self.assertIn(
            "cases",
            response_data
        )

        self.assertIn(
            "deaths",
            response_data
        )

        self.assertIn(
            "tests",
            response_data
        )

    # =========================================================================
    # TEST COUNTRY API VALID COUNTRY
    # =========================================================================

    def test_country_analysis_api_valid(self):
        """
        Test country analysis API
        with valid country.
        """

        response = self.client.get(
            "/api/country/India"
        )

        self.assertIn(
            response.status_code,
            [200, 404]
        )

        if response.status_code == 200:

            response_data = json.loads(
                response.data
            )

            self.assertIn(
                "country",
                response_data
            )

            self.assertIn(
                "dates",
                response_data
            )

    # =========================================================================
    # TEST COUNTRY API INVALID COUNTRY
    # =========================================================================

    def test_country_analysis_api_invalid(self):
        """
        Test country analysis API
        with invalid country.
        """

        response = self.client.get(
            "/api/country/InvalidCountryXYZ"
        )

        self.assertEqual(
            response.status_code,
            404
        )

    # =========================================================================
    # TEST TOP HOTSPOTS API
    # =========================================================================

    def test_top_hotspots_api(self):
        """
        Test top hotspots API.
        """

        response = self.client.get(
            "/api/top-hotspots"
        )

        self.assertEqual(
            response.status_code,
            200,
            msg=(
                "Top hotspots API failed."
            )
        )

        response_data = json.loads(
            response.data
        )

        self.assertIn(
            "countries",
            response_data
        )

        self.assertIn(
            "cases",
            response_data
        )

    # =========================================================================
    # TEST 404 PAGE
    # =========================================================================

    def test_404_error_page(self):
        """
        Test invalid route handling.
        """

        response = self.client.get(
            "/invalid-route"
        )

        self.assertEqual(
            response.status_code,
            404
        )

    # =========================================================================
    # TEST RESPONSE CONTENT TYPE
    # =========================================================================

    def test_api_response_content_type(self):
        """
        Validate API response content type.
        """

        response = self.client.get(
            "/api/global-trend"
        )

        self.assertEqual(
            response.content_type,
            "application/json"
        )

    # =========================================================================
    # TEST RESPONSE TIME
    # =========================================================================

    def test_response_not_empty(self):
        """
        Ensure response contains data.
        """

        response = self.client.get("/")

        self.assertGreater(
            len(response.data),
            0,
            msg=(
                "Empty response received."
            )
        )

    # =========================================================================
    # TEST TEMPLATE RENDERING
    # =========================================================================

    def test_template_rendering(self):
        """
        Ensure HTML rendering works.
        """

        response = self.client.get("/")

        self.assertIn(
            b"<html",
            response.data.lower()
        )

    # =========================================================================
    # TEST HEALTH ROUTE JSON FORMAT
    # =========================================================================

    def test_health_route_json_format(self):
        """
        Validate health route JSON.
        """

        response = self.client.get("/health")

        response_data = json.loads(
            response.data
        )

        self.assertIsInstance(
            response_data,
            dict
        )

    # =========================================================================
    # TEST API JSON FORMAT
    # =========================================================================

    def test_global_trend_json_format(self):
        """
        Validate JSON API format.
        """

        response = self.client.get(
            "/api/global-trend"
        )

        response_data = json.loads(
            response.data
        )

        self.assertIsInstance(
            response_data,
            dict
        )

    # =========================================================================
    # TEST STATUS CODE TYPES
    # =========================================================================

    def test_status_code_integer(self):
        """
        Validate status code datatype.
        """

        response = self.client.get("/")

        self.assertIsInstance(
            response.status_code,
            int
        )

    # =========================================================================
    # TEST MULTIPLE ROUTES
    # =========================================================================

    def test_multiple_routes(self):
        """
        Validate multiple routes together.
        """

        routes = [

            "/",

            "/dashboard",

            "/analysis",

            "/about",

            "/health"
        ]

        for route in routes:

            response = self.client.get(
                route
            )

            self.assertIn(
                response.status_code,
                [200]
            )

    # =========================================================================
    # TEST INVALID API METHOD
    # =========================================================================

    def test_invalid_method(self):
        """
        Test invalid POST request.
        """

        response = self.client.post(
            "/api/global-trend"
        )

        self.assertIn(
            response.status_code,
            [405, 500]
        )

    # =========================================================================
    # TEST HEAD REQUEST
    # =========================================================================

    def test_head_request(self):
        """
        Test HEAD request.
        """

        response = self.client.head("/")

        self.assertEqual(
            response.status_code,
            200
        )

    # =========================================================================
    # TEST OPTIONS REQUEST
    # =========================================================================

    def test_options_request(self):
        """
        Test OPTIONS request.
        """

        response = self.client.options("/")

        self.assertIn(
            response.status_code,
            [200]
        )

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )