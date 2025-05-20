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


#? DF created, if data does not load, try with new terminal. 
#! Query, if not complex could be fixed with pandas. 

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





