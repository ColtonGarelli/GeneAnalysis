import pandas as pd
import GEOparse as geo
import re
import os


def get_geo(geo_accesions: list = None, paths= None):
    """

    Args:
        geo_accesions:

    Returns:

    """
    geos = list()
    if paths is None:
        for i in geo_accesions:
            geos.append(geo.get_GEO(i))
        geo_entries = geos
    else:
        for i in paths:
            geos.append(geo.get_GEO(filepath=os.path.join(i)))
        geo_entries = geos
    return geo_entries


def get_controls(data):
    """
    gsms = [geos[0].gsms.get(i) for i in parse_geo.get_controls(geos[0])] to get a list of gsm objects
    Args:
        data:

    Returns:

    """
    controls = list()
    control_terms = ['healthy', 'normal', 'control', 'ctrl']
    if isinstance(data, geo.GEOTypes.GSM):
        sample_info = [i for i in data.metadata.get('characteristics_ch1')]
        for i in sample_info:
            if 'healthy' in i.lower() or 'control' in i.lower() or 'normal' in i.lower():
                controls.append(data)
    elif isinstance(data, geo.GEOTypes.GSE):
        gsms = data.gsms
        for k, v in gsms.items():
            meta = v.metadata.get('characteristics_ch1')
            for i in meta:
                for term in control_terms:
                    if re.search(term, i, re.IGNORECASE):
                        controls.append(k)
    else:
        print('wrong datatype!!')

    return controls


def print_data_processing_method(gses):
    datasets = [i for i in gses]
    for i1 in datasets:
        temp = i1
        samples = [i2 for i2 in i1.gsms]
        for i3 in samples:
            # print(temp.gsms.get(i3).metadata.get('characteristics_ch1'))
            print(temp.gsms.get(i3).metadata.get('data_processing'))
            # print(i1(i3).get('charactersitics_ch1').get('data_processing'))
        # print([i.gsms.get(i2).metadata.get('charactersitics_ch1').get('data_processing') for i2 in i.gsms.keys()])


def geo_to_common(geos: list):
    pass


def map_genes_to_expression(expr_vals, gene_names):
    pass


