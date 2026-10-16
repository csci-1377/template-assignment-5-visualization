# Assignment 5: Tidy Tuesday Datasets

## Read First

For Part D of Assignment 5, we’ve asked you to act as a data journalist and ask/answer a question with a visualization. Here, you’ll find 10 sample datasets from the Tidy Tuesday weekly data science challenge. Each dataset is provided with a description, a link to the original GitHub page for that week, a table of columns in the dataset, and a script to pull in the data and tidy it up. Each script downloads its files into `data/<dataset_name>`, so run it from the root of the repository. **Note that the given column formats are post-tidying and may differ from the raw dataset, and that even tidied datasets can have aberrations you'll have to work around.**

For your question, you can make up your own or choose from any of the sample questions. Creative questions will earn some extra credit!

## Working With Large Datasets

Altair refuses to render any dataframe over 5,000 rows to keep you from unknowingly shipping a huge chart spec to the browser. Some of the datasets below are larger than that. Run this once, before you plot, and Altair will hand the data off to VegaFusion instead of embedding it:

```python
import altair as alt

alt.data_transformers.enable('vegafusion')
```

Note that some of these datasets are VERY large (namely the repair cafes dataset). If they feel slow or are hard to work with, consider aggregating parts of data both in your preprocessing (for ease of use) and in your representation (for fidelity). We have decided to let _you_ handle this part
because working with and understanding how to represent big data is an important part of data journalism.

## 1. Measles Cases Across the World

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-06-24/readme.md 

Description: A dataset of provisional measles and rubella cases across the world, downloaded from the World Health Organization as of 2025-06-12.

Sample Questions:

- How have global measles cases changed over time?
- Which regions or countries consistently report the highest measles burden?
- Are there seasonal patterns in measles outbreaks across different regions?
- Does the ratio of laboratory-confirmed cases to total cases reveal differences in healthcare capacity across countries?

Format:

`cases_month`

| variable | class | description |
| --- | --- | --- |
| region | str | Region name. |
| country | str | Country name. |
| iso3 | str | Three letter country code. |
| year | float64 | Year. |
| month | float64 | Month. |
| measles_suspect | float64 | Suspected measles cases. |
| measles_clinical | float64 | Clinically-compatible measles cases. |
| measles_epi_linked | float64 | Epidemiologically-linked measles cases. |
| measles_lab_confirmed | float64 | Laboratory-confirmed measles cases. |
| measles_total | float64 | Total measles cases: the sum of clinically-compatible, epidemiologically linked and laboratory-confirmed cases. |
| rubella_clinical | float64 | Clinically-compatible rubella cases. |
| rubella_epi_linked | float64 | Epidemiologically-linked rubella cases. |
| rubella_lab_confirmed | float64 | Laboratory-confirmed rubella cases. |
| rubella_total | float64 | Total rubella cases. |
| discarded | float64 | Discarded cases: a suspected case that has been investigated and discarded as non-measles (and non-rubella). |
| date | datetime64 | First of the month, constructed from year and month (e.g. 2024-03-01). |

`cases_year`

| variable | class | description |
| --- | --- | --- |
| region | str | Region name. |
| country | str | Country name. |
| iso3 | str | Three letter country code. |
| year | float64 | Year. |
| total_population | float64 | Country population. |
| annualized_population_most_recent_year_only | float64 | Annualized population 2025. |
| total_suspected_measles_rubella_cases | float64 | Suspected measles/rubella cases. |
| measles_total | float64 | Total measles cases. |
| measles_lab_confirmed | float64 | Laboratory-confirmed measles cases. |
| measles_epi_linked | float64 | Epidemiologically-linked measles cases. |
| measles_clinical | float64 | Clinically-compatible measles cases. |
| measles_incidence_rate_per_1000000_total_population | float64 | Measles cases per million population. |
| rubella_total | float64 | Total rubella cases. |
| rubella_lab_confirmed | float64 | Laboratory-confirmed rubella cases. |
| rubella_epi_linked | float64 | Epidemiologically-linked rubella cases. |
| rubella_clinical | float64 | Clinically-compatible rubella cases. |
| rubella_incidence_rate_per_1000000_total_population | float64 | Rubella cases per million population. |
| discarded_cases | float64 | Discarded cases. |
| discarded_non_measles_rubella_cases_per_100000_total_population | float64 | Discarded cases per million population. |

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'measles')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2025-06-24')
finally:
    os.chdir(cwd)

