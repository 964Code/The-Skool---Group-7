from utils.constants import DATA_DIRECTORY,ASSETS_DIRECTORY
import pandas as pd
import duckdb as db
import json
from difflib import get_close_matches
import numpy as np


with open(ASSETS_DIRECTORY / "swedish_regions.geojson", "r") as file:
    json_data = json.load(file)

json_data.get("features")[0].get("properties")

df_2024 = pd.read_excel(DATA_DIRECTORY / "resultat-ansokningsomgang-2024.xlsx", sheet_name="Tabell 3", skiprows=5)
df_2023 = pd.read_excel(DATA_DIRECTORY / "resultat-ansokningsomgang-2023.xlsx", sheet_name="Tabell 3", skiprows=5)
df_2022 = pd.read_excel(DATA_DIRECTORY / "resultat-ansokningsomgang-2022.xlsx", sheet_name="Tabell 3")


df_2024["År"] = 2024
df_2023["År"] = 2023
df_2022["År"] = 2022


df_2024_filtered = db.query("""--sql
         SELECT År,"Utbildningsanordnare administrativ enhet",Utbildningsområde ,beslut,Kommun, Län, 
         FROM df_2024
         """).df()
df_2023_filtered = db.query("""--sql
         SELECT År,"Utbildningsanordnare administrativ enhet" ,Utbildningsområde,beslut,Kommun, Län
         FROM df_2023
         """).df()
df_2022_filtered = db.query("""--sql
         SELECT År,"Utbildningsanordnare administrativ enhet" ,Utbildningsområde,beslut,Kommun, län
         FROM df_2022
         """).df()
df_combined = pd.concat([df_2022_filtered, df_2023_filtered, df_2024_filtered], ignore_index=True)


school_approved = db.query("""--sql
    SELECT 
        År,"Utbildningsanordnare administrativ enhet" AS Skola,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
    FROM df_combined
    WHERE År == 2024
    GROUP BY "Utbildningsanordnare administrativ enhet", År
    ORDER BY Beviljade DESC
""").to_df()

result_all = db.query("""--sql
    SELECT 
        År,
        Utbildningsområde,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag
    FROM df_combined
    GROUP BY År, Utbildningsområde
""").to_df()

approval_rate_df = db.query("""--sql
    SELECT
        År,
        Utbildningsområde,
        COUNT(*) AS total_ansökningar,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS beviljade,
        ROUND(100.0 * COUNT(*) FILTER (WHERE Beslut = 'Beviljad') / COUNT(*),2) AS "beviljandegrad (%)"
    FROM df_combined
    GROUP BY År, Utbildningsområde
    ORDER BY År,"beviljandegrad (%)" DESC
""").df()

approval_rate_df.head()


df_region_total = db.query("""--sql
    SELECT 
        År,Län,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag
    FROM df_combined
    GROUP BY Län, År
    ORDER BY År ASC, Beviljade DESC
""").to_df()

df_regions_approved = db.query("""--sql
             SELECT län, CAST(COUNT_IF(beslut = 'Beviljad') as INTEGER) as Beviljade
             FROM df_combined
             WHERE län != 'Flera kommuner'
             GROUP BY län
             ORDER BY Beviljade DESC, län ASC
             """).df()

df_regions_rejected = db.query("""--sql
             SELECT län, CAST(COUNT_IF(beslut = 'Avslag') as INTEGER) as Avslag
             FROM df_combined
             WHERE län != 'Flera kommuner'
             GROUP BY län
             ORDER BY Avslag DESC, län ASC
             """).df()

df_region_total

properties = [feature.get("properties") for feature in json_data.get("features")]
region_code = {property.get("name"): property.get("ref:se:länskod") for property in properties}

region_total = get_close_matches(df_region_total["Län"].iloc[0], region_code.keys())[0]

region_code_map = []

for region in df_region_total["Län"]:
    match = get_close_matches(region, region_code.keys(), n=1)
    if match:
        region_code_map.append(region_code[match[0]])
    else:
        region_code_map.append(None)


log_approved = np.log(df_regions_approved["Beviljade"]+1)
log_rejected = np.log(df_regions_rejected["Avslag"]+1)
