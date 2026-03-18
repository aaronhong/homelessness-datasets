"""
Compile and standardize PIT and HIC data from raw Excel files into CSVs.

Outputs:
  data/processed/pit_by_coc.csv  — PIT counts by CoC, all years, long format
  data/processed/hic_by_coc.csv  — HIC counts by CoC, all years, long format

Run download.py first to populate data/raw/.
"""

import os
import re
import pandas as pd
import pyxlsb

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def clean_colname(name):
    """Standardize a column name to snake_case with no special characters."""
    name = str(name).lower().strip()
    name = name.replace("/", "_")          # slashes → underscore
    name = name.replace("-", "_")          # dashes → underscore
    name = re.sub(r"[,.()\[\]]", "", name) # remove punctuation
    name = re.sub(r"\s+", "_", name)       # spaces → underscore
    name = re.sub(r"_+", "_", name)        # collapse multiple underscores
    name = name.strip("_")                 # strip leading/trailing underscores
    return name


def clean_columns(df):
    """Apply clean_colname to all columns, deduplicating if needed."""
    seen = {}
    new_cols = []
    for c in df.columns:
        name = clean_colname(c)
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        new_cols.append(name)
    df.columns = new_cols
    return df


def read_xlsb(path):
    """Read all sheets from a .xlsb file into a dict of DataFrames."""
    sheets = {}
    with pyxlsb.open_workbook(path) as wb:
        for sheet_name in wb.sheets:
            with wb.get_sheet(sheet_name) as sheet:
                rows = []
                for row in sheet.rows():
                    rows.append([cell.v for cell in row])
            if rows:
                df = pd.DataFrame(rows[1:], columns=rows[0])
                sheets[sheet_name] = df
    return sheets


def compile_pit_by_coc():
    path = os.path.join(RAW_DIR, "pit", "2007-2024-PIT-Counts-by-CoC.xlsb")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Not found: {path}\nRun download.py first.")

    print("Reading PIT by CoC (this may take a moment)...")
    sheets = read_xlsb(path)

    frames = []
    for sheet_name, df in sheets.items():
        # Each sheet is typically one year; sheet name is the year
        df = df.copy()
        df = clean_columns(df)
        df.dropna(how="all", inplace=True)

        # Detect year from sheet name (e.g. "2024", "2023")
        year = None
        try:
            year = int(str(sheet_name).strip())
        except ValueError:
            pass

        if year:
            df["year"] = year

        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    combined = clean_columns(combined)

    # Drop rows with no year (blank/header rows between sheets)
    combined = combined[combined["year"].notna()]
    combined["year"] = combined["year"].astype(int)

    out_path = os.path.join(PROCESSED_DIR, "pit_by_coc.csv")
    combined.to_csv(out_path, index=False)
    print(f"Saved: {out_path} ({len(combined):,} rows)")
    return combined


def compile_hic_by_coc():
    path = os.path.join(RAW_DIR, "hic", "2007-2024-HIC-Counts-by-CoC.xlsx")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Not found: {path}\nRun download.py first.")

    print("Reading HIC by CoC...")
    xl = pd.ExcelFile(path)

    frames = []
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=0)
        df = df.copy()
        df.dropna(how="all", inplace=True)

        year = None
        try:
            year = int(str(sheet_name).strip())
        except ValueError:
            pass

        if year:
            df["year"] = year

        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    combined = clean_columns(combined)

    # Drop rows with no year
    combined = combined[combined["year"].notna()]
    combined["year"] = combined["year"].astype(int)

    out_path = os.path.join(PROCESSED_DIR, "hic_by_coc.csv")
    combined.to_csv(out_path, index=False)
    print(f"Saved: {out_path} ({len(combined):,} rows)")
    return combined


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    compile_pit_by_coc()
    compile_hic_by_coc()
    print("\nDone. Processed files are in data/processed/")


if __name__ == "__main__":
    main()
