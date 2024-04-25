import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .plotly_visuals import DATA
from .base_plotly_visuals import MARKER_COLOURS


def visualise_summary_stats():
    """
    Generates a 
    """
    
    specific_trends = pd.concat([DATA.iloc[:, 1: 11], DATA['date']], axis=1)
    specific_trends = specific_trends[specific_trends['date'] >= datetime.date(1993, 5, 1)]

    fig = make_subplots(rows=3, 
                        cols=1, 
                        subplot_titles=("Total economic inactivity",
                                        "Breakdown of reasons",
                                        "number of respondents' desire to get a job overtime"), 
                        shared_yaxes=True,
                        vertical_spacing = 0.15
                        )
    
    fig.add_trace(
        go.Scatter(x=list(specific_trends.date), y=specific_trends.iloc[:, 0],
                marker_color='#206095', name='Economic inactivity'
                ),
        row=1, col=1)

    fig.add_shape(type='rect',
            x0=datetime.date(2022, 7, 1), y0=min(specific_trends['Total economically inactive aged 16-64 (thousands)']) - 500_000,
            x1=max(specific_trends['date']), y1=max(specific_trends['Total economically inactive aged 16-64 (thousands)']) + 500_000,
            line=dict(color='rgba(0,0,0,0)', width=0),
            fillcolor='rgba(180,180,180,0.5)')


    for colour, column in zip(MARKER_COLOURS[1:],specific_trends.iloc[:, 1:8].columns):
        fig.add_trace(
            go.Scatter(x=specific_trends['date'], y=specific_trends[column],
                        marker_color=colour, name=column
                        ),
            row=2, col=1)

    fig.add_shape(type='rect',
                x0=datetime.date(2022, 7, 1), y0=0,
                x1=max(specific_trends['date']), y1=max(specific_trends['Long-term sick']) + 500_000,
                line=dict(color='rgba(0,0,0,0)', width=0),
                fillcolor='rgba(180,180,180,0.5)', xref='x2', yref='y2')


    for colour, column in zip([MARKER_COLOURS[0], MARKER_COLOURS[-1]],
                            specific_trends.iloc[:, 8:10].columns):
        fig.add_trace(
            go.Scatter(x=specific_trends['date'], y=specific_trends[column],
                        marker_color=colour, name=column, 
                        ),
            row=3, col=1)

    fig.add_shape(type='rect',
                x0=datetime.date(2022, 7, 1), y0=0,
                x1=max(specific_trends['date']), y1=max(specific_trends['Does not want job (thousands)']) + 500_000,
                line=dict(color='rgba(0,0,0,0)', width=0),
                fillcolor='rgba(180,180,180,0.5)', xref='x3', yref='y3')


    for i in range(len(fig.data)):
        fig.update_xaxes(title_text="Date", row=i+1, col=1)
        fig.update_yaxes(title_text="Number", row=i+1, col=1)


    fig.update_layout(
        xaxis=dict(rangeselector=dict(
            buttons=list([dict(step="year", count=5, label='5-year'),
                        dict(step="year", count=10, label='10-year'),
                        dict(step="year", count=20, label="20-year"),
                        dict(step="all", label="all-time")])),
            type="date",
            title="Date"),
        xaxis2=dict(type="date", title="Date"),
        xaxis3=dict(type="date", title="Date"),
        title="Number of 16-64 individuals that are economically inactive overtime",
        height=1200,
        width=1200,
        # legend_tracegroupgap=250
        )

    fig.update_xaxes(matches='x')

    return fig