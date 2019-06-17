import pandas as pd
import GEOparse as geo


def get_geo(geo_accesions: list):
    """

    Args:
        geo_accesions:

    Returns:

    """
    geos = list()
    for i in geo_accesions:
        geos.append(geo.get_GEO(i))
    geo_entries = geos
    return geo_entries


def geo_to_common(geos: list):
    pass


