import plotly.graph_objects as go
import pandas as pd
import json
from plotly import io
import plotly.utils
def create_plot(name):
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    df = pd.read_csv('datasets/daily/{}.csv'.format(name))

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'])
                        ])

    fig.update_layout(
        title='CandleStick Chart',
        yaxis_title=name,
        shapes = [dict(
            x0='2021-06-01', x1='2021-06-01', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x='2021-06-01', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='Increase Period Begins')]
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
    fig.show()
    # div = io.to_html.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)
    # return div
# create_plot('ACC.NS')
# print(div)