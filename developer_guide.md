# Developer guide for market-monitor

This is a short developer guide for anybody planning to develop an app like market-monitor. 
The app is pretty light-weight with 2 core files containing most of the code. Instead of restating 
everything, I have added links where there is better info available. Let's dive in.

## Functions

There are 3 core functions that play with the APIs to generate content for the 3 main pages.
All of them lie in `~/scripts/functions.py` file. Go through the in-depth docstrings (by clicking on function name) to learn more about it.

Use | Function | Description
------------ | ------------- | ---
Stocks | [`stock_chart(stock_object, period)]`](https://github.com/vinaykale64/market-monitor/blob/master/scripts/functions.py#L4) | Returns an interactive dash plot of stock price against time periods.
Options | [`options_table(stock_object, date, kind)`](https://github.com/vinaykale64/market-monitor/blob/master/scripts/functions.py#L71) | Returns the options info of a stock on any given date in tabular format.
News | [`get_news_markdown(ticker_symbol, count)`](https://github.com/vinaykale64/market-monitor/blob/master/scripts/functions.py#L180) | Returns a markdown text string which has `count` top news sources.

## Learning Dash

Dash is a great tool to create interactive apps using Python. I have found it very user-friendly and easy to pick up. 
Following are great links to get started on it.

* [Dash Tutorial](https://dash.plotly.com/installation)
* [Dash Core Componenets (DCC)](https://dash.plotly.com/dash-core-components )
* [Dash Gallery](https://dash-gallery.plotly.host/Portal/)

## Installation and Deployment

### Step 1: 
Create a new conda environment. I am using python 3.6 and setting env name as 
`market-monitor`. Once created activate the environment.

``` bash
  conda create -n market-monitor python=3.6 -y
  source activate market-monitor
```

### Step 2: 
Install requirements listed out in the `requirements.txt` file.

``` bash
  pip install -r requirements.txt
```

### Step 3: 
Run the app locally 
``` bash
  python stock_chart_app.py
```

Now that you have it running locally, feel free to make some changes and play with the code. 


Once you feel you want to deploy your own app, we need to use a platform to deploy it on. 
[Heroku](https://www.heroku.com/) is one such platform as a service (PaaS) option that enables developers to build, r
un, and operate applications entirely in the cloud. They let you host one app for free which should be enough.

Dash already has a great tutorial on how-to host your dash app on Heroku so I will just link it here.

* [Dash Heroku Deployment Guide](https://dash.plotly.com/deployment)

That's about it.   
Please reach out if you have any more questions.

