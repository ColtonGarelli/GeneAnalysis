"""Functions for file output.

This module contains functions for creating new directories, managing temp directories, determining if directories/files
already exist, and outputting data to files.
"""
import pandas as pd
import os
from datetime import date


def dataframe_to_csv(df: pd.DataFrame or [pd.DataFrame], base_path: str or os.PathLike, file_name: str=None):
    """
    Output a given dataframe to csv
    Args:
        df:

        base_path:

        file_name:

    Returns:

    """
    if file_name is None:
        if isinstance(df, pd.DataFrame):
            df.to_csv(os.path.join(base_path, ""))
        if isinstance(df, list):
            [i.to_csv(os.path.join(base_path, file_name)) for i in df]
    else:
        if isinstance(df, pd.DataFrame):
            df.to_csv(os.path.join(base_path, file_name))
        if isinstance(df, list):
            [i.to_csv(os.path.join(base_path, file_name)) for i in df]


def make_original_file_name(file_out_dir, file_extension: str, root_dir: str or os.PathLike = None, file_name: str = None):
    counter = 0
    if root_dir is None:
        root_dir = os.path.expanduser("~")
    if not os.path.isdir(file_out_dir):
        file_out_dir = create_new_file_dir(root_dir)
    if file_name is not None:
        new_file_name = file_name + "_PAM_Output_{}".format(counter)
    else:
        new_file_name = "PAM_Output_{}".format(counter)
    new_file_path = os.path.join(file_out_dir, new_file_name)
    while os.path.exists(new_file_path):
        counter += 1
        if counter < 11:
            new_file_path = new_file_path[:-1]
        elif counter > 10:
            new_file_path = new_file_path[:-2]
        elif counter > 100:
            new_file_path = new_file_path[:-3]
        new_file_path = new_file_path + "_" + str(counter)
    return os.path.join(new_file_path + file_extension)


def create_new_file_dir(root_dir, dirname=None):
    """

    Args:
        root_dir: the root directory of
        dirname: a name for the folder to create

    Returns:

    """
    if dirname is None:
        new_dir_name = os.path.join(root_dir, "GeneAnalysis_output_{}".format(date.today()))
    else:
        new_dir_name = os.path.join(root_dir, dirname)
    counter = 0
    if os.path.isdir(new_dir_name):
        new_dir_name = new_dir_name + "_{}".format(counter)
        while os.path.isdir(new_dir_name):
            counter += 1
            if counter < 11:
                new_dir_name = new_dir_name[:-1]
            elif counter > 10:
                new_dir_name = new_dir_name[:-2]
            elif counter > 100:
                new_dir_name = new_dir_name[:-3]

            new_dir_name = new_dir_name + str(counter)
            os.path.join(new_dir_name)
        os.mkdir(new_dir_name)
    else:
        os.mkdir(new_dir_name)
    return new_dir_name

