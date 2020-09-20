import plotly.graph_objects as go
import finviz

def stock_chart(stock_object, period):
    """
    Returns an interactive plot of stock price against time period specified.

    Parameters
    ----------

    stock_object: yfinance.ticker.Ticker
        Stock Ticker Object

    period: str
        Time period in str format.
        It can take values ['1d', '1mo', '3mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    Returns
    -------

    fig: plotly.graph_objs._figure.Figure
        Plotly figure object

    """

    period_list = ["1d", "1mo", "3mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    if period not in period_list:
        raise KeyError(
            "Incorrect period specified. Allowed list: "
            "['1d','1mo','3mo','1y','2y','5y','10y','ytd','max']"
        )

    # Intervals set similar to RH policy
    if period == "1d":
        interval = "5m"
    else:
        interval = "1d"

    data = stock_object.history(period=period, interval=interval)

    fig = go.Figure(
        data=go.Scatter(
            y=data["Close"], x=data.index, line=dict(color="chartreuse", width=4)
        ),
    )

    fig.add_layout_image(
        dict(
            source=stock_object.info["logo_url"],
            xref="paper",
            yref="paper",
            x=1,
            y=1.05,
            sizex=0.2,
            sizey=0.2,
            xanchor="left",
            yanchor="bottom",
        )
    )

    fig.update_layout(
        hovermode="x",
        template="presentation",
        #xaxis_showgrid=False,
        yaxis_showgrid=False,
    )

    return fig


def options_table(stock_object, date=None, kind="calls"):
    """
    Returns the info about options of a stock on any given date in tabular format.
    If `date` is not given, it fetches data for the next closest date. If `kind` is
    not specified or None, it returns data for calls.

    Parameters
    ----------

    stock_object: yfinance.ticker.Ticker
        Stock Ticker Object

    date: str, default None
        Date in str format. Should be amony `stock_object.options` list

    kind: str, default `calls`
        Type of options data to return. Takes either `calls` or `puts`

    Returns
    -------

    fig: plotly.graph_objs._figure.Figure
        Plotly table figure object

    """
    try:
        possible_dates = stock_object.options
    except:
        possible_dates = []

    if date is None:
        date = possible_dates[0]
    if date not in possible_dates:
        raise KeyError(
            "Invalid date selected. For available dates, try ticker_object.options"
        )

    if kind == "puts":
        data = stock_object.option_chain(date=date).puts

    else:
        data = stock_object.option_chain(date=date).calls

    data = data[
        [
            "strike",
            "lastPrice",
            "bid",
            "ask",
            "change",
            "percentChange",
            "volume",
            "openInterest",
            "impliedVolatility",
            "inTheMoney",
        ]
    ]

    data.columns = [
        "Strike",
        "Last Price",
        "Bid",
        "Ask",
        "Change",
        "Percent Change",
        "Volume",
        "Open Interest",
        "Implied Volatility",
        "In The Money",
    ]

    price = stock_object.history(period='1d', interval='5m').iloc[[-1]]['Close'][0]
    data = data.iloc[(data['Strike'] - price).abs().argsort()[:10]].sort_values(by=['Strike']).reset_index(drop=True)

    data = data.round(3)
    bold_columns = ["<b>" + x + "</b>" for x in data.columns]

    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[1, 1.1, 1, 1, 1, 1.4, 1.1, 1.4, 1.5, 1.2],
                header=dict(
                    values=bold_columns,
                    fill_color="black",
                    line_color="darkslategray",
                    font=dict(color="white", size=12),
                    align="center",
                ),
                cells=dict(
                    values=data.T.values.tolist(),
                    # fill_color="white",
                    align="center",
                    # font=dict(color="white", size=12),
                    fill=dict(color=[['rgb(127, 255, 0)' if val == True else 'rgb(239, 243, 255)' for val in
                                      data.T.values.tolist()[-1]]])
                ),
            )
        ]
    )
    table_title = "Stock: {}, Date: {}, Kind: {}".format(
        stock_object.ticker, date, kind
    )
    fig.update_layout(
        height=450, title_text=table_title,
    )

    return fig


def get_news_markdown(ticker_symbol, count):
    """
    Returns a markdown text string which has `count` top news sources.

    Parameters
    ----------

    ticker_symbol: str
        Stock Ticker Sumbol Value

    count: int
        Number of news items to return

    Returns
    -------

    joined_str: str
        String containing markdown news sources

    """
    news = finviz.get_news(ticker_symbol)[:count]
    joined_str = ''
    i = 1
    for news_item in news:
        title = news_item[0]
        url = news_item[1]
        joined_str += str(i)+'. [' + title + '](' + url + ')\n'
        i += 1
    return joined_str

