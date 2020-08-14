import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import yfinance as yf
from scripts.functions import stock_chart, options_table

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

period_list = ["1d", "1mo", "3mo", "1y", "2y", "5y", "10y", "ytd", "max"]
colors = {"background": "#FFFFFF", "text": "#000000"}

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H4(
            "STOCK INFO VISUALIZER",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            [
                "Enter Stock Ticker Symbol ",
                dcc.Input(id="ticker", value="AAPL", type="text"),
            ],
            style={"color": colors["text"], "textAlign": "center"},
        ),
        html.Br(),
        html.Div(
            [
                "Select Time Period",
                dcc.Dropdown(
                    id="period",
                    options=[{"label": i, "value": i} for i in period_list],
                    value="3mo",
                ),
            ],
            style={
                "width": "20%",
                "color": colors["text"],
                "textAlign": "left",
                "align-items": "center",
                "padding-left": "40%",
            },
        ),
        html.Div(
            id="hover-data",
            style={"color": colors["text"], "fontSize": 32, "padding-left": "5%"},
        ),
        dcc.Graph(id="stock-chart"),
        html.Br(),
        html.Div(
                    [
                        "Select Options Date",
                        dcc.Dropdown(id="options-dates-dropdown"),
                    ],
                    style={
                        "width": "20%",
                        "color": colors["text"],
                        "textAlign": "left",
                        "align-items": "center",
                        "padding-left": "40%",
                    },
                ),
        html.Div(
                    [
                        "Select Options Kind",
                        dcc.Dropdown(
                            id='options-kind-dropdown',
                            options=[
                                {'label': 'Calls', 'value': 'calls'},
                                {'label': 'Puts', 'value': 'puts'}
                            ],
                            value='calls'
                        )
                    ],
                    style={
                        "width": "20%",
                        "color": colors["text"],
                        "textAlign": "left",
                        "align-items": "center",
                        "padding-left": "40%",
                    },
                ),
        dcc.Graph(id="options-table"),
    ],
)

@app.callback(
    dash.dependencies.Output('options-dates-dropdown', 'options'),
    [dash.dependencies.Input('ticker', 'value')])
def get_possible_dates(ticker):
    obj = yf.Ticker(ticker)
    return [{'label': i, 'value': i} for i in obj.options]

@app.callback(
    dash.dependencies.Output('options-dates-dropdown', 'value'),
    [dash.dependencies.Input('ticker', 'value')])
def get_default_dates(ticker):
    obj = yf.Ticker(ticker)
    return obj.options[0]


@app.callback(
    Output("stock-chart", "figure"),
    [Input("ticker", "value"), Input("period", "value")],
)
def update_figure(ticker, period):

    obj = yf.Ticker(ticker)
    fig = stock_chart(stock_object=obj, period=period)
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
    return fig


@app.callback(
    Output("options-table", "figure"),
    [Input("ticker", "value"),
     Input("options-dates-dropdown", "value"),
     Input("options-kind-dropdown", "value")
    ],
)
def update_figure(ticker, date, kind):

    obj = yf.Ticker(ticker)
    fig = options_table(stock_object=obj, date=date, kind=kind)
    #fig.update_layout(
    #    plot_bgcolor=colors["background"],
    #    paper_bgcolor=colors["background"],
    #    font_color=colors["text"],
    #)
    return fig


@app.callback(Output("hover-data", "children"), [Input("stock-chart", "hoverData")])
def display_hover_data(hoverData):
    if hoverData is None:
        return "_"
    else:
        return "{}".format(hoverData["points"][0]["y"], hoverData["points"][0]["x"])


if __name__ == "__main__":
    app.run_server(debug=True)
