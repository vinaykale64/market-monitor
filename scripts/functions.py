import plotly.graph_objects as go

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