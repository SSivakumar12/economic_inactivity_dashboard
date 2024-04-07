import re
# import requests
# import io
import typing
import datetime
import pandas as pd

DATE_PATTERN: str =  r'\b\d{4}\b'
NUMBER_PATTERN: str = r'\d+'


FILE_PATH_PATTERN: str = r"^inac01sa(.*)\.xls$"

def extract_year(date_string: str) -> typing.Union[str, None]:
    """
    from a given string extracts the year from the string.
    If a year doesn't exist then return None

    parameters
    -----------
    date_string: str
        a string which contains some numbers in it.
  
    -----------
    year: str
      a string representation of the year within the string
    
    example implementation
    ----------
    ```python
    >>> extract_year('2024 is the year!!!')
    >>> '2024'

    >>> extract_year('20003 is something I can look forward to!!')
    >>> '2000'
    ```
    """
    
    pattern = re.search(NUMBER_PATTERN, date_string)

    if pattern:
        year = pattern.group(0)
        if len(year) > 4:
            year = year[:4]
        return year
    else:
        return None

def filter_out_unwanted_rows(df: pd.DataFrame) -> pd.DataFrame:
  """
  filter out the indexes of rows that contain background information
  but do not have anyting valuable for analysis
  
  parameters
  ----------
  df: pd.DataFrame
    a datafrane that contains that contains unemployment index

  returns
  --------
  df: pd.DataFrame
    a new copy of the dataframe with noise rows removed 
  """
  df_copy = df.copy(deep=True)
  df_copy['Unnamed: 0'] = df_copy['Unnamed: 0'].apply(str)
  

  indexes_to_remove = (list(range(0, df_copy[df_copy['Unnamed: 0'] == 'Dataset identifier code'].index[0] + 2)) 
                       + list(range(df_copy[df_copy['Unnamed: 0'].str.contains('Note: ')].index[0] - 1, df.shape[0])))
  df = df[~df.index.isin(indexes_to_remove)]
  return df

def transform_dataframe_for_analysis(col_headers: typing.List[str], removed_noise_df: pd.DataFrame) -> pd.DataFrame:
  """
  using the relevant headers from the original dataframe and adds them to the dataframe that has been initally cleaned

  parameters
  ----------
  col_headers: List[str]
    a list of column headers of the dataframe

  removed_noise_df: pd.DataFrame
    a dataframe which was has been partially cleaned and is subsequently cleaned within this functions  
  """
  col_headers[0] = 'date'
  removed_noise_df.columns = col_headers
  removed_noise_df['date'] = [datetime.datetime.strptime(x.split('-')[1].split(' ')[0] + f' {extract_year(x)}', '%b %Y').date()
                     for x in removed_noise_df.loc[:, 'date']]
  removed_noise_df.rename(columns={'Other2': 'Other', 'Discouraged workers1': 'Discouraged workers'}, inplace=True)
  return removed_noise_df


## Alternative approach for more automated approach and update the dashbooard to point to this output

# def extract_load_transform_dataframe() -> typing.Union[dict[str, pd.DataFrame], ValueError]:
#   output = requests.get('https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peoplenotinwork/economicinactivity/datasets/economicinactivitybyreasonnotseasonallyadjustedinac01nsa/current/inac01nsamar2024.xls')
#   if output.status_code != 200:
#     raise ValueError(f'Bad request: Expected Data not sent correctly')
#   else:
#     df = pd.read_excel(io.BytesIO(output.content), 
#                       sheet_name=None, 
#                       skiprows=4,
#                       na_values=['..'])
#     df.pop('Note', None)
#     for sheet_name, dataframe in df.items():
#        cols = dataframe.loc[0]
#        dataframe = dataframe.loc[4:, :]
#        df[sheet_name] = transform_dataframe_for_analysis(cols, dataframe).loc[:, :'Wants a job (thousands)'].dropna()
#     return df
    
##
