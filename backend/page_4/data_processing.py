from utils.constants import DATA_DIRECTORY
import pandas as pd
import duckdb as db
from difflib import get_close_matches


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


approved_schools = db.query("""--sql
    SELECT 
        År,"Utbildningsanordnare administrativ enhet" AS Skola,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
    FROM df_combined
    WHERE År == 2024
    GROUP BY "Utbildningsanordnare administrativ enhet", År
    ORDER BY Beviljade DESC
""").to_df()

all_results = db.query("""--sql
    SELECT 
        År,
        Utbildningsområde,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag
    FROM df_combined
    GROUP BY År, Utbildningsområde
""").to_df()

all_school_results = db.query("""--sql
    SELECT 
        År,
        "Utbildningsanordnare administrativ enhet" AS Skola,
        Utbildningsområde,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
        COUNT(*) FILTER (WHERE Beslut = 'Avslag') AS Avslag
    FROM df_combined
    GROUP BY År, Utbildningsområde, Skola
""").to_df()


unique_schools = []
def find_standard_name(namn):
    match = get_close_matches(namn, unique_schools, n=1, cutoff=0.8)
    if match:
        return match[0]
    else:
        unique_schools.append(namn)
        return namn

all_school_results["StandardSkola"] = all_school_results["Skola"].apply(find_standard_name)

grouped_df = db.query("""--sql
    SELECT *
    FROM (
        SELECT 
            StandardSkola, 
            År, 
            SUM(Beviljade) AS Beviljade,
            SUM(Avslag) AS Avslag,
            ROW_NUMBER() OVER (PARTITION BY År ORDER BY SUM(Beviljade) DESC) AS rn
        FROM all_school_results
        GROUP BY StandardSkola, År
        Order by År, Beviljade DESC
    )
""").to_df()










