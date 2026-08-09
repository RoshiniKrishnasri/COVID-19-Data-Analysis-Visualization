<div align="center">

# 🦠 COVID-19 Data Analysis & Visualization Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-Latest-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://chartjs.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-50%20Passed-success?style=for-the-badge&logo=pytest)](tests/)

<br/>

> **A production-ready, full-stack web dashboard** for exploring and visualizing global COVID-19 pandemic data — built with Flask, Pandas, Chart.js, and machine learning clustering.

<br/>

[🚀 Live Demo](#-getting-started) · [📊 Features](#-features) · [🛠 Tech Stack](#-tech-stack) · [📁 Project Structure](#-project-structure) · [🤝 Contributing](#-contributing)

</div>

---

## 📸 Screenshots

| Home Page | Interactive Dashboard |
|:---------:|:---------------------:|
| Real-time KPI cards with global COVID stats | Interactive time-series, bubble chart, and clustering |

| Analysis Page | About Page |
|:-------------:|:----------:|
| 6 in-depth chart analyses with insights | Project overview, dataset details, and methodology |

---

## ✨ Features

### 📊 Interactive Data Visualizations
- 📈 **Global Trends** — Time-series line charts for cases & deaths with country filter
- 🫧 **Bubble Chart** — Tests vs. Cases vs. Deaths multi-dimensional view
- 🗺️ **Hotspot Analysis** — Top 10 countries by case load
- 💉 **Vaccination Trends** — Global vaccination progress over time
- 🏆 **Country Rankings** — Side-by-side top country comparisons
- ⚰️ **Mortality Rate Analysis** — Case Fatality Rate (CFR) for major countries

### 🤖 Machine Learning
- **K-Means Clustering** — Groups countries into behavioral clusters based on COVID patterns
- **Silhouette Score Evaluation** — Automatic optimal cluster quality assessment
- **Standard Scaler Preprocessing** — Normalized features for fair comparison

### 🧹 Data Processing Pipeline
- **Automated Data Cleaning** — Handles missing values, type normalization, outlier filtering
- **Feature Engineering** — Derived metrics like positivity rate, CFR, smoothed rolling averages
- **Dual Dataset Support** — Works with both raw OWID data and pre-processed cleaned CSV

### 🎨 Premium UI/UX
- Fully responsive **Bootstrap 5** layout (mobile, tablet, desktop)
- **Dark Mode** toggle with persistent preference
- Smooth **CSS animations** and micro-interactions
- Real-time **toast notifications** and loading states
- Accessible color contrast across all components

### 🔧 Production-Ready Architecture
- RESTful **JSON API** endpoints for all chart data
- **CORS** enabled for cross-origin API access
- **Rotating log files** with structured logging
- **50 automated tests** across data loading, cleaning, and Flask routes
- Gunicorn-ready with a `Procfile` for deployment

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.9+, Flask 3.0, Werkzeug |
| **Data Processing** | Pandas 2.2, NumPy 1.26 |
| **Machine Learning** | scikit-learn 1.5, SciPy 1.13 |
| **Visualization** | Chart.js (frontend), Matplotlib, Plotly |
| **Frontend** | HTML5, Bootstrap 5.3, Font Awesome 6, Vanilla JS |
| **Server** | Gunicorn (production), Flask dev server (development) |
| **Testing** | Pytest 8.2 — 50 tests, 1 skipped |
| **Data Source** | [Our World in Data (OWID)](https://ourworldindata.org/covid-cases) |

---

## 📁 Project Structure

```
covid19-data-analysis-visualization/
│
├── 📄 app.py                    # Main Flask application (routes + API endpoints)
├── ⚙️  config.py                 # App configuration and environment settings
├── 📄 requirements.txt          # Python dependencies
├── 🚀 Procfile                  # Gunicorn deployment command
├── 🏃 runtime.txt               # Python runtime version
│
├── 📂 data/
│   ├── raw/                     # Original OWID COVID dataset (~9.5 MB)
│   └── processed/               # Cleaned & feature-engineered CSVs
│
├── 📂 src/
│   ├── data_loader.py           # Dataset loading with flexible column mapping
│   ├── data_cleaning.py         # Data cleaning pipeline
│   ├── analysis.py              # Statistical analysis functions
│   ├── feature_engineering.py   # Derived metrics and feature creation
│   └── visualization.py         # Matplotlib/Plotly chart generators
│
├── 📂 templates/
│   ├── base.html                # Base layout (navbar, footer, dark mode)
│   ├── index.html               # Home page with KPI cards
│   ├── dashboard.html           # Interactive charts dashboard
│   ├── analysis.html            # Deep-dive analysis charts
│   ├── about.html               # Project info and dataset details
│   ├── 404.html                 # Custom 404 error page
│   └── 500.html                 # Custom 500 error page
│
├── 📂 static/
│   ├── css/style.css            # Custom production stylesheet
│   ├── js/dashboard.js          # Dashboard chart logic
│   ├── js/analysis.js           # Analysis page chart logic
│   └── images/                  # Logo and pre-generated visualizations
│
├── 📂 notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_visual_analysis.ipynb
│
├── 📂 tests/
│   ├── test_data_loading.py     # 15 tests for dataset loading
│   ├── test_cleaning.py         # 16 tests for data cleaning
│   └── test_flask_routes.py     # 20 tests for Flask API routes
│
└── 📂 utils/
    ├── constants.py             # Project-wide constants
    └── helpers.py               # Utility helper functions
```

---

## 🚀 Getting Started

### Prerequisites
- Python **3.9+**
- pip

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RoshiniKrishnasri/COVID-19-Data-Analysis-Visualization.git
cd COVID-19-Data-Analysis-Visualization
```

### 2️⃣ Create & Activate a Virtual Environment

```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS / Linux
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

Open your browser at 👉 **http://localhost:5000**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page with KPI summary |
| `GET` | `/dashboard` | Interactive dashboard |
| `GET` | `/analysis` | Deep-dive analysis charts |
| `GET` | `/about` | Project info and methodology |
| `GET` | `/api/summary` | JSON summary stats (total cases, deaths, tests) |
| `GET` | `/api/trend` | JSON global/country time-series data |
| `GET` | `/api/dashboard/bubble` | JSON bubble chart clustering data |
| `GET` | `/api/analysis/top-countries` | JSON top 10 countries by total cases |
| `GET` | `/api/analysis/mortality` | JSON top 10 countries by CFR |
| `GET` | `/health` | Health check endpoint |

---

## 🧪 Running Tests

```bash
python -m pytest
```

**Expected Output:**
```
collected 51 items

tests/test_cleaning.py ................    [ 31%]
tests/test_data_loading.py ..............s [ 60%]
tests/test_flask_routes.py ....................  [100%]

================= 50 passed, 1 skipped in 54.29s =================
```

---

## 📊 Dataset

| Attribute | Details |
|-----------|---------|
| **Source** | [Our World in Data (OWID)](https://ourworldindata.org/covid-cases) |
| **File** | `owid-covid-data.csv` |
| **Size** | ~9.5 MB |
| **Records** | 44,785 rows × 41 columns |
| **Coverage** | Global — 200+ countries, 2020–2023 |
| **Key Columns** | `location`, `date`, `new_cases`, `new_deaths`, `new_tests`, `total_vaccinations`, `stringency_index`, `gdp_per_capita` |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** this repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and **commit**: `git commit -m "Add: your feature description"`
4. **Push** to your fork: `git push origin feature/your-feature-name`
5. Open a **Pull Request**

Please make sure all existing tests pass before submitting a PR.

---

## 👩‍💻 Author

<div align="center">

**Gaddam Roshini Krishna Sri**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-RoshiniKrishnasri-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/roshini-krishnasri/)
[![GitHub](https://img.shields.io/badge/GitHub-RoshiniKrishnasri-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RoshiniKrishnasri)
[![Email](https://img.shields.io/badge/Email-roshinikrishnasri%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:roshinikrishnasri@gmail.com)

*Data Science Enthusiast | Aspiring Data Analyst*

</div>

---

## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐ **If you found this project useful, please give it a star!** ⭐

*Built with ❤️ using Python, Flask, and real-world COVID-19 data*

</div>