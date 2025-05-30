import pandas as pd
from pathlib import Path
import duckdb
from utils.constants import DATA_DIRECTORY


df_courses = pd.read_excel(
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

def filter_kpi_data(df_kpi, education_area=None, school=None):
    df_filtered = df_kpi.copy()

    if education_area:
        df_filtered = df_filtered[df_filtered["Utbildningsområde"] == education_area]

    if school:
        df_filtered = df_filtered[df_filtered["Anordnare namn"] == school]

    return df_filtered.reset_index(drop=True)


def extract_kpis_kurser(df_filtered):

    total_courses = df_filtered["total_kurser"].sum()
    amount_total_approved = df_filtered["beviljade_kurser"].sum()
    approved_seats = df_filtered["beviljade_platser"].sum()
    percentage_approved = (
        (amount_total_approved / total_courses) * 100 if total_courses > 0 else 0.0
    )

    return {
        "antal_kurser": total_courses,
        "antal_beviljade_kurser": int(amount_total_approved),
        "antal_beviljade_platser": int(approved_seats),
        "godkännandeprocent": int(percentage_approved) if percentage_approved == int(percentage_approved) else round(percentage_approved, 2),

    }

