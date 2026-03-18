# Homelessness Datasets

National aggregation of HUD Point-in-Time (PIT) counts and Housing Inventory Count (HIC) data at the Continuum of Care (CoC) level, compiled from all available years.

## Data Sources

- **PIT Counts** — HUD Exchange annual Point-in-Time count estimates by CoC
- **HIC** — HUD Exchange annual Housing Inventory Count by CoC
- **Other** — Additional homelessness-related datasets as collected

## Structure

```
data/
├── raw/          # Raw Excel files downloaded from HUD (not tracked in git)
│   ├── pit/      # PIT Excel files by year
│   ├── hic/      # HIC Excel files by year
│   └── other/    # Other raw datasets
└── processed/    # Cleaned, standardized, compiled CSVs (tracked in git)
    └── other/

scripts/
├── download.py   # Downloads all PIT and HIC Excel files from HUD Exchange
└── compile.py    # Standardizes and merges all years into compiled CSVs

output/           # Analysis outputs (figures, tables, reports)
```

## Reproducing the Data

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download all raw files:
   ```bash
   python scripts/download.py
   ```

3. Compile and standardize:
   ```bash
   python scripts/compile.py
   ```

Processed files will be saved to `data/processed/`.

## Coverage

- **Geography:** All U.S. Continuums of Care (CoCs)
- **Years:** All available years from HUD Exchange
- **Unit of analysis:** CoC-year

## Notes

Raw Excel files are not tracked in git — run `download.py` to regenerate them locally.
