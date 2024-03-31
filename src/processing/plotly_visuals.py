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




def total_economic_activty_overtime(data=DATA) -> go.Figure:

    labels: typing.Dict[str, str] = {
    "xaxis_title": "Date", 
    "yaxis_title": "Number",
    "title": "Number of economic inactivity aged 16-64 overtime"}

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], 
                             y=data['Total economically inactive aged 16-64 (thousands)'],
                  marker_color=MARKER_COLOURS, name='Economic inactivity'))
    fig = add_colour_contrast(fig, data, 'Total economically inactive aged 16-64 (thousands)',
                              'Total economically inactive aged 16-64 (thousands)')
    fig.update_layout(**labels, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    return fig


def breakdown_reason_of_economic_inactivity(data=DATA) -> go.Figure:

    labels: typing.Dict[str, str] = {
    "xaxis_title": "Year", 
    "yaxis_title": "Count of economic inactivity",
    "title": "breakdown of reason for economic activity overtime"}
    data_copy = pd.concat([data.iloc[:, 2:9], data['date']], axis=1)
    data_window = data_copy[data_copy['date'] >= datetime.date(1993, 5, 1)]
    columns = [x for x in data_window.columns if x != 'date']
    
    fig = go.Figure()
    for colour, column in zip(MARKER_COLOURS, columns):
        fig.add_trace(go.Scatter(x=data_window['date'], y=data_window[column], 
                                 marker_color=colour, name=column))
    fig = add_colour_contrast(fig, data_window, 'Long-term sick', 'Long-term sick')
    fig.update_layout(**labels, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    return fig


def add_colour_contrast(fig: go.Figure, df: pd.DataFrame, col1: str, col2: str) -> go.Figure:
    """
    Adds a grey colour contrast to highlight the data quality issues
    as well as the step change in continuity in counts from July-Sep 22
    parameters
    ---------

    returns
    -------
    go.Figure

    """
    y_0= min(df[col1]) -500_000 if min(df[col1]) >= 500_000 else 0
    fig.add_shape(type='rect',
              x0=datetime.date(2022, 7, 1), y0=y_0,
              x1=max(df['date']), y1=max(df[col2]) + 500_000,
              line=dict(color='rgba(0,0,0,0)', width=0),
              fillcolor='rgba(180,180,180,0.5)')
    return fig
