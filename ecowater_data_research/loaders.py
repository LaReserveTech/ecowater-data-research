import json

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr


def load_from_cds(filepath: str) -> pd.DataFrame:
    """Load GeoDataFrame from NetCDF file.

    Parameters
    ----------
    filepath : str
        Path to the NetCDF file containing the data.

    Returns
    -------
    pd.DataFrame
        DataFrame from the file.
    """
    gdf = xr.open_dataset(filepath).to_dataframe().reset_index()
    gdf["time"] = gdf["time"].dt.date
    gdf.groupby(["latitude", "longitude", "time"]).sum().reset_index()
    return gdf


def load_swi_metadata(filepath: str) -> pd.DataFrame:
    """Load and Format metadata csv for SWI data

    Parameters
    ----------
    filepath : str
        Path to data CSV

    Returns
    -------
    pd.DataFrame
        Formatted DataFrame
    """
    return pd.read_csv(
        filepath,
        delimiter=";",
        skiprows=4,
        usecols=["lat_dg", "lon_dg", "#num_maille"],
    ).rename(
        columns={
            "lat_dg": "latitude",
            "lon_dg": "longitude",
            "#num_maille": "maille_nb",
        }
    )


def load_swi_data(
    filepaths: str | list[str],
    metadata_filepath: str,
    years: list[int] | int = [],
) -> pd.DataFrame:
    """Load and Format SWI data from Météo France

    Parameters
    ----------
    filepaths : str | list[str]
        Path or list of path of files to load.
    metadata_filepath : str
        Metadata CSV path
    years : list[int] | int, optional
        Years to consider, all years will be returned if empty., by default []

    Returns
    -------
    pd.DataFrame
        Formatted DataFrame
    """
    meta = load_swi_metadata(metadata_filepath)
    if isinstance(filepaths, str):
        filepaths = [filepaths]
    if isinstance(years, int):
        years = [years]
    dfs = []
    for file in filepaths:
        # Read file
        lambert_df = pd.read_csv(
            file,
            delimiter=";",
            usecols=["DATE", "NUMERO", "SWI_UNIF_MENS3"],
        )
        # remove date (date format: YYYYMM)
        date = lambert_df.pop("DATE").astype(str)
        # Rename columns
        lambert_df.rename(
            columns={
                "NUMERO": "maille_nb",
                "SWI_UNIF_MENS3": "SWI",
            },
            inplace=True,
        )
        # replace ',' in number to convert to float
        lambert_df["SWI"] = (
            lambert_df["SWI"].astype(str).str.replace(",", ".").astype(float)
        )
        # parse year and month from date column
        year = date.str.slice(0, 4).astype(int)
        month = date.str.slice(4).astype(int)
        day = pd.Series(np.ones(month.shape))
        # create new date column
        lambert_df["date"] = pd.to_datetime(
            pd.concat(
                [year, month, day],
                axis=1,
                keys=["year", "month", "day"],
            )
        )
        # select relevant years
        if years:
            lambert_df = lambert_df[lambert_df["date"].dt.year.isin(years)]
        lambert_df["date"] = lambert_df["date"].dt.date
        # merge with metadata to get latitude and longitude
        df = lambert_df.merge(meta, on="maille_nb")
        dfs.append(df)
    # concatenate all files
    return pd.concat(dfs, ignore_index=True)


def load_geojson(filepath: str) -> dict:
    """Load GeoJson

    Parameters
    ----------
    filepath : str
        Path to the geojson file.

    Returns
    -------
    dict
        Dictionnary corresponding to the geojson.
    """
    return json.load(open(filepath))


def load_geotable(filepath: str) -> gpd.GeoDataFrame:
    """Return transposed GeoDataFrame corresponding to the geojson.

    Parameters
    ----------
    filepath : str
        Path to the geojson file.

    Returns
    -------
    gpd.GeoDataFrame
        Transposed GeoDataFrame corresponding to the geojson.
    """
    return gpd.read_file(filepath).transpose()
