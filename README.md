# market-monitor

![py27](https://img.shields.io/badge/python-2.7-brightgreen)
![py36](https://img.shields.io/badge/python-3.6%2B-brightgreen)
![black](https://img.shields.io/badge/black--white)
![license](https://img.shields.io/badge/license-MIT-white)

Welcome to github repo of the [market-monitor app](https://stock-app-vk94.herokuapp.com/). Created completely in Python.

This is a dash app which 
- let's user choose a stock/company/ETF from NYSE and NASDAQ exchanges
- shows prices across a chart with customizable time periods (1d/1mo/3mo/1y/2y/5y/10y/ytd)
- shows options info table closest to stock price with color codes (green-ITM, white-OTM)
- any recent news about the underlying organization

Its updated live and uses the [yfinance](https://pypi.org/project/yfinance/), [finviz](https://github.com/mariostoev/finviz) API in backend.

If you want to learn more, please check out the [Developer Guide](https://github.com/vinaykale64/market-monitor/blob/master/developer_guide.md). Feel free to contribute through PR or raise issues. Leave a star if you like the work :)

## Stocks
<img src="images/pic_1.png" width="80%">

## Options
<img src="images/pic_2.png" width="80%">

## News
<img src="images/pic_3.png" width="80%">
