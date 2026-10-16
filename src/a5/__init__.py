import os

import pandas as pd
import geopandas as gpd
from shapely import ops
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")

def load_dunkins():
    raw_dunkins = pd.read_json(os.path.join(DATA_DIR, "dunkinDonuts.json"))
    pop = pd.read_json(os.path.join(DATA_DIR, "statePop.json"))

    def parse_hours(s):
        try:
            s = s.strip()
            if s == "24HOURS":
                return 24.0
            if s == "":
                return 0.
            start, end = s.split("-")
            def to_frac(t):
                h, m = map(int, t.split(":"))
                return h + m / 60
            return to_frac(end) - to_frac(start)
        except ValueError as e:
            return 0.

    raw_dunkins.sat_delivery_hours = raw_dunkins.sat_delivery_hours.map(parse_hours)

    def aggregate(state, df):
        pop_state = pop.loc[pop["state"] == state].iloc[0]
        store_count = len(df)
        return pd.DataFrame([{
            "region": pop_state["region"],
            "store_count": store_count,
            "stores_per_100k": (store_count / pop_state["population"]) * 100_000,
            "stores_per_sqmi": store_count / pop_state["land_sq_mi"],
            "avg_sat_delivery_hours": df["sat_delivery_hours"].mean(),
            "frac_loyalty": (df["loyalty"] == "Y").mean(),
        }])

    return (
        raw_dunkins
        .groupby("state")
        .apply(lambda df: aggregate(df.name, df))
        .reset_index()
        .drop(columns=["level_1"])
    )
  
def load_ri_life():
    raw_life = pd.read_csv(os.path.join(DATA_DIR, "life_expectancy_ri.csv"))
    raw_life["Rural/Urban"] = raw_life["Composite measure of rural-urban status"].map(lambda n: "Urban" if n > raw_life["Composite measure of rural-urban status"].median() else "Rural")

    life = raw_life.rename(columns={
        "Rural/Urban": "rural_urban",
        "Life expectancy": "life_expectancy",
        "Name": "name",
        "Rank of ASMR": "asmr_rank",
        "Median rent": "rent",
        "Gini Index": "gini",
        "Age-standardized mortality rate (ASMR) per 100,000": "asmr",
        "Percent of population in food desert": "pct_food_desert",
        'Fast food and convenience stores per square mile': "fast_food",
        "Percent living within 10 minutes of a farmers' market": "pct_farmers_market",
        "Percent of population with less than high school education": "pct_less_hs",
        "Percent of population with a bachelor's degree or higher": "pct_bachelors",
    })[[
        "rural_urban", "life_expectancy", "name", "asmr", "asmr_rank", "rent", "gini", "pct_food_desert", "fast_food", "pct_farmers_market", "pct_less_hs", "pct_bachelors"
    ]]

    geo = gpd.read_file(os.path.join(DATA_DIR, "ri_towns_lonlat.geojson"))
    geo["geometry"] = geo["geometry"].apply(
        lambda geom: ops.transform(lambda x, y: (y, x), geom)
    )

    normalize = lambda s: s.strip().upper()
    geo["name_key"] = geo["NAME"].apply(normalize)
    life["name_key"] = life["name"].apply(normalize)

    return geo.merge(life, on="name_key", how="left") \
        .drop(columns=["name_key", "name", "STATEFP", "COUNTYFP", "COUSUBFP", "COUSUBNS", "GEOIDFQ", "GEOID", "NAMELSAD", "STUSPS",
                      "NAMELSADCO", "STATE_NAME", "LSAD", "ALAND", "AWATER"]) \
        .rename(columns={"NAME": "county"})