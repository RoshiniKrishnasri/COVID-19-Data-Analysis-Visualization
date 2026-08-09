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

    print(f"Patched: {filename}")

# Data paths are already set to owid-covid-data (1).csv
# This script is kept for reference. Run again if you need to re-patch paths.

DATA_FILE = "owid-covid-data (1).csv"

files_to_check = ["data_loader.py", "data_cleaning.py"]

for fname in files_to_check:
    fpath = os.path.join(src_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if DATA_FILE in content:
        print(f"[OK] {fname} already uses correct dataset: {DATA_FILE}")
    else:
        print(f"[WARN] {fname} may need path update.")