cases_month = pd.read_csv(os.path.join(data_dir, 'cases_month.csv'))
cases_year = pd.read_csv(os.path.join(data_dir, 'cases_year.csv'))
num_cols = ['measles_suspect', 'measles_clinical', 'measles_epi_linked',
            'measles_lab_confirmed', 'measles_total', 'rubella_clinical',
            'rubella_epi_linked', 'rubella_lab_confirmed', 'rubella_total', 'discarded']
for col in num_cols:
    cases_month[col] = pd.to_numeric(cases_month[col], errors='coerce')
cases_month['date'] = pd.to_datetime(
    cases_month['year'].astype(str) + '-' + cases_month['month'].astype(str) + '-01'
)
year_num_cols = [c for c in cases_year.columns if c not in ['region', 'country', 'iso3', 'year']]
for col in year_num_cols:
    cases_year[col] = pd.to_numeric(cases_year[col], errors='coerce')
cases_year['year'] = pd.to_numeric(cases_year['year'], errors='coerce')
```

## 2. Salmonid Mortality Data

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-03-17/readme.md 

Description: Monthly mortality and losses data for Norwegian farmed salmonids, published by the Norwegian Veterinary Institute via the Laksetap Shiny App and API, with data available from 2020.

Sample Questions:

- How does monthly mortality differ across the time period data is available for?
- Which region has lowest mortality?
- What other types of losses may be significant in addition to death of fish?

Format:

`monthly_losses`

| variable | class | description |
| --- | --- | --- |
| species | str | The species of fish. |
| date | datetime64 | The month for the observation. |
| geo_group | str | Country, county or area level for the data. |
| region | str | The name of the geo_group. |
| losses | float64 | Total number of fish losses. |
| dead | float64 | Number of dead fish. |
| discarded | float64 | Number of discarded fish. |
| escaped | float64 | Number of escaped fish. |
| other | float64 | Number of other losses. |

`monthly_mortality`

| variable | class | description |
| --- | --- | --- |
| species | str | The species of fish. |
| date | datetime64 | The month for the observation. |
| geo_group | str | Country, county or area level for the data. |
| region | str | The name of the geo_group. |
| median | float64 | Median mortality. |
| q1 | float64 | Lower quartile. |
| q3 | float64 | Upper quartile. |

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'salmonids')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-03-17')
finally:
    os.chdir(cwd)

monthly_losses = pd.read_csv(os.path.join(data_dir, 'monthly_losses_data.csv'))
monthly_mortality = pd.read_csv(os.path.join(data_dir, 'monthly_mortality_data.csv'))
monthly_losses['date'] = pd.to_datetime(monthly_losses['date'])
monthly_mortality['date'] = pd.to_datetime(monthly_mortality['date'])
for col in ['losses', 'dead', 'discarded', 'escaped', 'other']:
    monthly_losses[col] = pd.to_numeric(monthly_losses[col], errors='coerce')

for col in ['median', 'q1', 'q3']:
    monthly_mortality[col] = pd.to_numeric(monthly_mortality[col], errors='coerce')
```

## 3. Wreck Inventory of Ireland

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-06-30/readme.md 

Description: The Wreck Inventory of Ireland Database (WIID) holds records of over 18,000 known and potential wreck sites in the marine and inland waterways of Ireland, including all known wrecks dating to pre-1946.

Sample Questions:

- How many wrecks still have not been found?
- Where are shipwrecks more likely to occur around Ireland?

Format:

`wrecks`

