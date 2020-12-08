import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from mongodb import connect
import requests
import joblib
from bs4 import BeautifulSoup

# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# available_indicators = df['Indicator Name'].unique()
# model

# covid data
db_covid = connect("covid")
collection_covid = db_covid.get_collection("cases")
data_covid = list(collection_covid.find())
df_covid = pd.DataFrame.from_records(data_covid).iloc[::-1]
df_covid = df_covid.reset_index().drop(['index','_id'], axis=1)

# stock data
db_stock = connect('stock')
collection_stock = db_stock.get_collection("historical")
data_stock = list(collection_stock.find())
df_stock = pd.DataFrame.from_records(data_stock)
codes = df_stock.code.unique()


COLORS = ['rgb(637,657,687)', 'rgb(80,80,80)', 'rgb(100,100,100)', 'rgb(115,115,115)', 'rgb(135,67,69)',
          'rgb(189,189,189)', 'rgb(67,80,100)', 'rgb(123,33,67)', 'rgb(138,45,69)', 'rgb(167,167,167)',
          'rgb(87,67,87)', 'rgb(67,67,67)', 'rgb(49,130,189)', 'rgb(467,67,35)', 'rgb(168,168,168)',
          'rgb(6,33,105)', 'rgb(8,14,215)', 'rgb(47,47,47)']

stock_dic = {'^GSPC':'S&P500','^DJI':'Dow Jones Industrial Average', 'GC=F':'Gold', 'CL=F':'Crude Oil',
             'AAPL':'Apple', 'MSFT':'Microsoft', 'GOOG':'Goolge', 'FB':'Facebook',
             'AMZN':'Amazon', 'WMT':'Walmart', 'GE':'General Electric', 'MMM':'3M',
             'AMT':'American Medical Technologists', 'JNJ':'Johnson & Johnson','PFE':'Pfizer',
             'JPM':'JPMorgan Chase & Co.', 'V':'Visa', 'XOM':'Exxon Mobil'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
available_indicators = ['close', 'high', 'low', 'open']

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='close'
            ),
            dcc.Dropdown(
                id='crossfilter-code-column',
                options=[{'label': i, 'value': i} for i in codes],
                value='FB'
            ),
        ],style={'width': '49%', 'display': 'inline-block'}),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-model-predictor'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Br(),
    html.Div(id='news')
])


