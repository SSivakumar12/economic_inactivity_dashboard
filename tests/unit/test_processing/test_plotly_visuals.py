import pytest
import plotly.graph_objects as go
import pandas as pd
from src.processing import plotly_visuals
from helpers import plotly_assertions


@pytest.fixture
def mock_file_path_data(mocker):
    """
    mock the dataframe for the purposes of the test
    """
    data = pd.DataFrame({
        'date': [1,2,3],
        'Total economically inactive aged 16-64 (thousands)': [1,2,3]
    })
    mocker.patch('src.processing.plotly_visuals.DATA', 
                 return_value=data)
    return data


def test_total_economic_activty_overtime_visual(mock_file_path_data):
    """
    Test whether plotly visuals render as expected
    """
    fig = plotly_visuals.total_economic_activty_overtime(mock_file_path_data)

    expected_config = {
        'length': 1,
        'title': 'Number of economic inactivity aged 16-64 overtime',
        'xaxis': 'Year',
        'yaxis_title': 'Number',
        'x_data': [1,2,3],
        'y_data': [1,2,3]}
    _ = plotly_assertions(fig, expected_config)