| variable | class | description |
| --- | --- | --- |
| date | datetime64 | Standardised date of the shipwreck event, where an exact date could be determined; NaT otherwise. |
| year | float64 | Calendar year of the shipwreck event (but see descriptive_date). |
| wreck_name | str | Recorded name of the wrecked vessel. |
| wreck_no | str | Unique identifier assigned to the shipwreck record. |
| classification | str | Vessel type or classification. |
| description | str | Historical description of the vessel. |
| descriptive_date | str | Original date information as recorded in the source material, including approximate or uncertain dates. |
| place_of_loss | str | Recorded location where the vessel was lost. |
| latitude | float64 | Latitude of the shipwreck location; NaN where unknown. |
| longitude | float64 | Longitude of the shipwreck location; NaN where unknown. |
| source_of_co_ordinate | str | Source or method used to obtain the geographic coordinates. |
| location_known | bool | True if both latitude and longitude are present; False otherwise. Derived column. |

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'wrecks')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-06-30')
finally:
    os.chdir(cwd)

wrecks = pd.read_csv(os.path.join(data_dir, 'wreck_inventory.csv'))
wrecks['date'] = pd.to_datetime(wrecks['date'], errors='coerce')
wrecks['year'] = pd.to_numeric(wrecks['year'], errors='coerce')
wrecks['latitude'] = pd.to_numeric(wrecks['latitude'], errors='coerce')
wrecks['longitude'] = pd.to_numeric(wrecks['longitude'], errors='coerce')
wrecks['location_known'] = wrecks['latitude'].notna() & wrecks['longitude'].notna()
```

## 4. Many Penguins (Penguin Morphology)

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-07-14/readme.md 

Description: Morphometric data for 93 penguins from 18 species within 6 genera, drawn from the AVONET database of comprehensive functional trait data for all birds (Tobias et al. 2022).

Sample Questions:

- How do trait values covary within/across species and genera?
- Is there a good way to do ordination/visualization that handles the missingness of some of the traits nicely?
- Are there interesting ways to visualize these data in >2 dimensions?

Format:

`penguins`

| variable | class | description |
| --- | --- | --- |
| species | category | Penguin species name. |
| genus | category | Penguin genus name. |
| shortname | category | Abbreviated species name. |
| sex | category | Sex of the individual sampled: M = Male; F = Female; U = Unknown. |
| beak.length_culmen | float64 | Length from the tip of the beak to the base of the skull (mm). |
| beak.length_nares | float64 | Length from the anterior edge of the nostrils to the tip of the beak (mm). |
| beak.width | float64 | Width of the beak at the anterior edge of the nostrils (mm). |
| beak.depth | float64 | Depth of the beak at the anterior edge of the nostrils (mm). |
| tarsus.length | float64 | Length of the tarsus from the posterior notch between tibia and tarsus (mm). |
| wing.length | float64 | Length from the carpal joint to the tip of the longest primary on the unflattened wing (mm). |
| kipps.distance | float64 | Length from the tip of the first secondary feather to the tip of the longest primary (mm). |
| secondary1 | float64 | Length from the carpal joint to the tip of the first secondary (mm). |
| hand-wing.index | float64 | 100*DK/Lw, where DK is Kipp's distance and Lw is wing length (mm). |
| tail.length | float64 | Distance between the tip of the longest rectrix and the point at which the two central rectrices protrude from the skin (mm). |

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'penguins')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-07-14')
finally:
    os.chdir(cwd)

penguins = pd.read_csv(os.path.join(data_dir, 'many_penguins.csv'))
for col in ['species', 'genus', 'shortname', 'sex']:
    penguins[col] = penguins[col].astype('category')
morph_cols = ['beak.length_culmen', 'beak.length_nares', 'beak.width',
              'beak.depth', 'tarsus.length', 'wing.length', 'kipps.distance',
              'secondary1', 'hand-wing.index', 'tail.length']
for col in morph_cols:
    penguins[col] = pd.to_numeric(penguins[col], errors='coerce')
```

## 5. Sustainable Energy for All

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-05-26/readme.md 

Description: Country-level historical data from the UN SE4ALL initiative tracking access to electricity and non-solid fuel, share of renewable energy in total final energy consumption by technology, and energy intensity rate of improvement.

Sample Questions:

- Which countries have the lowest capacity for solar energy?
- What form of renewable energy has, on average, experienced the fastest rate of adoption?

Format:

`energy`

