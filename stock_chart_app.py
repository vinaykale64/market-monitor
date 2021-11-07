import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pickle

import yfinance as yf
from scripts.functions import stock_chart, options_table, get_news_markdown

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

period_list = ["1d", "1mo", "3mo", "1y", "2y", "5y", "10y", "ytd", "max"]
colors = {"background": "#FFFFFF", "text": "#000000"}
ticker_options = pickle.load(open( "dropdown_options.p", "rb" ) )

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H2(
            "market monitor",
            style={"textAlign": "center", "color": colors["text"], "fontSize": 42, "font-weight": "bold"},
        ),
        html.Br(),

        html.Label(
            ["Search for a company to start (Use CAPS for ticker e.g. AAPL)",
             dcc.Dropdown(id="my-dynamic-dropdown", placeholder="Apple Inc. (AAPL)", value="AAPL")
             ],
            style={"color": colors["text"],
                   "textAlign": "center",
                   "fontSize": 18,
                   "width": '30%',
                   "padding-left": "35%"}
        ),

        html.Br(),
        html.Br(),

        dcc.Tabs([
            dcc.Tab(label='Stocks', children=[
                html.Br(),
                html.Div([

                    html.Div(
                        id="hover-data",
                        style={"color": colors["text"],
                               "fontSize": 48,
                               "padding-left": "5%",
                               "font-weight": "bold"},
                        className="six columns"
                    ),

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
                            "width": "45%",
                            "color": colors["text"],
                            "textAlign": "left",
                            "padding-left": "30%",
                        },
                        className="six columns"
                    ),
                ], className="row"),

                dcc.Graph(
                    id='stock-chart',
                    style={
                        "padding-left": "5%",
                        "padding-right": "5%"
                    }
                ),

                html.Div(
                    [html.P("(Hover over the graph to get precise info)")],
                    style={"textAlign": "center"},
                ),
            ]),
            dcc.Tab(label='Options', children=[
                html.Br(),
                html.Br(),
                html.Div(
                    ["Select Date of Expiry", dcc.Dropdown(id="options-dates-dropdown")],
                    style={
                        "color": colors["text"],
                        "textAlign": "left",
                        "align-items": "center",
                        "padding-left": "32.5%",
                        "width": "15%",
                        "display": "inline-block",
                    },
                ),
                html.Div(
                    [
                        "Select Type",
                        dcc.Dropdown(
                            id="options-kind-dropdown",
                            options=[
                                {"label": "Calls", "value": "calls"},
                                {"label": "Puts", "value": "puts"},
                            ],
                            value="calls",
                        ),
                    ],
                    style={
                        "color": colors["text"],
                        "textAlign": "left",
                        "align-items": "center",
                        "padding-left": "5%",
                        "width": "15%",
                        "display": "inline-block",
                    },
                ),
                html.Br(),
                html.Br(),
                dcc.Graph(id="options-table", style={"padding-left": "5%", "padding-right": "5%"}),
            ]),
            dcc.Tab(label='Latest News', children=[
                html.Br(),
                html.Br(),
                dcc.Markdown(
                    id='news-markdown',
                    style={"white-space": "pre", "padding-left": "5%", "width": "15%", "fontSize": 18,}
                ),
            ]),
        ], style={"fontSize": 24}
        ),
        html.Br(),
        dcc.Markdown(
        """
        Created in Python. [Github Repo.](https://github.com/vinaykale64/stocks_visualizer)
        """,
            style={"textAlign": "center"}
        ),
        html.Br(),
    ],
)


@app.callback(
    dash.dependencies.Output("my-dynamic-dropdown", "options"),
    [dash.dependencies.Input("my-dynamic-dropdown", "search_value")],
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in ticker_options if search_value in o["label"]]


@app.callback(
    dash.dependencies.Output("options-dates-dropdown", "options"),
    [Input("my-dynamic-dropdown", "value")],
)
def get_possible_dates(ticker):

    obj = yf.Ticker(ticker)
    return [{"label": i, "value": i} for i in obj.options]



@app.callback(
    dash.dependencies.Output("options-dates-dropdown", "value"),
    [Input("my-dynamic-dropdown", "value")],
)
def get_default_dates(ticker):
    obj = yf.Ticker(ticker)
    try:
        return obj.options[0]
    except:
        return ''


@app.callback(
    Output("stock-chart", "figure"),
    [Input("my-dynamic-dropdown", "value"), Input("period", "value")],
)
def update_figure(ticker, period):

    obj = yf.Ticker(ticker)
    fig = stock_chart(stock_object=obj, period=period)
    fig.update_layout(
        height=600
    )
    return fig


@app.callback(
    Output("options-table", "figure"),
    [
        Input("my-dynamic-dropdown", "value"),
        Input("options-dates-dropdown", "value"),
        Input("options-kind-dropdown", "value"),
    ],
)
def update_table(ticker, date, kind):

    obj = yf.Ticker(ticker)
    fig = options_table(stock_object=obj, date=date, kind=kind)
    return fig


@app.callback(Output("hover-data", "children"),
              [Input("stock-chart", "hoverData"),
               Input("stock-chart", "figure"),
               Input("my-dynamic-dropdown", "value")]
             )
def display_hover_data(hoverData, figure, ticker):

    obj = yf.Ticker(ticker)
    if hoverData is None:
        return obj.ticker + ' ' + str(figure['data'][0]['y'][-1])
    else:
        return "{} {}".format(obj.ticker, round(hoverData["points"][0]["y"],2))


@app.callback(Output("news-markdown", "children"),
              [Input("my-dynamic-dropdown", "value")]
             )
def return_news(ticker):
    return get_news_markdown(ticker, 15)



if __name__ == "__main__":
    app.run_server(debug=True)
