import datetime as dt

import pandas as pd
import xarray as xr

DATA_START_DATE = dt.datetime(1900, 1, 1)


def load_from_cds(filepath: str) -> pd.DataFrame:
    return xr.open_dataset(filepath).to_dataframe().reset_index()