| variable | class | description |
| --- | --- | --- |
| country_name | str | Name of country. |
| country_code | str | Three-letter ISO country code. |
| yr | Int64 | The year. |
| access_non_solid_fuel_rural_pop_pct | float64 | Percentage of rural population with access to Non-Solid fuel. |
| access_non_solid_fuel_total_pop_pct | float64 | Percentage of total population with access to Non-Solid fuel. |
| access_non_solid_fuel_urban_pop_pct | float64 | Percentage of urban population with access to Non-Solid fuel. |
| access_electricity_rural_pop_pct | float64 | Percentage of rural population with access to electricity. |
| access_electricity_total_pop_pct | float64 | Percentage of total population with access to electricity. |
| access_electricity_urban_pop_pct | float64 | Percentage of urban population with access to electricity. |
| biogas_consumption_tfec_pct | float64 | Percentage of Biogas in total final energy consumption. |
| biogas_consumption_terajoules | float64 | Terajoules of Biogas energy consumed. |
| divisia_decomp_analysis_activity_component_index | float64 | Changes in energy use caused by the size of the economy. |
| divisia_decomp_analysis_energy_intensity_component_index | float64 | Changes caused by efficiency. |
| divisia_decomp_analysis_structure_component_index | float64 | Changes caused by shifts in the economy. |
| energy_intensity_level_final_energy_megajoules_per_usd_2005_ppp | float64 | Final energy MJ per 2005 USD PPP. |
| energy_intensity_level_primary_energy_megajoules_per_usd_2005_ppp | float64 | Primary energy MJ per 2005 USD PPP. |
| energy_intensity_agricultural_sector_megajoules_per_usd_2005 | float64 | MJ per 2005 USD for agricultural sector. |
| energy_intensity_industrial_sector_megajoules_per_usd_2005 | float64 | MJ per 2005 USD for industrial sector. |
| energy_intensity_other_sectors_megajoules_per_usd_2005 | float64 | MJ per 2005 USD for other sectors. |
| energy_savings_primary_energy_terajoules | float64 | Terajoules of primary energy savings. |
| final_to_primary_energy_ratio_pct | float64 | Percentage ratio of final energy to primary energy. |
| geothermal_energy_consumption_tfec_pct | float64 | Percentage of Geothermal in TFEC. |
| geothermal_energy_consumption_terajoules | float64 | Terajoules of Geothermal energy consumed. |
| hydro_energy_consumption_tfec_pct | float64 | Percentage of Hydro in TFEC. |
| hydro_energy_consumption_terajoules | float64 | Terajoules of Hydro energy consumed. |
| liquid_biofuels_energy_consumption_tfec_pct | float64 | Percentage of Liquid biofuels in TFEC. |
| liquid_biofuels_consumption_terajoules | float64 | Terajoules of Liquid biofuels consumed. |
| marine_energy_consumption_tfec_pct | float64 | Percentage of Marine energy in TFEC. |
| marine_consumption_terajoules | float64 | Terajoules of Marine energy consumed. |
| modern_biomass_energy_consumption_tfec_pct | float64 | Percentage of Modern biomass in TFEC. |
| modern_biomass_consumption_terajoules | float64 | Terajoules of Modern biomass consumed. |
| perc_renewable_of_total_electricity_output | float64 | Renewable energy percentage of total electricity output. |
| renewable_energy_consumption_terajoules | float64 | Terajoules of Renewable energy consumed. |
| renewable_energy_consumption_tfec_pct | float64 | Percentage of Renewable energy in TFEC. |
| renewable_energy_electricity_output_gigawatt_hours | float64 | Renewable energy output in GWh. |
| renewable_energy_installed_capacity_gigawatts | float64 | Renewable energy installed capacity in GW. |
| share_of_renewable_capacity_in_total_capacity_pct | float64 | Percentage share of installed capacity of Renewable energy. |
| solar_energy_consumption_tfec_pct | float64 | Percentage of Solar in TFEC. |
| solar_energy_consumption_terajoules | float64 | Terajoules of Solar energy consumed. |
| thermal_efficiency_in_power_supply_pct | float64 | Percentage of Thermal efficiency in power supply. |
| total_electricity_output_gigawatt_hours | float64 | Total electricity output in GWh. |
| total_final_consumption_terajoules | float64 | Terajoules of Total final energy consumed. |
| total_final_energy_consumption_tfec | float64 | Total final energy consumed (TFEC). |
| total_installed_generation_capacity_gigawatts | float64 | Total installed generation capacity in GW. |
| total_primary_energy_supply_terajoules | float64 | Terajoules of Total primary energy supply. |
| traditional_biomass_consumption_tfec_pct | float64 | Percentage of Traditional biomass in TFEC. |
| traditional_biomass_consumption_terajoules | float64 | Terajoules of Traditional biomass consumed. |
| transmission_and_distribution_losses_pct | float64 | Percentage of power lost in transmission and distribution. |
| waste_energy_consumption_tfec_pct | float64 | Percentage of Waste energy in TFEC. |
| waste_energy_consumption_terajoules | float64 | Terajoules of Waste energy consumed. |
| wind_energy_consumption_tfec_pct | float64 | Percentage of Wind energy in TFEC. |
| wind_energy_consumption_terajoules | float64 | Terajoules of Wind energy consumed. |

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'energy')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-05-26')
finally:
    os.chdir(cwd)

