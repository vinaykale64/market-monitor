import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import yfinance as yf
from functions import stock_chart

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




@app.callback(
    Output('stock-chart', 'figure'),
    [Input('ticker', 'value'),
     Input('period', 'value')])
def update_figure(ticker, period):

    obj = yf.Ticker(ticker)
    fig = stock_chart(stock_object=obj, period=period)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)