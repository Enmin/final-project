import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from pymongo import MongoClient
import pandas as pd
import sys
sys.path.append("..")
from src.prepare_data import get_covid_case, get_stock_data

# from database import fetch_all_bpa_as_df

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(637,657,687)', 'rgb(80,80,80)', 'rgb(100,100,100)', 'rgb(115,115,115)', 'rgb(135,67,69)',
          'rgb(189,189,189)', 'rgb(67,80,100)', 'rgb(123,33,67)', 'rgb(138,45,69)', 'rgb(167,167,167)',
          'rgb(87,67,87)', 'rgb(67,67,67)', 'rgb(49,130,189)', 'rgb(467,67,35)', 'rgb(168,168,168)',
          'rgb(6,33,105)', 'rgb(8,14,215)', 'rgb(47,47,47)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first



def page_header(app):
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('yangyinke', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                              'paddingLeft': '4px', 'color': '#a3a7b0',
                                              'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/yangyinke'),
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # Covid case number and stock price
        Explore the relationship between stock price and covid case number

        ### Data Source
        This project utilizes up-to-date covid case data from [The COVID Tracking Project](https://covidtracking.com/data/national/cases)
        and stock price data from [Yahoo Finance](https://finance.yahoo.com/). 
        All data in the database are **updated every day**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def stock_price_trend():
    """
    Returns description of plots about stock price trend and covid case number
    """
    return html.Div(children=[dcc.Markdown('''

        ### Stock Price Trend
        The plots below are about stock price trend and covid case number. Stocks were divided into three 
        plots based on their corresponding scale.
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def stock_price_fluc():
    """
    Returns description of plots about stock price fluctuation and covid case number
    """
    return html.Div(children=[dcc.Markdown('''

        ### Stock Price Fluctuation
        The plots below are about stock price fluctuation and covid case number. Stocks were divided into three 
        plots based on their types of fluctuation rate
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def static_trend_graph(codes, scale, target, covid_df, stock_df, stack=False):
    """
    Returns a plot of stock price and covid case
    """
    if covid_df is None or stock_df is None:
        return go.Figure()
    fig = go.Figure()

    # plot the trend of close stock price
    for i, code in enumerate(codes):
        df = stock_df[stock_df['code'] == code]
        # df = df[df['date'] >= '2020-01-22']
        fig.add_trace(go.Scatter(x=df['date'], y=df[target], mode='lines', name=code,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))

    # plot the trend of new cases
    if scale == 100:
        name = 'new cases scaled by hundredth'
    elif scale == 1000:
        name = 'new cases scaled by thousandth'
    elif scale == 10:
        name = 'new cases scaled by tenth'
    elif scale == 1000000:
        name = 'new cases scaled by millionth'
    elif scale == 100000:
        name = 'new cases scaled by 1/100,000'
    else:
        name = None
    fig.add_trace(go.Scatter(x=covid_df['date'], y=covid_df['new_case'] / scale, mode='lines', name=name,
                             line={'width': 2, 'color': 'orange'}))

    fig.update_layout(template='plotly_dark',
                      title=None,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='number of new cases/stock price',
                      xaxis_title='Date')
    return fig


def low_stock_price_plot(covid_df, stock_df):
    codes = ['AAPL', 'MSFT', 'FB', 'WMT', 'GE', 'MMM', 'AMT', 'JNJ', 'PFE', 'JPM', 'V', 'XOM', 'CL=F']
    fig = static_trend_graph(codes, 1000, 'close', covid_df, stock_df, stack=False)
    fig.update_layout(title='cheap stock price & number of new cases')
    return fig


def exp_stock_price_plot(covid_df, stock_df):
    codes = ['GOOG', 'AMZN', '^GSPC', 'GC=F', ]
    fig = static_trend_graph(codes, 100, 'close', covid_df, stock_df, stack=False)
    fig.update_layout(title='expensive stock price & number of new cases')
    return fig


def dj_plot(covid_df, stock_df):
    codes = ['^DJI', ]
    fig = static_trend_graph(codes, 10, 'close', covid_df, stock_df, stack=False)
    fig.update_layout(title='Dow Jones Industrial Average & number of new cases')
    return fig


def stock_price_fluc_plot(covid_df, stock_df):
    codes = ['AAPL', 'MSFT', 'GOOG', 'FB', 'AMZN', 'WMT', 'GE', 'MMM', 'AMT', 'JNJ', 'PFE', 'JPM', 'V', 'XOM']
    fig = static_trend_graph(codes, 1000000, 'fluctuation', covid_df, stock_df, stack=False)
    fig.update_layout(yaxis_title='number of new cases/fluctuation percentage',
                      title='stock price fluctuation percentage & number of new cases')
    return fig


def market_index_fluc_plot(covid_df, stock_df):
    codes = ['^GSPC', '^DJI', 'GC=F']  # , 'CL=F']
    fig = static_trend_graph(codes, 1000000, 'fluctuation', covid_df, stock_df, stack=False)
    fig.update_layout(yaxis_title='number of new cases/fluctuation percentage',
                      title='market index fluctuation percentage & number of new cases')
    return fig


def co_fluc_plot(covid_df, stock_df):
    codes = ['CL=F']
    fig = static_trend_graph(codes, 100000, 'fluctuation', covid_df, stock_df, stack=False)
    fig.update_layout(yaxis_title='number of new cases/fluctuation percentage',
                      title='Crude Oil Jan 21 fluctuation percentage & number of new cases')
    return fig


def dynamic_layout(app):
    # get data first
    covid_df = get_covid_case()
    stock_df = get_stock_data()

    return html.Div([
        page_header(app),
        html.Hr(),
        description(),
        stock_price_trend(),
        # dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        dcc.Graph(id='stock_price1', figure=low_stock_price_plot(covid_df, stock_df)),
        dcc.Graph(id='stock_price2', figure=exp_stock_price_plot(covid_df, stock_df)),
        dcc.Graph(id='stock_price3', figure=dj_plot(covid_df, stock_df)),
        stock_price_fluc(),
        dcc.Graph(id='stock_fluc1', figure=stock_price_fluc_plot(covid_df, stock_df)),
        dcc.Graph(id='stock_fluc2', figure=market_index_fluc_plot(covid_df, stock_df)),
        dcc.Graph(id='stock_fluc3', figure=co_fluc_plot(covid_df, stock_df)),
        # what_if_description(),
        # what_if_tool(),
        # architecture_summary(),
    ], className='row', id='content')


if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.run_server(debug=True, port=1050, host='0.0.0.0')
