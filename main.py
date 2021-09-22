import plotly.graph_objects as go
import numpy as np
from scipy.misc import derivative
import dash
from dash import dcc
from dash import html


def f(x):
    return np.log(x)


def f_line(f, x, x_n):
    slope = derivative(f, x_n, dx=0.1)
    x_nn = x_n - f(x_n) / slope
    return slope * (x - x_n) + f(x_n), x_nn


x = np.linspace(0.2, 2.2, 500)

trace = go.Scatter()
trace1 = go.Scatter()
trace2 = go.Scatter(x=x, y=f(x))

g = go.FigureWidget(data=[trace, trace1, trace2],
                    layout=go.Layout(
                        title=dict(
                            text='Newton'
                        ),
                        barmode='overlay',
                        xaxis=go.layout.XAxis(range=[0.2, 2.2]),
                        yaxis=go.layout.YAxis(range=[-1, 1]),
                        height=500,
                        width=500,

                    ))


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    style={'width': '50%', 'float': 'left', 'marginLeft': 20, 'marginRight': 20},
    children=[
        dcc.Graph(figure=g, id='graph'),
        dcc.Slider(id='slider', min=1, max=6, value=1, step=1),
    ])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    x_n = 2

    for i in range(0, value):
        f_l, x_n = f_line(f, x, x_n)

    with g.batch_update():
        g.data[0].x = x
        g.data[0].y = f_l

        g.data[1].x = [x_n, x_n]
        g.data[1].y = [0, f(x_n)]

        g.layout.barmode = 'overlay'
        g.layout.xaxis.title = 'X'
        g.layout.yaxis.title = 'Y'

    return g


if __name__ == '__main__':
    app.run_server(debug=True)
