
import pandas as pd
from pathlib import Path
import duckdb

from utils.constants import DATA_DIRECTORY

df_stud = pd.read_csv(DATA_DIRECTORY / "Yrkeshogskolan_transformed.csv").rename(columns={'Unnamed: 0': 'År'})