def register_callbacks(app):
    @app.callback(
        dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
        [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
         dash.dependencies.Input('crossfilter-code-column', 'value')])
    def update_graph(xaxis_column_name, code):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # plot the trend of close stock price
        df = df_stock[df_stock.code == code].drop('_id', axis=1)
        result = df_covid.join(df.set_index('date'), on='date').dropna()
        result = result.replace(0, 1)
        x = list(result['date'])
        x_rev = x[::-1]

        y1 = list(np.log10(result['case']).replace([np.inf, -np.inf], 0))
        y2 = list(np.log10(result['new_case']).replace([np.inf, -np.inf], 0))
        y3 = result[xaxis_column_name]
        y4 = [0 for i in list(y1)]

        if True:
            fig.add_trace(go.Scatter(
                x=x + x_rev,
                y=y1 + y4,
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',
                line_color='rgba(255,255,255,0)',
                yaxis='y2',
                name='total_case'),
                secondary_y=True,
            )
            fig.add_trace(go.Scatter(
                x=x + x_rev,
                y=y2 + y4,
                fill='toself',
                fillcolor='rgba(0,176,246,0.2)',
                line_color='rgba(255,255,255,0)',
                yaxis='y2',
                name='new_case'),
                secondary_y=True,
            )

        fig.add_trace(go.Scatter(x=result['date'], y=y3, mode='lines', name=stock_dic[code],
                                 line={'width': 2, 'color': 'rgb(637,657,687)'}, yaxis='y'))

        fig.update_layout(template='plotly_dark',
                          title="Real World Data",
                          plot_bgcolor='#23272c',
                          paper_bgcolor='#23272c',
                          yaxis_title='number of new cases/stock price',
                          xaxis_title='Date',
                          yaxis2=dict({
                              'tickmode': 'array',
                              'tickvals': [0, 1, 2, 3, 4, 5, 6, 7],
                              'ticktext': ['10^{}'.format(i) for i in [0, 1, 2, 3, 4, 5, 6, 7]]}
                          ))
        return fig

    def generate_df(df):
        df = df[['date', 'case', 'close', 'new_case']].reset_index()
        period = 10
        dataset = pd.DataFrame(
            columns=['case{}'.format(i) for i in range(period)] + ['price{}'.format(i) for i in range(period)] + [
                'target'])
        for i in range(len(df) - period):
            case = []
            price = []
            for j in range(period):
                case.append(df['case'][i + j])
                price.append(df['close'][i + j])
            row = case + price + [df['close'][i + period]]
            dataset.loc[len(dataset.index)] = row
        return dataset

    @app.callback(
        dash.dependencies.Output('crossfilter-model-predictor', 'figure'),
        [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
         dash.dependencies.Input('crossfilter-code-column', 'value')])
    def update_prediction(xaxis_column_name, code):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        model = joblib.load('../model/model.pkl')

        # plot the trend of close stock price
        df = df_stock[df_stock.code == code].drop('_id', axis=1)
        result = df_covid.join(df.set_index('date'), on='date').dropna()
        result = result.replace(0, 1)
        dataset = generate_df(result)
        y = dataset['target']
        X = dataset.loc[:, dataset.columns != 'target']
        predictions = [model.predict([i])[0] for i in X.values]
        x = list(result['date'])
        x_rev = x[::-1]

        y1 = list(np.log10(result['case']).replace([np.inf, -np.inf], 0))
        y2 = list(np.log10(result['new_case']).replace([np.inf, -np.inf], 0))
        y4 = [0 for i in list(y1)]

        if True:
            fig.add_trace(go.Scatter(
                x=x + x_rev,
                y=y1 + y4,
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',
                line_color='rgba(255,255,255,0)',
                yaxis='y2',
                name='total_case'),
                secondary_y=True,
            )
            fig.add_trace(go.Scatter(
                x=x + x_rev,
                y=y2 + y4,
                fill='toself',
                fillcolor='rgba(0,176,246,0.2)',
                line_color='rgba(255,255,255,0)',
                yaxis='y2',
                name='new_case'),
                secondary_y=True,
            )

        fig.add_trace(go.Scatter(x=result['date'], y=predictions, mode='lines', name=stock_dic[code],
                                 line={'width': 2, 'color': 'rgb(637,657,687)'}, yaxis='y'))

        fig.update_layout(template='plotly_dark',
                          title='Random Forest Model Predictions',
                          plot_bgcolor='#23272c',
                          paper_bgcolor='#23272c',
                          yaxis_title='number of new cases/stock price',
                          xaxis_title='Date',
                          yaxis2=dict({
                              'tickmode': 'array',
                              'tickvals': [0, 1, 2, 3, 4, 5, 6, 7],
                              'ticktext': ['10^{}'.format(i) for i in [0, 1, 2, 3, 4, 5, 6, 7]]}
                          ))
        return fig

    @app.callback(
        dash.dependencies.Output('news', 'children'),
        [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
         dash.dependencies.Input('crossfilter-code-column', 'value')])
    def update_news(x, code):
        url = 'https://finance.yahoo.com/quote/{}/news?p={}'.format(code, code)
        r = requests.get(url, headers={'content-type': 'application/json'})
        soup = BeautifulSoup(r.text, 'html.parser')
        li = soup.find_all('li', attrs={'class': 'js-stream-content Pos(r)'})
        links = []
        for i in range(len(li)):
            info = li[i].find('a')
            links.append(dcc.Link(info.text, href=url.split('?')[0]+info.attrs['href'],
                                  style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex'}))
        return links


if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = layout
    register_callbacks(app)
    code = 'AAPL'
    xaxis_column_name = 'close'
    app.run_server(debug=True, port=8851)