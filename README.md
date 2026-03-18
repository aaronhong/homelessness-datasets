# Homelessness Datasets

National aggregation of HUD Point-in-Time (PIT) counts and Housing Inventory Count (HIC) data at the Continuum of Care (CoC) level, compiled from all available years (2007–2024).

## Data Sources

- **PIT & HIC** — HUD User: [2024 AHAR Part 1](https://www.huduser.gov/portal/datasets/ahar/2024-ahar-part-1-pit-estimates-of-homelessness-in-the-us.html)

## Structure

```
data/
├── raw/          # Raw Excel files downloaded from HUD (not tracked in git)
│   ├── pit/
│   ├── hic/
│   └── other/
└── processed/    # Cleaned, compiled CSVs (tracked in git)
    ├── pit_by_coc.csv   — full PIT panel, all variables
    ├── pit_core.csv     — PIT core variables, all years (use for longitudinal analysis)
    ├── hic_by_coc.csv   — full HIC panel, all variables
    ├── hic_core.csv     — HIC core variables, harmonized across all years
    └── other/

scripts/
├── download.py   # Downloads all raw Excel files from HUD User
└── compile.py    # Compiles, cleans, and outputs all processed files

output/           # Analysis outputs
```

## Reproducing the Data

```bash
pip install -r requirements.txt
python scripts/download.py
python scripts/compile.py
```

---

## Processed Files

### For longitudinal analysis (recommended starting point)

| File | Rows | Columns | Years | Description |
|---|---|---|---|---|
| `pit_core.csv` | 6,923 | 26 | 2007–2024 | PIT core variables consistent across all years |
| `hic_core.csv` | 7,450 | 11 | 2007–2024 | HIC bed counts by program type, harmonized across all years |

### Full panels (all variables)

| File | Rows | Columns | Years | Description |
|---|---|---|---|---|
| `pit_by_coc.csv` | 6,923 | 1,409 | 2007–2024 | All PIT variables (many are year-specific) |
| `hic_by_coc.csv` | 7,450 | 167 | 2007–2024 | All HIC variables (naming varies by era) |

---

## PIT — Variable Availability

Variables are **not fully harmonized across all years**. Use `pit_core.csv` for full 2007–2024 panel analysis.

### Core variables (available in all years — `pit_core.csv`)
```
coc_number, coc_name, year
overall_homeless
overall_homeless_individuals
overall_homeless_people_in_families
overall_homeless_family_households
overall_chronically_homeless_individuals
sheltered_es_homeless
sheltered_es_homeless_individuals
sheltered_es_homeless_people_in_families
sheltered_es_homeless_family_households
sheltered_th_homeless
sheltered_th_homeless_individuals
sheltered_th_homeless_people_in_families
sheltered_th_homeless_family_households
sheltered_total_homeless
sheltered_total_homeless_individuals
sheltered_total_homeless_people_in_families
sheltered_total_homeless_family_households
sheltered_total_chronically_homeless_individuals
unsheltered_homeless
unsheltered_homeless_individuals
unsheltered_homeless_people_in_families
unsheltered_homeless_family_households
unsheltered_chronically_homeless_individuals
```

### Additional variables by first year available

| First available | Variable group |
|---|---|
| 2009 | `sheltered_es_chronically_homeless_individuals` |
| 2010 | Safe Haven (SH) shelter type: `sheltered_sh_homeless`, `sheltered_sh_homeless_individuals`, `sheltered_sh_chronically_*` |
| 2011 | Veterans: `overall_homeless_veterans`, `sheltered_*_homeless_veterans`, `unsheltered_homeless_veterans`; Youth under 18: `overall_homeless_individuals_under_18`, `sheltered_*_homeless_individuals_under_18` |
| 2013 | Age brackets: `*_under_18`, `*_age_18_to_24`, `*_over_24` |
| 2014 | Race: `*_white`, `*_black_african_american_or_african`, `*_hispanic_latina_e_o`, `*_american_indian_alaska_native_or_indigenous`, `*_asian_or_asian_american`, `*_native_hawaiian_or_other_pacific_islander`, `*_multi_racial`; Gender: `*_woman`, `*_man`, `*_transgender` |
| 2015 | Unaccompanied and parenting youth: `*_unaccompanied_youth_under_25`, `*_parenting_youth_under_25`, `*_children_of_parenting_youth` |
| 2016 | Race × gender breakdowns for youth subgroups |
| 2017 | Non-binary gender: `*_non_binary` |
| 2022 | Gender questioning: `*_gender_questioning` |
| 2023 | Expanded age brackets: `*_age_25_to_34`, `*_age_35_to_44`, `*_age_45_to_54`, `*_age_55_to_64`, `*_over_64` |
| 2024 | Race × ethnicity intersections (e.g., `*_black_african_american_or_african_and_hispanic_latina_e_o`); new gender categories: `*_culturally_specific_identity`, `*_different_identity`, `*_more_than_one_gender`; new race: `*_middle_eastern_or_north_african` |

---

## HIC — Variable Availability

Variable names changed substantially across eras. Use `hic_core.csv` for full 2007–2024 panel analysis.

### Core variables (harmonized across all years — `hic_core.csv`)

| Variable | Years available | Description |
|---|---|---|
| `coc_number` | 2007–2024 | Continuum of Care identifier |
| `year` | 2007–2024 | Survey year |
| `total_year_round_beds_es` | 2007–2024 | Emergency Shelter year-round beds |
| `total_year_round_beds_th` | 2007–2024 | Transitional Housing year-round beds |
| `total_year_round_beds_psh` | 2007–2024 | Permanent Supportive Housing year-round beds |
| `total_year_round_beds_sh` | 2008–2024 | Safe Haven year-round beds |
| `total_year_round_beds_rrh` | 2013–2024 | Rapid Re-Housing year-round beds |
| `total_year_round_beds_oph` | 2014–2024 | Other Permanent Housing year-round beds |
| `total_seasonal_beds_es` | 2007–2024 | Emergency Shelter seasonal beds |
| `total_overflow_beds_es` | 2007–2024 | Emergency Shelter overflow/voucher beds |
| `total_chronic_homeless_beds_psh` | 2007–2013, 2017–2024 | PSH beds dedicated to chronically homeless |

### Full HIC variable list (in `hic_by_coc.csv`)

The full panel has 167 columns. Variable names follow the pattern `[measure]_[program_type]`, e.g.:

```
total_year_round_beds_[es|th|sh|rrh|psh|oph|es_th_sh]
total_non_dv_year_round_beds_[program]
total_hmis_year_round_beds_[program]
hmis_participation_rate_for_year_round_beds_[program]
total_seasonal_beds_es
total_overflow_beds_es
total_units_for_households_with_children_[program]
total_beds_for_households_with_children_[program]
total_beds_for_households_without_children_[program]
total_beds_for_households_with_only_children_[program]
dedicated_veteran_beds_[program]        (2017+)
dedicated_youth_beds_[program]          (2017+)
dedicated_chronically_homeless_beds_psh (2017+)
```

---

## Abbreviations

| Abbreviation | Meaning |
|---|---|
| ES | Emergency Shelter |
| TH | Transitional Housing |
| SH | Safe Haven |
| PSH | Permanent Supportive Housing |
| RRH | Rapid Re-Housing |
| OPH | Other Permanent Housing |
| DV | Domestic Violence |
| HMIS | Homeless Management Information System |
| CoC | Continuum of Care |
| PIT | Point-in-Time count |
| HIC | Housing Inventory Count |