energy = pd.read_csv(os.path.join(data_dir, 'energy_cleaned.csv'))
energy['yr'] = pd.to_numeric(energy['yr'], errors='coerce').astype('Int64')
id_cols = ['country_name', 'country_code', 'yr']
for col in energy.columns:
    if col not in id_cols:
        energy[col] = pd.to_numeric(energy[col], errors='coerce')
```

## 6. The Palomar Spectroscopic Survey of Nearby Galaxies

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-08-11/readme.md 

Description: Spectroscopic observations of 486 nearby galaxies from the Palomar survey, classifying each galaxy's nucleus as powered by young stars, an active galactic nucleus (AGN), or a combination, based on emission-line measurements from the 200-inch Hale Telescope.

Sample Questions:

- What types of nuclear activity are most common, and how does that vary with galaxy morphology (spirals vs. ellipticals)?
- Can you recreate the classic BPT diagnostic diagram using the emission-line ratios? Where do the different activity types fall?
- Is there a relationship between a galaxy's velocity dispersion (a proxy for central mass) and the type of nuclear activity it hosts?
- Which galaxy morphological types are most likely to host Seyfert nuclei vs. LINERs?

Format:

`emission`

| variable | class | description |
| --- | --- | --- |
| galaxy_name | str | Common name of the galaxy. Can be joined with the survey dataset. |
| h_gamma | float64 | H-gamma (4340 Å) line intensity relative to H-alpha (= 1.0). |
| h_beta | float64 | H-beta (4861 Å) line intensity relative to H-alpha (= 1.0). Fundamental reference line for emission-line diagnostics. |
| oiii_5007 | float64 | [O III] 5007 Å forbidden line intensity relative to H-alpha. Strongest line from doubly-ionized oxygen. |
| oi_6300 | float64 | [O I] 6300 Å forbidden line intensity relative to H-alpha. Enhanced in shocks and LINER nuclei. |
| nii_6583 | float64 | [N II] 6583 Å forbidden line intensity relative to H-alpha. Key line in BPT classification diagrams. |
| sii_6716 | float64 | [S II] 6716 Å forbidden line intensity relative to H-alpha. One member of the sulfur doublet. |
| sii_6731 | float64 | [S II] 6731 Å forbidden line intensity relative to H-alpha. The 6716/6731 ratio is density-sensitive. |

`survey`

| variable | class | description |
| --- | --- | --- |
| galaxy_name | str | Common name of the galaxy (e.g. "NGC 224", "IC 342"). |
| hubble_type | str | Morphological type in the Hubble sequence (e.g. "Sb", "E2", "SBc"). |
| b_magnitude | float64 | Apparent blue (B-band) magnitude, uncorrected for extinction. |
| helio_velocity_km_s | float64 | Heliocentric radial velocity in km/s. |
| ra_j2000 | str | Right ascension in J2000 coordinates. |
| dec_j2000 | str | Declination in J2000 coordinates. |
| ha_hb_ratio | float64 | Observed H-alpha to H-beta intensity ratio. Theoretical value for pure hydrogen gas is 2.86; higher values indicate dust reddening. |
| internal_reddening_ebv | float64 | Internal color excess E(B-V) derived from the H-alpha/H-beta ratio. |
| sii_density_ratio | float64 | Ratio of [S II] 6716 to [S II] 6731 line intensities. Used to estimate electron density. |
| electron_density_cm3 | float64 | Electron density in particles per cubic centimeter. |
| log_oiii_hb | float64 | Dereddened [O III] 5007 / H-beta intensity ratio. Used on the y-axis of BPT diagrams. |
| log_oi_ha | float64 | Dereddened [O I] 6300 / H-alpha intensity ratio. |
| log_nii_ha | float64 | Dereddened [N II] 6583 / H-alpha intensity ratio. Primary x-axis of the classic BPT diagram. |
| log_sii_ha | float64 | Dereddened [S II] (6716+6731) / H-alpha intensity ratio. |
| spectral_class | str | Nuclear spectral classification code (e.g. "S1.9", "L2", "T2:", "H"). |
| activity_type | category | Simplified nuclear activity classification: "Seyfert", "LINER", "Transition", "H II", or "Absorption". |
| activity_subtype | float64 | Numeric subtype (1 or 2). Type 1 shows broad emission lines; type 2 shows only narrow lines. |
| classification_confidence | str | Confidence level: "confident", "uncertain", or "very uncertain". |
| velocity_dispersion_km_s | float64 | Adopted central stellar velocity dispersion in km/s. |
| velocity_dispersion_error | float64 | Measurement uncertainty on the velocity dispersion in km/s. |

`galaxies` (merged)

The script also produces a merged dataframe `galaxies = survey.merge(emission, on='galaxy_name', how='left')` that combines all columns from both tables above, joined on `galaxy_name`.

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'galaxies')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-08-11')
finally:
    os.chdir(cwd)

survey = pd.read_csv(os.path.join(data_dir, 'palomar_survey.csv'))
emission = pd.read_csv(os.path.join(data_dir, 'palomar_emission_lines.csv'))

survey['activity_type'] = survey['activity_type'].astype('category')
num_survey = ['b_magnitude', 'helio_velocity_km_s', 'ha_hb_ratio',
              'internal_reddening_ebv', 'sii_density_ratio', 'electron_density_cm3',
              'log_oiii_hb', 'log_oi_ha', 'log_nii_ha', 'log_sii_ha',
              'velocity_dispersion_km_s', 'velocity_dispersion_error']
for col in num_survey:
    survey[col] = pd.to_numeric(survey[col], errors='coerce')
galaxies = survey.merge(emission, on='galaxy_name', how='left')
```

