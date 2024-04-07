"""
the base functions for plotly visuals
"""
import typing
import datetime
import pandas as pd
import plotly.graph_objects as go


MARKER_COLOURS: typing.List[str] = ['#206095', '#27a0cc', '#003c57', '#118c7b', 
                                    '#a8bd3a', '#871a5b', '#f66068', '#746cb1', 
                                    '#22d0b6']


def create_time_series_visual(df: pd.DataFrame,
                              column: typing.List[str],
                              labels: typing.Dict) -> go.Figure:
    fig = go.Figure()
    for colour, column in zip(MARKER_COLOURS, column):
        fig.add_trace(go.Scatter(x=df['date'], y=df[column], 
                                 marker_color=colour, name=column))
    fig.update_layout(**labels)
    return fig


def add_colour_contrast(fig: go.Figure, 
                        df: pd.DataFrame, 
                        col1: typing.Union[str, int], 
                        col2: str) -> go.Figure:
    """
    Adds a grey colour contrast to highlight the data quality issues
    as well as the step change in continuity in counts from July-Sep 22
    parameters
    ---------
    fig: go.Figure
        a plotly figure to update
    df: pd.DataFrame
        the dataframe which contains the economic inactivity
    col1: str|int
        if type int it sets the minimum point of shape to 0
    col2: str
        the column which contains the largest count of economic inactivity
    
    returns
    -------
    go.Figure

    """
    if isinstance(col1, str):
        y_0 = min(df[col1]) -500_000 if min(df[col1]) >= 500_000 else 0
    else:
        y_0 = col1
    
    fig.add_shape(type='rect',
              x0=datetime.date(2022, 7, 1), y0=y_0,
              x1=max(df['date']), y1=max(df[col2]) + 500_000,
              line=dict(color='rgba(0,0,0,0)', width=0),
              fillcolor='rgba(180,180,180,0.5)')
    return fig


def bar_chart(df: pd.DataFrame, 
              col: typing.List[str], 
              labels: typing.Dict[str, str]) -> go.Figure:
    pass