import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json

import yfinance as yf
from scripts.functions import stock_chart

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

period_list = ['1d', '1mo', '3mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H4("STOCK INFO VISUALIZER DEMO",
            style={'textAlign': 'center', 'color': colors['text']}
            ),
    html.Div(["Stock Ticker ",
              dcc.Input(id='ticker', value='AAPL', type='text')
              ],
             style={'color': colors['text'], 'textAlign': 'center'}
             ),
    html.Br(),
    html.Div(["Time Period",
              dcc.Dropdown(
                  id='period',
                  options=[{'label': i, 'value': i} for i in period_list],
                  value='3mo'
              )
            ], style={'width': '20%',
                      'color': colors['text'],
                      'textAlign': 'left',
                      'align-items': 'center',
                      'padding-left':'40%',
                      }),
    dcc.Graph(id='stock-chart'),
    html.Div(id='hover-data', style={'color': colors['text'], 'textAlign': 'center'}),

])




@app.callback(
    Output('stock-chart', 'figure'),
    [Input('ticker', 'value'),
     Input('period', 'value')])
def update_figure(ticker, period):

    obj = yf.Ticker(ticker)
    fig = stock_chart(stock_object=obj, period=period)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

@app.callback(
    Output('hover-data', 'children'),
    [Input('stock-chart', 'hoverData')])
def display_hover_data(hoverData):
    if hoverData is None:
        return ''
    else:
        return 'PRICE {} at {}'.format(hoverData['points'][0]['y'], hoverData['points'][0]['x'])

if __name__ == '__main__':
    app.run_server(debug=True)