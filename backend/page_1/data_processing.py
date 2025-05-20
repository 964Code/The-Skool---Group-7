import pandas as pd
from pathlib import Path
import duckdb

## For relative path
from utils.constants import DATA_DIRECTORY


df_kurser = pd.read_excel(
    DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"
).drop(
    columns=[
        "Diarienummer",
        "Kommun",
        "Län",
        "FA-region",
        "Antal kommuner",
        "Antal län",
        "Antal FA-regioner",
    ])


#! Query, if not complex could be fixed with pandas. 

# Regular DF
def approved_courses_filter(df):
    approved_courses = duckdb.query(
        """--sql
        SELECT
            "Anordnare namn" AS anordnare,
            COUNT(*) FILTER (WHERE Beslut ILIKE '%Bevilj%') AS "antal beviljade",
            COUNT(*) FILTER (WHERE Beslut ILIKE '%Avslag%') AS "antal avslag",
        FROM df
        GROUP BY "Anordnare namn"
        ORDER BY "antal beviljade" DESC;
        """
    ).df()
    return approved_courses

#----------------------------------------------

# Regular DF
def generate_kpi_df(df):
    kpi_df = duckdb.query(
        """--sql
            SELECT
                "Anordnare namn",
                "Utbildningsområde",
                COUNT(*) AS total_kurser,
                SUM(CASE WHEN Beslut = 'Beviljad' THEN 1 ELSE 0 END) AS beviljade_kurser,
                SUM(CASE WHEN Beslut = 'Beviljad' THEN "Totalt antal beviljade platser" ELSE 0 END) AS beviljade_platser,
                ROUND(100.0 * SUM(CASE WHEN Beslut = 'Beviljad' THEN 1 ELSE 0 END) / COUNT(*), 2) AS godkännandeprocent
            FROM df
            GROUP BY "Anordnare namn", "Utbildningsområde",
            ORDER BY "Anordnare namn" DESC
        """
    ).df()

    return kpi_df

def filter_kpi_data(df_kpi, utbildningsområde=None, skola=None):
    df_filtered = df_kpi.copy()

    if utbildningsområde:
        df_filtered = df_filtered[df_filtered["Utbildningsområde"] == utbildningsområde]

    if skola:
        df_filtered = df_filtered[df_filtered["Anordnare namn"] == skola]

    return df_filtered.reset_index(drop=True)

def extract_kpis_kurser(df_filtered):

    # Aggregate over all rows in case there are multiple utbildningsområden or skolor
    antal_kurser = df_filtered["total_kurser"].sum()
    antal_beviljade_kurser = df_filtered["beviljade_kurser"].sum()
    antal_beviljade_platser = df_filtered["beviljade_platser"].sum()
    godkännandeprocent = (
        (antal_beviljade_kurser / antal_kurser) * 100 if antal_kurser > 0 else 0.0
    )

    return {
        "antal_kurser": antal_kurser,
        "antal_beviljade_kurser": int(antal_beviljade_kurser),
        "antal_beviljade_platser": int(antal_beviljade_platser),
        "godkännandeprocent": int(godkännandeprocent) if godkännandeprocent == int(godkännandeprocent) else round(godkännandeprocent, 2),

    }


#----------------------------------------------
