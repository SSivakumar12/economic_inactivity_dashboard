import typing
import datetime
import pandas as pd
import plotly.graph_objects as go

from .pre_process_data import (extract_most_recent_data,
                              load_and_transform_dataframe)


RECENT_FILE_PATH: str = extract_most_recent_data()
DATA: pd.DataFrame = load_and_transform_dataframe(RECENT_FILE_PATH, 'People')
MARKER_COLOURS: typing.List[str] = ['#206095', '#27a0cc', '#003c57', '#118c7b', 
                                    '#a8bd3a', '#871a5b', '#f66068', '#746cb1', 
                                    '#22d0b6']

def total_economic_activty_overtime() -> go.Figure:

    labels: typing.Dict[str, str] = {
    "xaxis_title": "Date", 
    "yaxis_title": "Number",
    "title": "Number of economic inactivity aged 16-64 overtime"}

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=DATA['date'], 
                             y=DATA['Total economically inactive aged 16-64 (thousands)'],
                  marker_color=MARKER_COLOURS, name='Economic inactivity'))
    fig.update_layout(**labels)
    return fig


def breakdown_reason_of_economic_inactivity() -> go.Figure:

    labels: typing.Dict[str, str] = {
    "xaxis_title": "Date", 
    "yaxis_title": "Count of economic inactivity",
    "title": "breakdown of reason for economic activity overtime"}
    data_copy = pd.concat([DATA.iloc[:, 2:9], DATA['date']], axis=1)
    data_window = data_copy[data_copy['date'] >= datetime.date(1993, 5, 1)]
    columns = [x for x in data_window.columns if x != 'date']
    
    fig = go.Figure()
    for colour, column in zip(MARKER_COLOURS, columns):
        fig.add_trace(go.Scatter(x=data_window['date'], y=data_window[column], 
                                 marker_color=colour, name=column))
    fig.update_layout(**labels)
    return fig