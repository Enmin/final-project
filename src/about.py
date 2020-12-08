import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from pymongo import MongoClient
import pandas as pd


def about_page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('About Page', style={'text-align': 'center'})],
                 className="ten columns"),
    ], className="row")


def about_page():
    """
    Returns cotents on about page
    """
    return html.Div(children=[dcc.Markdown('''
        ### Project Summary
        The big idea of this project is to analyze the potential impact of covid case number on the change in stock market.        
        The project is constituted of 3 parts:     
        1. Collect stock price information from open source websites. Collect COVID data from open source websites.      
        2. Make data analysis on the relationship between covid case number and stock price.       
        3. We might be able to find the relationship between the change of stock prices and covid case number. At the end of the 
        project, we will build machine learning models to do predictions on the  stock price based on COVID data.        

        ### Team members.   
        Yangyin Ke: yangyin_ke@brown.edu      
        Huaqi Nie: huaqi_nie@brown.edu       
        Enmin Zhou: enmin_zhou@brown.edu       
        ### Possible Next Step
        Considering that the stock market under pandemic is influced by various features, we are thinking
        about adding more features to our model to do more accurate predictions. One of our ideas is to collect 
        some information about major social events such as oil war, persident election and covid-19 vaccine. We 
        plan to do NLP on the content of news and apply it to our model-building.      
        ### References
        1. Afees A. Salisu and Xuan Vinh Vo, Predicting stock returns in the presence of COVID-19 pandemic: The role of health news , 2020 Oct, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7322492/           
        2. Andrea Ialenti, The Coronavirus Effect on the Stock Market, Mar 2020, https://towardsdatascience.com/the-coronavirus-effect-on-the-stock-market-b7a4739406e8     
        3. Asim Kumer Dey, Toufiqul Haq, Kumer Das, Irina Panovska, Quantifying the impact of COVID-19 on the US stock market: An analysis from multi-source information, Aug 2020, https://arxiv.org/abs/2008.10885      
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")