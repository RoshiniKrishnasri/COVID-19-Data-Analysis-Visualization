import os

src_dir = r"c:\Users\roshi\Downloads\REAL_WORLD_PROJECTS\covid19-data-analysis-visualization-main (2)\covid19-data-analysis-visualization-main\covid19-data-analysis-visualization-main\src"

def patch_file(filename, replacements):
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. data_loader.py
patch_file("data_loader.py", [
    ('    "new_deaths",\n    "new_vaccinations"\n]', '    "new_deaths"\n]'),
    ('    "deaths": "new_deaths",\n    "vaccinations": "new_vaccinations",\n}', '    "deaths": "new_deaths"\n}'),
    ('                "new_deaths",\n                "new_vaccinations"\n            ]', '                "new_deaths"\n            ]'),
])

# 2. data_cleaning.py
patch_file("data_cleaning.py", [
    ('    "new_deaths",\n    "new_vaccinations"\n]', '    "new_deaths"\n]'),
    ('                "deaths": "new_deaths",\n                "vaccinations": "new_vaccinations",\n            }', '                "deaths": "new_deaths"\n            }'),
    ('                "new_deaths",\n                "new_vaccinations"\n            ]', '                "new_deaths"\n            ]'),
])

# 3. analysis.py
analysis_replacements = [
    # Remove total vaccinations from global_summary
    ('''                "total_vaccinations": int(
                    latest_df[
                        "total_vaccinations"
                    ].sum()
                ),

''', ''),
    # Clear out vaccination_analysis
    ('''    def vaccination_analysis(self):
        """
        Analyze vaccination progress.
        """

        try:

            logger.info(
                "Generating Vaccination Analysis"
            )

            vaccination_df = (
                self.df.groupby("country")[
                    "total_vaccinations"
                ]
                .max()
                .reset_index()
            )

            vaccination_df = (
                vaccination_df.sort_values(
                    by="total_vaccinations",
                    ascending=False
                )
                .head(10)
            )

            logger.info(
                "Vaccination Analysis Completed"
            )

            return vaccination_df

        except Exception as error:

            logger.error(
                f"Vaccination Analysis Failed: "
                f"{error}"
            )

            raise''', '''    def vaccination_analysis(self):
        return None'''),
    # Remove it from generate_all_analysis
    ('''                "vaccination_analysis":
                self.vaccination_analysis(),
''', '')
]
patch_file("analysis.py", analysis_replacements)

# 4. feature_engineering.py
fe_replacements = [
    ('''    def create_total_vaccination_feature(self):
        """
        Generate cumulative vaccination feature.
        """

        try:

            logger.info(
                "Creating Vaccination Feature"
            )

            self.df[
                "total_vaccinations_country"
            ] = (
                self.df.groupby("country")[
                    "new_vaccinations"
                ]
                .cumsum()
            )

            logger.info(
                "Vaccination Feature Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Vaccination Feature Failed: "
                f"{error}"
            )

            raise''', '''    def create_total_vaccination_feature(self):
        return self.df'''),
    ('''    def create_vaccination_rolling_average(self):
        """
        Generate vaccination rolling average.
        """

        try:

            logger.info(
                "Creating Vaccination Rolling Average"
            )

            self.df[
                "rolling_avg_vaccinations"
            ] = (
                self.df.groupby("country")[
                    "new_vaccinations"
                ]
                .transform(
                    lambda x: x.rolling(
                        window=7,
                        min_periods=1
                    ).mean()
                )
            )

            logger.info(
                "Vaccination Rolling Average Created"
            )

            return self.df

        except Exception as error:

            logger.error(
                f"Vaccination Rolling Average Failed: "
                f"{error}"
            )

            raise''', '''    def create_vaccination_rolling_average(self):
        return self.df''')
]
patch_file("feature_engineering.py", fe_replacements)

# 5. visualization.py
viz_replacements = [
    ('''    def generate_global_vaccination_trend(self):
        """
        Generate global vaccination trend chart.
        """

        try:

            logger.info(
                "Generating Vaccination Trend"
            )

            global_trend = (
                self.df.groupby("date")[
                    "new_vaccinations"
                ]
                .sum()
                .reset_index()
            )

            plt.figure(figsize=(14, 6))

            sns.lineplot(
                data=global_trend,
                x="date",
                y="new_vaccinations",
                color="#2ecc71",
                linewidth=2
            )

            plt.title(
                "Global Daily COVID-19 Vaccinations",
                fontsize=16,
                fontweight="bold"
            )

            plt.xlabel(
                "Date",
                fontsize=12
            )

            plt.ylabel(
                "Daily Vaccinations",
                fontsize=12
            )

            plt.xticks(rotation=45)

            plt.grid(
                True,
                linestyle="--",
                alpha=0.7
            )

            plt.tight_layout()

            vaccination_path = os.path.join(
                self.output_dir,
                "global_vaccination_trend.png"
            )

            plt.savefig(
                vaccination_path,
                dpi=300
            )

            plt.close()

            logger.info(
                "Vaccination Trend Generated"
            )

            return vaccination_path

        except Exception as error:

            logger.error(
                f"Vaccination Trend Failed: "
                f"{error}"
            )

            raise''', '''    def generate_global_vaccination_trend(self):
        return None'''),
    ('''                "global_vaccination_trend":
                self.generate_global_vaccination_trend(),
''', '')
]
patch_file("visualization.py", viz_replacements)

print("Patching complete.")
