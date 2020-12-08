import dash_core_components as dcc
import dash_html_components as html


def detail_header():
    return html.Div(id='header', children=[
        html.Div([html.H3('Project Detail', style={'text-align': 'center'})],
                 className="ten columns"),
    ], className="row")


def detail_page():
    """
    Returns cotents on about page
    """
    return html.Div(children=[dcc.Markdown('''
        ### Datasets Used
        The COVID Tracking Project: https://covidtracking.com/data/national/cases        
        Yahoo Finance: https://finance.yahoo.com/          

        ### Website Development and Technology    
        The most significant tool we used to develop website is Dash, which is a useful tool, based on Flask, to visulize our 
        data trend and our prediction result. We implemented functions for each corresponding conttent and combine them 
        together in the application layout. 
        ### Data Handling and Database Design
        The covid case data and stock market data are grapped from relevant websites. After cleaning them and transforming them 
        into our desied form, we build a dataset based on them. We set up our database on MongoDB cluster and a update data_scraper 
        function has been implemented to enable the database to update every day. For data analysis and building model in this project, 
        we connect the mongo client to our MongoDB and obtain our desired data.       
        ### Notebooks
        1. ETL_EDA: https://github.com/Enmin/final-project/blob/master/skeleton/ETL_EDA.ipynb      
        2. Enhancement: https://github.com/Enmin/final-project/blob/master/skeleton/Enhancement.ipynb        
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")
