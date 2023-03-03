from copy import deepcopy

import geopandas as gpd
import numpy as np
import pandas as pd


def transform_to_gdf(
    df: pd.DataFrame,
    longitude: str = "longitude",
    latitude: str = "latitude",
) -> gpd.GeoDataFrame:
    """Transform a DataFrame to a GeoDataFrame with GeoPoints.

    Parameters
    ----------
    df : pd.DataFrame
        Original DataFrame.
    longitude : str, optional
        Name of the longitude column., by default "longitude"
    latitude : str, optional
        Name of the latitude column., by default "latitude"

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame
    """
    longitude = df.pop("longitude")
    latitude = df.pop("latitude")
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(
            longitude,
            latitude,
        ),
    )
    return gdf


def contains(
    region_series: gpd.GeoSeries,
    gdf: gpd.GeoDataFrame,
    geometry_col_regions: str,
    geometry_col_gdf: str,
) -> bool:
    """Check if the points in gdf are in the regions in regions_series.

    Parameters
    ----------
    region_series : gpd.GeoSeries
        DataFrame of all regions (GeoDataFrame from geojson).
    gdf : gpd.GeoDataFrame
        GeoDataFrame with all points to test.
    geometry_col_regions : str
        Regions geometry index.
    geometry_col_gdf : str
        GeoDataFrame geomtry column.

    Returns
    -------
    bool
        Series with booleans to indicate if the points are in the regions.
    """
    return region_series[geometry_col_regions].contains(gdf[geometry_col_gdf])


def set_code_where_true(region_series: pd.Series) -> pd.Series:
    """Replace True in Series with the region code.

    Parameters
    ----------
    region_series : pd.Series
        Boolean series.

    Returns
    -------
    pd.Series
        Series with codes instead of True and NaN instead of False.
    """
    return region_series.where(
        region_series,
        np.nan,
    ).mask(
        region_series,
        int(region_series.name),
    )


def map_geometry_to_region_code(
    gdf: gpd.GeoDataFrame,
    regions_table: pd.DataFrame,
    code_col: str = "code",
    geometry_col_regions: str = "geometry",
    geometry_col_gdf: str = "geometry",
    remove_empty: bool = True,
) -> pd.DataFrame:
    """Concatenate to GeoDataFrame the codes of the region containing the point.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame.
    regions_table : pd.DataFrame
        Regions Table.
    code_col : str, optional
        Region code index in regions_table., by default "code"
    geometry_col_regions : str, optional
        Geometry index in regions_table., by default "geometry"
    geometry_col_gdf : str, optional
        Geometry index in gdf., by default "geometry"
    remove_empty : bool, optional
        Whether to remove row when not contained in any region., by default True

    Returns
    -------
    pd.DataFrame
        gdf copy with additionnal column containing the region code.
    """
    regions_bools = regions_table.apply(
        contains,
        args=(gdf, geometry_col_regions, geometry_col_gdf),
        axis=0,
    )
    regions_bools.columns = regions_table.loc[code_col, :]
    if remove_empty:
        any_true = regions_bools.any(axis=1)
        gdf = gdf[any_true]
        regions_bools = regions_bools[any_true]

    regions_codes = regions_bools.apply(set_code_where_true)

    total = None
    for _, column in regions_codes.items():
        if total is None:
            total = column
            continue
        total[pd.isna(total)] = column[pd.isna(total)]
    output = deepcopy(gdf)
    output[code_col] = total
    return output
