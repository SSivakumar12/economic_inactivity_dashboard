import pytest
import datetime
import pandas as pd
from typing import Union
from src.processing import utils_fn


@pytest.mark.parametrize("test_input,expected", 
                         [("2024 is the year", "2024"), 
                          ("no numbers here...", None), 
                          # so far in the future that we can ignore this case
                          ("20101 is an edgecase", "2010")])
def test_extract_year(test_input: str, expected: str) -> Union[None, AssertionError]:
    assert utils_fn.extract_year(test_input) == expected


def test_filter_out_unwanted_rows(mock_dataframe: pd.DataFrame) -> Union[None, AssertionError]:
    expected_df = pd.DataFrame({
        'Unnamed: 0': ['Dec-Feb 2023']*6,
        'Other2': ['foo']*6,
        'Discouraged workers1': ['bar']*6})
    actual_df = utils_fn.filter_out_unwanted_rows(mock_dataframe).reset_index(drop=True)

    pd.testing.assert_frame_equal(expected_df, actual_df)


def test_transform_dataframe_for_analysis(mock_dataframe: pd.DataFrame) -> Union[None, AssertionError]:
    expected_df = pd.DataFrame({
        'date': [datetime.date(2023, 2, 1)]*6,
        'Other': ['foo']*6,
        'Discouraged workers': ['bar']*6})
    actual_df =\
        utils_fn.transform_dataframe_for_analysis(
            list(mock_dataframe.columns), 
            utils_fn.filter_out_unwanted_rows(mock_dataframe))
    
    pd.testing.assert_frame_equal(
        expected_df, 
        actual_df.reset_index(drop=True))
    