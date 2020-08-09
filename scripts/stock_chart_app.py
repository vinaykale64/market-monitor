import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yf

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

period_list = ['1d', '1mo', '3mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

app.layout = html.Div([
    html.H6("STOCK INFO VISUALIZER DEMO"),
    html.Div(["Stock Ticker Symbol: ",
              dcc.Input(id='ticker', value='AAPL', type='text')]),
    html.Div(["Time Period: ",
              dcc.Dropdown(
                  id='period',
                  options=[{'label': i, 'value': i} for i in period_list],
                  value='3mo'
              )
            ]),
    html.Br(),
    dcc.Graph(id='stock-chart'),

])


def stock_chart(stock_object, period, kind='interactive'):
    period_list = ['1d', '1mo', '3mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if period not in period_list:
        raise KeyError("Incorrect period specified. Allowed list: "
                       "['1d','1mo','3mo','1y','2y','5y','10y','ytd','max']")

    # Intervals set similar to RH policy
    if period == '1d':
        interval = '5m'
    else:
        interval = '1d'

    data = stock_object.history(period=period, interval=interval)
    plot_title = 'Stock: {}, Time Period: {}'.format(stock_object.ticker, period)

    fig = go.Figure(
        data=go.Scatter(y=data['Close'],
                        x=data.index,
                        line=dict(color='chartreuse', width=4)
                        ),

    )

    fig.add_layout_image(
        dict(
            source=stock_object.info['logo_url'],
            xref="paper", yref="paper",
            x=1, y=1.05,
            sizex=0.2, sizey=0.2,
            xanchor="left", yanchor="bottom"
        )
    )

    fig.update_layout(title=plot_title,
                      xaxis_title='Date',
                      yaxis_title='Closing Price',
                      template='plotly_dark',
                      xaxis_showgrid=False,
                      yaxis_showgrid=False
                      )

    if kind == 'interactive':
        #fig.show()
        return fig
    if kind == 'static':
        #fig.show("png")
        return fig

@app.callback(
    Output('stock-chart', 'figure'),
    [Input('ticker', 'value'),
     Input('period', 'value')])
def update_figure(ticker, period):
    #filtered_df = df[df.year == selected_year]
    #fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
    #                 size="pop", color="continent", hover_name="country",
    #                 log_x=True, size_max=55)
    #fig.update_layout(transition_duration=500)

    obj = yf.Ticker(ticker)
    fig=stock_chart(stock_object=obj, period=period)


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)