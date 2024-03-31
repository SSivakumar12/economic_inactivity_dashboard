import pytest
import datetime
import pandas as pd
from typing import Union
from src.processing import pre_process_data


@pytest.fixture
def mock_excel_read(mocker, mock_dataframe):
    dataframe = mocker.patch('src.processing.pre_process_data.pd.read_excel', 
                             return_value=mock_dataframe)
    return dataframe


def test_load_and_transform_dataframe(mock_excel_read) -> Union[None, AssertionError]:
    actual = pre_process_data.load_and_transform_dataframe('filename', 'sheet_name')

    expected_df = pd.DataFrame({
        'date': [datetime.date(2023, 2, 1)]*6,
        'foo': ['foo']*6,
        'bar' : ['bar']*6})

    mock_excel_read.assert_called_once_with(
        'filename',
        sheet_name='sheet_name',
        skiprows=4,
        na_values=['..'],
    )
    pd.testing.assert_frame_equal(actual.reset_index(drop=True), expected_df)


def test_extract_most_recent_data() -> Union[None, AssertionError]:
    assert '.xls' in pre_process_data.extract_most_recent_data()
