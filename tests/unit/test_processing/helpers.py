import typing
import plotly.graph_objects as go

def plotly_assertions(fig: go.Figure,
                      items: typing.Dict[str, str]) -> typing.Union[None, AssertionError]:
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == items.get('length', 0)
    assert fig.layout.title.text == items.get('title', '')
    assert list(fig.data[0].x) == items.get('x_data', [])
    assert list(fig.data[0].y) == items.get('y_data', [])
