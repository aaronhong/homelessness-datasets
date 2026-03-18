"""
Compile and standardize PIT and HIC data from raw Excel files into CSVs.

Outputs:
  data/processed/pit_by_coc.csv   — full PIT panel, all variables, all years
  data/processed/hic_by_coc.csv   — full HIC panel, all variables, all years
  data/processed/pit_core.csv     — PIT core variables available in all years (2007-2024)
  data/processed/hic_core.csv     — HIC core variables harmonized across all years (2007-2024)

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

    # Drop total/footnote rows — keep only valid CoC codes (e.g. AK-500, CA-600)
    combined = combined[combined["coc_number"].astype(str).str.match(r"^[A-Z]{2}-\d{3}$", na=False)]

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
        # Row 0 is a group header (merged cells); row 1 has the actual column names
        df = xl.parse(sheet_name, header=1)
        df = df.copy()
        df.dropna(how="all", inplace=True)
        if df.empty or len(df.columns) == 0:
            continue
        # Drop any rows where the CoC column is null or looks like a header repeat
        coc_col = df.columns[0]
        df = df[df[coc_col].notna()]
        df = df[~df[coc_col].astype(str).str.contains("CoC", case=False, na=False)]

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

    # Unify CoC identifier: early years used 'coc', later years used 'coc_number'
    if "coc" in combined.columns and "coc_number" in combined.columns:
        combined["coc_number"] = combined["coc_number"].fillna(combined["coc"])
        combined.drop(columns=["coc"], inplace=True)
    elif "coc" in combined.columns:
        combined.rename(columns={"coc": "coc_number"}, inplace=True)

    # Drop total/footnote rows — keep only valid CoC codes (e.g. AK-500)
    combined = combined[combined["coc_number"].astype(str).str.match(r"^[A-Z]{2}-\d{3}$", na=False)]

    out_path = os.path.join(PROCESSED_DIR, "hic_by_coc.csv")
    combined.to_csv(out_path, index=False)
    print(f"Saved: {out_path} ({len(combined):,} rows)")
    return combined


def compile_pit_core(pit_df):
    """Extract the 25 core PIT variables available in all years (2007-2024)."""
    core_cols = [
        "coc_number", "coc_name", "year",
        "overall_homeless",
        "overall_homeless_individuals",
        "overall_homeless_people_in_families",
        "overall_homeless_family_households",
        "overall_chronically_homeless_individuals",
        "sheltered_es_homeless",
        "sheltered_es_homeless_individuals",
        "sheltered_es_homeless_people_in_families",
        "sheltered_es_homeless_family_households",
        "sheltered_th_homeless",
        "sheltered_th_homeless_individuals",
        "sheltered_th_homeless_people_in_families",
        "sheltered_th_homeless_family_households",
        "sheltered_total_homeless",
        "sheltered_total_homeless_individuals",
        "sheltered_total_homeless_people_in_families",
        "sheltered_total_homeless_family_households",
        "sheltered_total_chronically_homeless_individuals",
        "unsheltered_homeless",
        "unsheltered_homeless_individuals",
        "unsheltered_homeless_people_in_families",
        "unsheltered_homeless_family_households",
        "unsheltered_chronically_homeless_individuals",
    ]
    df = pit_df[[c for c in core_cols if c in pit_df.columns]].copy()
    out_path = os.path.join(PROCESSED_DIR, "pit_core.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path} ({len(df):,} rows, {len(df.columns)} columns)")
    return df


def compile_hic_core(hic_df):
    """
    Build a harmonized HIC dataset with total year-round beds by program type.
    Variable names changed across years; this maps them to consistent names.

    Coverage:
      ES, TH, PSH: 2007-2024
      SH:          2008-2024
      RRH:         2013-2024
      OPH:         2014-2024
    """
    # Map of old column names → standard name, by year range
    # Each entry: (standard_name, [list of raw column names that mean the same thing])
    MAPPINGS = {
        "total_year_round_beds_es": [
            "total_year_round_es_beds",           # 2007-2013
            "total_year_round_beds_es",           # 2014+  (may be duplicated as es1)
        ],
        "total_year_round_beds_th": [
            "total_year_round_th_beds",
            "total_year_round_beds_th",
            "total_year_round_beds_th1",
        ],
        "total_year_round_beds_sh": [
            "total_year_round_sh_beds",
            "total_year_round_beds_sh",
            "total_year_round_beds_sh1",
        ],
        "total_year_round_beds_psh": [
            "total_year_round_psh_beds",
            "total_year_round_beds_psh",
        ],
        "total_year_round_beds_rrh": [
            "total_year_round_rrh_beds",
            "total_year_round_beds_rrh",
        ],
        "total_year_round_beds_oph": [
            "total_year_round_beds_oph",
        ],
        "total_seasonal_beds_es": [
            "total_seasonal_es_beds",
            "total_seasonal_beds_es",
        ],
        "total_overflow_beds_es": [
            "total_overflow_voucher_es_beds",
            "total_overflow_es_beds",
            "total_overflow_beds_es",
        ],
        "total_chronic_homeless_beds_psh": [
            "total_chronic_homeless_psh_beds",
            "dedicated_chronically_homeless_beds_psh",
        ],
    }

    rows = []
    for _, row in hic_df.iterrows():
        coc = row.get("coc_number") if pd.notna(row.get("coc_number")) else row.get("coc")
        new_row = {"coc_number": coc, "year": row["year"]}
        for std_name, candidates in MAPPINGS.items():
            val = None
            for c in candidates:
                if c in hic_df.columns and pd.notna(row.get(c)):
                    val = row[c]
                    break
            new_row[std_name] = val
        rows.append(new_row)

    df = pd.DataFrame(rows)
    # Reorder columns
    col_order = ["coc_number", "year"] + [k for k in MAPPINGS.keys()]
    df = df[[c for c in col_order if c in df.columns]]

    out_path = os.path.join(PROCESSED_DIR, "hic_core.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path} ({len(df):,} rows, {len(df.columns)} columns)")
    return df


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    pit = compile_pit_by_coc()
    hic = compile_hic_by_coc()
    compile_pit_core(pit)
    compile_hic_core(hic)
    print("\nDone. Processed files are in data/processed/")


if __name__ == "__main__":
    main()
