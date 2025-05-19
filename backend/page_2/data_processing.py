from utils.constants import DATA_DIRECTORY
import pandas as pd
import duckdb as db

df_2024 = pd.read_excel(DATA_DIRECTORY / "resultat-ansokningsomgang-2024.xlsx", sheet_name="Tabell 3", skiprows=5)
df_2023 = pd.read_excel(DATA_DIRECTORY / "resultat-ansokningsomgang-2023.xlsx", sheet_name="Tabell 3", skiprows=5)
df_2022 = pd.read_excel(DATA_DIRECTORY / "resultat-ansokningsomgang-2022.xlsx", sheet_name="Tabell 3")


df_2024["År"] = 2024
df_2023["År"] = 2023
df_2022["År"] = 2022


df_2024_filter = db.query("""--sql
         SELECT År,"Utbildningsanordnare administrativ enhet",Utbildningsområde ,beslut,Kommun, Län, 
         FROM df_2024
         """).df()
df_2023_filter = db.query("""--sql
         SELECT År,"Utbildningsanordnare administrativ enhet" ,Utbildningsområde,beslut,Kommun, Län
         FROM df_2023
         """).df()
df_2022_filter = db.query("""--sql
         SELECT År,"Utbildningsanordnare administrativ enhet" ,Utbildningsområde,beslut,Kommun, län
         FROM df_2022
         """).df()
df_combined = pd.concat([df_2022_filter, df_2023_filter, df_2024_filter], ignore_index=True)


skola_beviljade = db.query("""--sql
    SELECT 
        År,"Utbildningsanordnare administrativ enhet" AS Skola,
        COUNT(*) FILTER (WHERE Beslut = 'Beviljad') AS Beviljade,
    FROM df_combined
    WHERE År == 2024
    GROUP BY "Utbildningsanordnare administrativ enhet", År
    ORDER BY Beviljade DESC
""").to_df()
