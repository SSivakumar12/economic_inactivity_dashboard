import typing
import datetime
import pandas as pd
import plotly.graph_objects as go

from .pre_process_data import (extract_most_recent_data,
                              load_and_transform_dataframe)

from .base_plotly_visuals import (add_colour_contrast, 
                                  create_time_series_visual,
                                  MARKER_COLOURS)

RECENT_FILE_PATH: str = extract_most_recent_data()
DATA: pd.DataFrame = load_and_transform_dataframe(RECENT_FILE_PATH, 'People')
MEN_DATA: pd.DataFrame = load_and_transform_dataframe(RECENT_FILE_PATH, 'Men')
WOMEN_DATA: pd.DataFrame = load_and_transform_dataframe(RECENT_FILE_PATH, 'Women')


def total_economic_activty_overtime(data: pd.DataFrame=DATA) -> go.Figure:

    labels: typing.Dict[str, str] = {
    "xaxis": {"title":"Date", "showgrid": False}, 
    "yaxis": {"title":"Number", "showgrid":False},
    "paper_bgcolor": "rgba(255,255,255,1)",
    "title": "Number of economic inactivity aged 16-64 overtime"}

    fig = create_time_series_visual(df=data, 
                                    column=['Total economically inactive aged 16-64 (thousands)'], 
                                    labels=labels)
    fig = add_colour_contrast(fig, data, 'Total economically inactive aged 16-64 (thousands)',
                              'Total economically inactive aged 16-64 (thousands)')

    return fig


def breakdown_reason_of_economic_inactivity(
        title: str,
        column: str,
        data: pd.DataFrame=DATA) -> go.Figure:

    labels: typing.Dict = {
    "xaxis": {"title":"Date", "showgrid": False}, 
    "yaxis": {"title":"Number of economic inactivity", "showgrid":False},
    "paper_bgcolor": "rgba(255,255,255,1)",
    "title": title}
    
    data_copy = pd.concat([data.iloc[:, 2:9], data['date']], axis=1)
    data_window = data_copy[data_copy['date'] >= datetime.date(1993, 5, 1)]
    columns = [x for x in data_window.columns if x != 'date']
    
    fig = create_time_series_visual(df=data_copy, 
                                    column=columns, 
                                    labels=labels)
    fig = add_colour_contrast(fig, data_window, 0, column)
    return fig


def economic_inactivity_wanting_a_job(data: pd.DataFrame=DATA) -> go.Figure:
    labels: typing.Dict = {
    "xaxis": {"title": "Year", "showgrid":False},
    "yaxis": {"title":"Number of economically inactive", "showgrid": False},
    "title": "Number of economic inactive respondents wanting a job overtime",
    "paper_bgcolor": "rgba(255,255,255,1)"}

    job_desire_breakdown = pd.concat([data.iloc[:, 9:11], data['date']], axis=1)
    job_desire_breakdown =\
        job_desire_breakdown[job_desire_breakdown['date'] >= datetime.date(1993, 5, 1)]
    columns = [x for x in job_desire_breakdown.columns if x != 'date']

    fig = create_time_series_visual(fig=go.Figure(),
                                    df=job_desire_breakdown,
                                    column=columns,
                                    labels=labels)
    # fig = add_colour_contrast(fig, 
    #                           job_desire_breakdown, 
    #                           int(min(job_desire_breakdown['Wants a job (thousands)']) - 500_000),
    #                           int(max(job_desire_breakdown['Does not want job (thousands)']) + 500_000))
    return fig

def breakdown_of_economic_inactivity_by_gender(men_data:pd.DataFrame=MEN_DATA,
                                               women_data: pd.DataFrame=WOMEN_DATA
                                               ) -> go.Figure:
    labels: typing.Dict = {
        "xaxis": {"title": "Year", "showgrid": False},
        "yaxis": {"title":"Number of economically inactive", "showgrid": False},
        "title": "breakdown of economic inactivty overtime by gender",
        "paper_bgcolor": "rgba(255,255,255,1)"}
    cols = 'Total economically inactive aged 16-64 (thousands)'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=men_data["date"],
                             y=men_data[cols],
                             marker_color=MARKER_COLOURS[0],
                             name="Men"))
    fig.add_trace(go.Scatter(x=women_data["date"],
                             y=women_data[cols],
                             marker_color=MARKER_COLOURS[1],
                             name="Women"))
    fig.add_shape(type='rect',
                  x0=datetime.date(2022, 7, 1), 
                  y0=min(men_data[cols]) - 500_000,
                  x1=max(men_data['date']), 
                  y1=max(women_data[cols]) + 500_000,
                  line=dict(color='rgba(0,0,0,0)', width=0),
                  fillcolor='rgba(200,200,200,0.3)')
    fig.update_layout(**labels)
    return fig
