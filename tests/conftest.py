# fixtures that are re-used in multiple tests.
import pytest
import pandas as pd


@pytest.fixture
def mock_dataframe() -> pd.DataFrame:
    mock_dates = ['', '', '', 'Dataset identifier code', 
                  'Dec-Feb 2023', 'Dec-Feb 2023', 
                  'Dec-Feb 2023', 'Dec-Feb 2023', 
                  'Dec-Feb 2023', 'Dec-Feb 2023', 
                  'Dec-Feb 2023', '','Note: ',
                  '', '', '']
    df = pd.DataFrame({
        'Unnamed: 0': mock_dates,
        'Other2': ['foo']*len(mock_dates),
        'Discouraged workers1': ['bar']*len(mock_dates)
    })
    return df