## 7. Twinned Cities

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-05-12/readme.md 

Description: Data about twinned (sister) city links worldwide, covering legal or social agreements between geographically distinct cities for the purpose of promoting cultural and commercial ties.

Sample Questions:

- Is every country connected through a chain of twin city links?
- Which city is the most connected?
- Which countries are the most connected to each other?

Format:

`cities`

| variable | class | description |
| --- | --- | --- |
| id | str | City ID from Wikidata entity ID. Join with links data. |
| name | str | City name. |
| lng | float64 | Longitude. |
| lat | float64 | Latitude. |
| country | str | Country name. |
| countrycd | str | Two letter country code. Note that Taiwan has a code in the form XX-XX, and some entries as NA indicating a missing country code. |
| continent | str | Continent name. |

`links`

| variable | class | description |
| --- | --- | --- |
| source | str | ID of source city (from Wikidata entity ID), denoting link between source and target. The order of source and target does not matter. |
| target | str | ID of target city (from Wikidata entity ID). |

`links_enriched` (merged)

The script also produces `links_enriched`, which merges city metadata (name, coordinates, country, continent) onto both the source and target sides of each link, prefixed as `source_*` and `target_*`.

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'twinned_cities')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-05-12')
finally:
    os.chdir(cwd)

cities = pd.read_csv(os.path.join(data_dir, 'cities.csv'))
links = pd.read_csv(os.path.join(data_dir, 'links.csv'))
cities['lng'] = pd.to_numeric(cities['lng'], errors='coerce')
cities['lat'] = pd.to_numeric(cities['lat'], errors='coerce')
links_enriched = (
    links
    .merge(cities.rename(columns=lambda c: 'source_' + c if c != 'source' else c),
           left_on='source', right_on='source_id', how='left')
    .merge(cities.rename(columns=lambda c: 'target_' + c if c != 'target' else c),
           left_on='target', right_on='target_id', how='left')
)
```

## 8. Repair Cafes Worldwide

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-04-07/readme.md 

Description: Records of about 179,000 repair attempts logged by Repair Cafes worldwide, compiled by the [Repair Monitor](https://dashboard.repairmonitor.org/?language=en) since 2015. Repair Cafes are community events where volunteer fixers help people repair broken household items, and each record describes the item, its defect, and whether the repair succeeded.

Sample Questions:

- What kinds of items are most easily repaired?
- What are the most common reasons that items can't be repaired?
- Which countries have seen the most growth in Repair Cafe branches?
- Is GenAI becoming more popular than YouTube as a source of useful information for repairers?

Format:

`repairs`

| variable | class | description |
| --- | --- | --- |
| repair_id | str | Repair case ID number. |
| repair_date | datetime64 | Date of the repair. |
| repair_cafe_number | int64 | Repair cafe branch number. |
| repair_cafe_name | str | Repair cafe branch name. |
| country | str | Country. |
| kind_of_product | str | Product type. |
| category | str | Product category. |
| brand | str | Product brand. |
| estimated_year_of_production | int64 | Estimated year of production. |
| repaired | str | Whether the product was repaired. |
| repairability | float64 | Rating of repair ease, from 1 (difficult) to 10 (easy). |

`repairs_text`

| variable | class | description |
| --- | --- | --- |
| repair_id | str | Repair case ID number. |
| model | str | Product model or serial number. |
| defect_found | str | Description of defect. |
| problem_description | str | Description of repair problem or probable cause. |
| repair_method | str | Description of successful repair method. |
| partial_repair_notes | str | Description of partial repair method or advice. |
| failure_reasons | str | Reason(s) repair was not completed (list). |
| failure_reason_open | str | Reason repair was not completed (open answer). |
| used_repair_info | str | Whether repair information was consulted. |
| repair_info_source | str | Where did this information come from? |
| repair_info_url | str | Source repair information (url website). |
| suggestions | str | Advice for other repairers of similar products. |

`repairs_full` (merged)

The script also produces `repairs_full`, which merges all text detail columns from `repairs_text` onto `repairs` via `repair_id`.

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'repair_cafes')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-04-07')
finally:
    os.chdir(cwd)

repairs = pd.read_csv(os.path.join(data_dir, 'repairs.csv'))
repairs_text = pd.read_csv(os.path.join(data_dir, 'repairs_text.csv'))
repairs['repair_date'] = pd.to_datetime(repairs['repair_date'], errors='coerce')
repairs['repairability'] = pd.to_numeric(repairs['repairability'], errors='coerce')
# repair_id is not unique, but both files list repairs in the same order,
# so we number repeated ids to pair each repair with its own text row.
repairs['_n'] = repairs.groupby('repair_id').cumcount()
repairs_text['_n'] = repairs_text.groupby('repair_id').cumcount()
repairs_full = repairs.merge(repairs_text, on=['repair_id', '_n'], how='left')
repairs = repairs.drop(columns='_n')
repairs_text = repairs_text.drop(columns='_n')
repairs_full = repairs_full.drop(columns='_n')
```

