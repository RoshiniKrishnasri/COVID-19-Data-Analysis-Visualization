import json

notebook_path = 'c:/Users/roshi/Downloads/REAL_WORLD_PROJECTS/covid19-data-analysis-visualization-main (2)/covid19-data-analysis-visualization-main/covid19-data-analysis-visualization-main/notebooks/01_data_exploration.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        # Cell 59 (top_vaccinations)
        if 'top_vaccinations =' in source and 'total_vaccinations' in source:
            cell['source'] = [
                "# The 'owid-covid-data (1).csv' dataset does not contain vaccination data.\n",
                "# top_vaccinations = (\n",
                "#     df.groupby(\"country\")[\"total_vaccinations\"]\n",
                "#     .sum()\n",
                "#     .sort_values(ascending=False)\n",
                "#     .head(10)\n",
                "# )\n",
                "# top_vaccinations\n"
            ]
            cell['outputs'] = []
            
        # Cell 24 (global_trend)
        if 'global_trend =' in source and 'total_vaccinations' in source:
            new_source = []
            for line in cell['source']:
                if '"total_vaccinations"' in line:
                    continue
                if '"new_deaths",' in line:
                    new_source.append(line.replace('"new_deaths",', '"new_deaths"'))
                else:
                    new_source.append(line)
            cell['source'] = new_source
            cell['outputs'] = []
            
        # Cell 27 (plot new_vaccinations)
        if 'plt.title("Global COVID-19 Vaccinations Over Time")' in source:
            new_source = []
            for line in cell['source']:
                new_source.append('# ' + line if not line.startswith('#') else line)
            new_source.insert(0, "# The 'owid-covid-data (1).csv' dataset does not contain vaccination data.\n")
            cell['source'] = new_source
            cell['outputs'] = []
            
        # Clear errors in 25 and 26 so they are clean
        if 'plt.title("Global COVID-19 Cases Over Time")' in source or 'plt.title("Global COVID-19 Deaths Over Time")' in source:
            cell['outputs'] = []

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Notebook updated successfully.')
