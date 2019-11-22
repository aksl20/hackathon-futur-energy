import pandas as pd
import numpy as np

def clean_bp(file_path, sheet_name, usecols=list(range(55)), skiprows=2,
             index_col=0, skipfooter=10, drop_total=False):
    bp_df = pd.read_excel(str(file_path), sheet_name=sheet_name, 
                          usecols=usecols, skiprows=skiprows, index_col=index_col,
                          skipfooter=skipfooter).dropna().T.reset_index()
    columns = bp_df.columns[0]
    bp_df = bp_df.melt(id_vars=columns)
    bp_df.columns = ['date', 'country', bp_df.columns[1]]
    if drop_total:
        bp_df = bp_df.loc[~bp_df.country.str.lower().str.contains('total'), :]
    bp_df.date = pd.to_datetime(bp_df.date, format='%Y')
    bp_df = bp_df.pivot_table(index=['country', 'date'], values=bp_df.columns[2])
    return bp_df