## 9. The Languages of Africa

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2026/2026-01-13/readme.md 

Description: Popular languages spoken on the African continent, taken from the [Languages of Africa](https://en.wikipedia.org/wiki/Languages_of_Africa) page on Wikipedia. The data covers 502 languages from 17 language families across 51 countries, with an estimate of native speakers for each language. A language spoken in several countries appears once for each country.

Sample Questions:

- Which country in Africa has the largest number of spoken languages?
- Which family of languages has the highest density of speakers?
- Are there any languages that cut across multiple countries?

Format:

`africa`

| variable | class | description |
| --- | --- | --- |
| language | str | Name of popular African language. |
| family | category | Group of languages with similar ancestry, having similar vocabulary, phonetics and grammar. |
| native_speakers | float64 | Number of known native speakers of the language. |
| country | str | Country where this language is spoken. |

Download/Tidy Script:

```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'africa_languages')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2026-01-13')
finally:
    os.chdir(cwd)

africa = pd.read_csv(os.path.join(data_dir, 'africa.csv'))
africa['native_speakers'] = pd.to_numeric(africa['native_speakers'], errors='coerce')
africa['family'] = africa['family'].astype('category')
```

## 10. Groundhog Predictions

GitHub Link: https://github.com/rfordatascience/tidytuesday/blob/main/data/2024/2024-01-30/readme.md 

Description: Data on groundhog day predictions across the US and Canada. For anyone not familiar with the Groundhog Day tradition, if the groundhog sees its shadow and goes back into its burrow, that is a prediction of six more weeks of winter. Otherwise spring will come early.

Sample Questions:

- Which groundhogs have the longest prediction histories?
- Is there a geographic pattern to shadow vs. no-shadow predictions?
- How do predictions from actual groundhogs compare with those from substitute animals?
- Has the proportion of "early spring" predictions changed over time?

Format:

`groundhogs`

| variable | class | description |
| --- | --- | --- |
| id | int64 | A numeric id for this groundhog. |
| slug | str | The name of the groundhog, in simplified kebab case. |
| shortname | str | A short version of the name of the groundhog or groundhog substitute. |
| name | str | The full name of the groundhog or groundhog substitute. |
| city | str | The city in which the prediction takes place. |
| region | str | The state or province of the prediction. |
| country | str | The country of the prediction (USA or Canada). |
| latitude | float64 | The latitude of the city. |
| longitude | float64 | The longitude of the city. |
| source | str | A url with information about this groundhog. |
| current_prediction | str | A url with information about the most recent prediction. |
| is_groundhog | bool | Whether this predictor is a living groundhog. |
| type | str | A short description of the type of animal or other thing that makes the prediction. |
| active | bool | Whether this predictor is active (as of 2023). |
| description | str | A free-text description of the predictor. |
| image | str | A URL with an image of the predictor. |
| predictions_count | int64 | The number of predictions available for this predictor. |

`predictions`

| variable | class | description |
| --- | --- | --- |
| id | int64 | A numeric id for this groundhog. |
| year | int64 | The year of the prediction. |
| shadow | bool | Whether the groundhog saw its shadow, and thus predicts 6 more weeks of winter. May be NaN for years with no recorded prediction. |
| details | str | Free text with more information about this prediction. |

`groundhog_preds` (merged)

The script also produces `groundhog_preds`, which merges all groundhog metadata onto each prediction row via `id`.

Download/Tidy Script:
```python
import os
import pydytuesday
import pandas as pd

data_dir = os.path.join('data', 'groundhogs')
os.makedirs(data_dir, exist_ok=True)
cwd = os.getcwd()
os.chdir(data_dir)
try:
    pydytuesday.get_date('2024-01-30')
finally:
    os.chdir(cwd)

groundhogs = pd.read_csv(os.path.join(data_dir, 'groundhogs.csv'))
predictions = pd.read_csv(os.path.join(data_dir, 'predictions.csv'))
groundhogs['is_groundhog'] = groundhogs['is_groundhog'].astype(bool)
groundhogs['active'] = groundhogs['active'].astype(bool)
groundhogs['latitude'] = pd.to_numeric(groundhogs['latitude'], errors='coerce')
groundhogs['longitude'] = pd.to_numeric(groundhogs['longitude'], errors='coerce')
predictions['shadow'] = predictions['shadow'].map(
    {True: True, False: False, 'True': True, 'False': False}
)
groundhog_preds = predictions.merge(groundhogs, on='id', how='left')
```
