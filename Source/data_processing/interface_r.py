"""
A module containing data_processing to utilize R, mainly the ComBat function in the sva package
"""

import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.pandas2ri as rpd
# import rpy2.rinterface
# from rpy2.rinterface import SexpS4
# from rpy2.robjects.conversion import Converter
# stats = importr('stats')
methods = importr('methods')
base = importr('base')
biobase = importr('Biobase')
# DFP = importr('DFP')
# R = ro.r



def pandas_df_to_exprset(phenoData, featureData, dfs: pd.DataFrame or [pd.DataFrame]) -> pd.DataFrame or list:
    # TODO: !!!IMPORTANT!!! methods.new("ExpressionSet", exprs=base.as_matrix(df)) to make an exprset from df
    # object.r_repr() to print representation
    # phenoData = annotatedDF, featureData = AnnotatedDF, assayData=expresion matrix (type matrix or AssayData)
    """A function to convert a pandas DataFrame to a Biobase ExpressionSet

        Takes a list of pandas DataFrames or a single pandas DataFrame and converts it to
        (source: https://bioconductor.org/packages/release/bioc/html/Biobase.html)

    References:
        https://rpy2.readthedocs.io/en/version_2.7.x/generated_rst/s4class.html
        https://rpy2.readthedocs.io/en/version_2.7.x/_static/notebooks/s4class.html
        https://rpy2.readthedocs.io/en/version_2.8.x/robjects_oop.html

    Args:
        dfs: pd.DataFrame(s) to convert to Biobase.ExpressionSet (single dataframe or a list)

    Returns:
        a Biobase.ExpressionSet object or a list of Biobase.ExpressionSet objects

    """
    # attributes can be accessed using .slots

    rpd.activate()
    data = importr('data.table')
    base = importr('base')
    ballgown = importr('ballgown')
    # dfs.dropna(inplace=True)

    if isinstance(dfs, list):
        exprset = list()
        for i in dfs:
            data = [dfs[col].values.tolist() for col in dfs]
            cols = [col for col in dfs]
            exprset.append(methods.new('ExpressionSet', exprs=biobase.assayData(rpd.py2ri_pandasdataframe(data)), phenoData=biobase.AnnotatedDataFrame(phenoData),
                                       featureData=biobase.AnnotatedDataFrame(featureData)))
    else:
        # data = [dfs[col].values.tolist() for col in dfs]
        rphenoData = biobase.AnnotatedDataFrame(rpd.py2ri_pandasdataframe(phenoData))
        rfeatureData = biobase.AnnotatedDataFrame(rpd.py2ri_pandasdataframe(featureData))
        rdata = data.na_omit_data_table(rpd.py2ri_pandasdataframe(dfs))
        # used to be data.as_matrix
        exprs = base.as_matrix((rdata))
        # rdata = base.unname(rdata)
        # print(rdata)
        exprset = biobase.ExpressionSet()
        exprset.slots['assayData<-'] = exprs
        exprset.slots['phenoData'] = rphenoData
        exprset.slots['featureData'] = rfeatureData

        # print(ballgown.expr(exprset))
    # rpd.deactivate()
    return exprset


def get_feature_data(expr_df: pd.DataFrame, genes: str, probeIDs: bool = False):
    """

    Args:
        expr_df:

    Returns:

    """
    if not probeIDs:
        data = [i.replace(' ','.') for i in expr_df.index.to_list()]
        return pd.DataFrame(data=data)

    else:
        return pd.DataFrame(index=[i.replace(' ','.') for i in expr_df.index.to_list()], data=expr_df[[genes]])


def get_pheno_data(expr_df, disease, batches):
    """Sample ID, disease, batch

    Args:
        expr_df:
        disease:
        batches:

    Returns:

    """
    ind = expr_df.columns.to_list()
    no_space = [i.replace(' ', '.') for i in ind]
    no_dash = [i.replace('-', '.') for i in no_space]
    data = pd.DataFrame(data=[no_dash, disease]).transpose()
    data.columns = ['sample', 'disease']
    data['batch'] = batches


    # data.index = ind
    return data
    # return pd.DataFrame(index=ind, data=data, columns=['sample''disease', 'batch'])


def batch_adjust(expr_df, batch):
    # sample call: ir.batch_adjust(exprset, batch=[batch1.columns.to_list(), [1,1,1]])
    """
    TODO: some 0 or na somewhere causing regection
         Error in `contrasts<-`(`*tmp*`, value = contr.funs[1 + isOF[nn]]) :
         contrasts can be applied only to factors with 2 or more levels
    Args:
        expr_df:
        batch:

    Returns:

    """
    ro.pandas2ri.activate()
    sva = importr('sva')
    base = importr('base')
    batch_vec = ro.Vector(batch)
    # batch can be a pd dataframe. has to have multiple levels
    rbatch = ro.FactorVector(obj=ro.Vector(batch), labels=ro.Vector(batch[0]), levels=ro.Vector(batch[1:]))
    print(rbatch.slots['levels'].r_repr())
    # print(expr_df.slots['assayData'].r_repr())
    # NAs in corrected matrix caused by genes = 0?
    # remove na: batch1 = batch1[(batch1.T != 0).any()]
    # batch needs to have multiple list dimensions (multi-level)
    # df =base.as_matrix(rpd.py2ri_pandasdataframe(expr_df))
    batch_corrected = sva.ComBat(dat=expr_df, batch=rbatch) #, mod=ro.NULL)#, mean_only=True)
    ro.pandas2ri.deactivate()
    return batch_corrected







