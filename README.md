# Homelessness Datasets

National aggregation of HUD Point-in-Time (PIT) counts and Housing Inventory Count (HIC) data at the Continuum of Care (CoC) level, compiled from all available years (2007–2024).

## Data Sources

- **PIT Counts** — HUD User: [2024 AHAR Part 1](https://www.huduser.gov/portal/datasets/ahar/2024-ahar-part-1-pit-estimates-of-homelessness-in-the-us.html)
- **HIC** — HUD User: [2024 AHAR Part 1](https://www.huduser.gov/portal/datasets/ahar/2024-ahar-part-1-pit-estimates-of-homelessness-in-the-us.html)

## Structure

```
data/
├── raw/          # Raw Excel files downloaded from HUD (not tracked in git)
│   ├── pit/
│   ├── hic/
│   └── other/
└── processed/    # Cleaned, compiled CSVs (tracked in git)
    └── other/

scripts/
├── download.py   # Downloads all PIT and HIC Excel files from HUD User
└── compile.py    # Standardizes and merges all years into compiled CSVs

output/           # Analysis outputs (figures, tables, reports)
```

## Reproducing the Data

```bash
pip install -r requirements.txt
python scripts/download.py
python scripts/compile.py
```

---

## PIT — `data/processed/pit_by_coc.csv`

**6,923 rows** | Unit of analysis: CoC × year | Years: 2007–2024

Key columns: `coc_number`, `coc_name`, `year`, plus count variables below.

### Variable Availability by Year

Variables are **not fully harmonized across years** — HUD has expanded the data collection over time. The table below shows the first year each variable group becomes available.

#### Available from 2007 (23 variables) — core longitudinal variables
```
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

#### Available from 2009 (2 variables)
```
count_types
sheltered_es_chronically_homeless_individuals
```

#### Available from 2010 (4 variables) — Safe Haven (SH) shelter type added
```
sheltered_sh_homeless
sheltered_sh_homeless_individuals
sheltered_sh_chronically_homeless
sheltered_sh_chronically_homeless_individuals
```

#### Available from 2011 (16 variables) — veterans and youth under 18 added
```
overall_chronically_homeless
overall_chronically_homeless_people_in_families
overall_homeless_veterans
overall_homeless_individuals_under_18
sheltered_es_chronically_homeless
sheltered_es_chronically_homeless_people_in_families
sheltered_es_homeless_individuals_under_18
sheltered_th_homeless_individuals_under_18
sheltered_th_chronically_homeless (via sheltered_total)
sheltered_total_chronically_homeless
sheltered_total_chronically_homeless_people_in_families
sheltered_total_homeless_individuals_under_18
sheltered_total_homeless_veterans
unsheltered_chronically_homeless
unsheltered_chronically_homeless_people_in_families
unsheltered_homeless_individuals_under_18
unsheltered_homeless_veterans
```

#### Available from 2013 (47 variables) — age breakdowns added
```
overall_homeless_under_18
overall_homeless_age_18_to_24
overall_homeless_over_24
overall_homeless_people_in_families_under_18
overall_homeless_people_in_families_age_18_to_24
overall_homeless_people_in_families_over_24
overall_homeless_individuals_age_18_to_24
overall_homeless_individuals_over_24
overall_homeless_veterans_woman
... (and sheltered_es, sheltered_sh, sheltered_th, sheltered_total, unsheltered variants)
```

#### Available from 2014 (253 variables) — race and gender breakdowns added
```
overall_homeless_woman
overall_homeless_man
overall_homeless_transgender
overall_homeless_white
overall_homeless_black_african_american_or_african
overall_homeless_hispanic_latina_e_o
overall_homeless_non_hispanic_latina_e_o
overall_homeless_american_indian_alaska_native_or_indigenous
overall_homeless_asian_or_asian_american
overall_homeless_native_hawaiian_or_other_pacific_islander
overall_homeless_multi_racial
... (and all variants by shelter type, individuals, people_in_families, veterans)
```

#### Available from 2015 (38 variables) — parenting and unaccompanied youth added
```
overall_homeless_unaccompanied_youth_under_18
overall_homeless_unaccompanied_youth_age_18_24
overall_homeless_unaccompanied_youth_under_25
overall_homeless_parenting_youth_under_18
overall_homeless_parenting_youth_age_18_24
overall_homeless_parenting_youth_under_25
overall_homeless_children_of_parenting_youth
... (and sheltered/unsheltered variants)
```

#### Available from 2016 (121 variables) — race/gender breakdowns for youth added
```
overall_homeless_unaccompanied_youth_under_25_[race/gender]
overall_homeless_parenting_youth_under_25_[race/gender]
... (and sheltered/unsheltered variants)
```

#### Available from 2017 (36 variables) — non-binary gender added
```
overall_homeless_non_binary
overall_homeless_individuals_non_binary
overall_homeless_people_in_families_non_binary
overall_homeless_veterans_non_binary
... (and sheltered/unsheltered variants)
```

#### Available from 2022 (34 variables) — gender questioning added
```
overall_homeless_gender_questioning
overall_homeless_individuals_gender_questioning
overall_homeless_veterans_gender_questioning
... (and sheltered/unsheltered variants)
```

#### Available from 2023 (85 variables) — expanded age brackets added
```
overall_homeless_age_25_to_34
overall_homeless_age_35_to_44
overall_homeless_age_45_to_54
overall_homeless_age_55_to_64
overall_homeless_over_64
... (and sheltered/unsheltered variants by individuals, people_in_families)
```

#### Available from 2024 (647 variables) — detailed race × ethnicity intersections added
```
overall_homeless_american_indian_alaska_native_or_indigenous_only
overall_homeless_american_indian_alaska_native_or_indigenous_and_hispanic_latina_e_o
overall_homeless_black_african_american_or_african_only
overall_homeless_black_african_american_or_african_and_hispanic_latina_e_o
overall_homeless_middle_eastern_or_north_african (new race category)
overall_homeless_culturally_specific_identity (new gender category)
overall_homeless_different_identity (new gender category)
overall_homeless_more_than_one_gender (new gender category)
... (and all variants)
```

---

## HIC — `data/processed/hic_by_coc.csv`

**7,469 rows** | Unit of analysis: CoC × year | Years: 2007–2024

Key columns: `coc_number`, `coc_name`, `year`, plus bed/unit counts below.

> **Note:** The HIC Excel files use multi-level column headers which result in some `unnamed` columns in the compiled CSV. These correspond to sub-columns within program type tables. Improved parsing of the HIC file structure is a known issue.

### Variable Availability by Year

#### Available from 2007 (4 named variables)
```
emergency_shelter_es
transitional_housing_th
permanent_supportive_housing_psh
total_beds_esth
```

#### Available from 2008 (2 named variables) — Safe Haven added
```
safe_haven_sh
total_beds_esthsh
```

#### Available from 2013 (1 named variable) — Rapid Re-Housing added
```
rapid_rehousing_rrh
```

#### Available from 2014 (5 named variables) — additional program types added
```
other_permanent_housing_oph
rapid_re_housing_excluding_demonstration_programs
rapid_re_housing_demonstration_projects_dem
total_rapid_re_housing_including_demonstration_programs
total_beds_es_th_sh
```

#### Available from 2017 (1 named variable)
```
rapid_re_housing_rrh  (renamed/restructured from earlier version)
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
| CoC | Continuum of Care |
| PIT | Point-in-Time count |
| HIC | Housing Inventory Count |
