import json

import geopandas as gpd
import xarray as xr


def load_from_cds(filepath: str) -> gpd.GeoDataFrame:
    """Load GeoDataFrame from NetCDF file.

    Parameters
    ----------
    filepath : str
        Path to the NetCDF file containing the data.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame from the file.
    """
    gdf = xr.open_dataset(filepath).to_dataframe().reset_index()
    gdf["time"] = gdf["time"].dt.date
    gdf.groupby(["latitude", "longitude", "time"]).sum().reset_index()
    return gdf


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
