import plotly.graph_objects as go
import pandas as pd
import datetime
from .plotly_visuals import WOMEN_DATA, MEN_DATA
from .base_plotly_visuals import MARKER_COLOURS




def visualise_gender_breakdown():
    women_specific_trends = pd.concat([WOMEN_DATA.iloc[:, 1: 11], WOMEN_DATA['date']], axis=1)
    women_specific_trends = women_specific_trends[women_specific_trends['date'] >= datetime.date(1993, 5, 1)]

    men_specific_trends = pd.concat([MEN_DATA.iloc[:, 1: 11], MEN_DATA['date']], axis=1)
    men_specific_trends = men_specific_trends[men_specific_trends['date'] >= datetime.date(1993, 5, 1)]
    desired_columns = list(men_specific_trends.iloc[:, 1:8].columns)
    fig = go.Figure()
    # Add traces for men
    for colour, column in zip(MARKER_COLOURS[1:], desired_columns):
        fig.add_trace(go.Scatter(x=women_specific_trends['date'], y=women_specific_trends[column],
                                marker_color=colour, name=f'women_{column}'))
    
    for colour, column in zip(MARKER_COLOURS[1:], desired_columns):
        fig.add_trace(go.Scatter(x=men_specific_trends['date'], y=men_specific_trends[column],
                                marker_color=colour, name=f'men_{column}'))

    fig.update_layout(
    title="Breakdown of reasons for economic inactivity by Gender",
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="all",
                     method="update",
                     args=[{"visible": [True]*len(desired_columns)*2},
                           {"title": "Breakdown of reasons for economic inactivity by Gender"}]),
                dict(label="women",
                     method="update",
                     args=[{"visible": [True]*len(desired_columns) + [False]*len(desired_columns)},
                           {"title": "Breakdown of reassons of economic inactivity within women"}]),
                dict(label="men",
                     method="update",
                     args=[{"visible": [False]*len(desired_columns) + [True]*len(desired_columns)},
                           {"title": "Breakdown of reassons of economic inactivity within men"}])

            ]),
        )
    ])
    return fig
