import os
import datetime
import re
from typing import List
import pandas as pd
from .utils_fn import (transform_dataframe_for_analysis,
                       filter_out_unwanted_rows,
                       FILE_PATH_PATTERN)

FILE_PATH = os.path.join(os.getcwd(), 'src/data/')



def load_and_transform_dataframe(filename: str, sheet_name: str) -> pd.DataFrame:
    """
    takes a given file and performs ETL ready for data analysis
    parameters
    ---------
    filename: str
        the particular excel file that is to be read
    sheet_name: str
        the particular sheet in the excel spreadsheet to read

    returns
    -------
    pd.DataFrame: a cleaned dataframe which is ready to visualise
    """

    data: pd.DataFrame = pd.read_excel(filename, 
                        sheet_name=sheet_name,
                        skiprows=4,
                        na_values=['..'],
                        # engine='openpyxl'
                        )
    col_headers: List[str] = data.loc[0, :].to_list()

    data = transform_dataframe_for_analysis(col_headers, 
                                            filter_out_unwanted_rows(data))
    return data

def extract_most_recent_data() -> str:
    """
    extracts the most recent data file to produce the data visualisations 
    and update the publication links
    
    returns
    ------
    str: the relative file path of the data to carry out ETL on.
    """
    data_dir = sorted(
        {f'{FILE_PATH}{x}':datetime.datetime.fromtimestamp(os.path.getmtime(f'{FILE_PATH}{x}')) 
         for x in os.listdir(FILE_PATH) if re.match(FILE_PATH_PATTERN, x)}.items(),
         key=lambda x: x[1]
         )

    return data_dir[0][0]

