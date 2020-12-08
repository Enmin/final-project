import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import page_1
import page_2
import figures
import about
import detail

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
page_1.register_callbacks(app)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


index_page = html.Div([
    html.H1("Welcome to Data Secrets", style={'text-align': 'center'}),
    dcc.Link('About', href='/about', style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex'}),
    html.Br(),
    dcc.Link('Detail', href='/detail', style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex'}),
    html.Br(),
    dcc.Link('Basic Data Analysis', href='/page_2', style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex'}),
    html.Br(),
    dcc.Link('Model & Prediction', href='/page_1', style={'font-size': '30px', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                              'justify-content': 'center', 'display': 'flex'}),
    html.Br(),
    html.Div([dcc.Graph(id='stock_pie_chart', figure=figures.index_visual())]),
    html.Br(),
    html.A([html.Img(id='logo1', src=app.get_asset_url('github.png'), style={'height': '50px', 'padding-bottom': '1px'}),
                html.Span('Yangyin Ke', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})], className="two columns row", href='https://github.com/yangyinke'),
    html.A([html.Img(id='logo2', src=app.get_asset_url('github.png'), style={'height': '50px', 'padding-bottom': '1px'}),
                html.Span('Huaqi Nie', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})], className="two columns row", href='https://github.com/huaqi010'),
    html.A([html.Img(id='logo3', src=app.get_asset_url('github.png'), style={'height': '50px', 'padding-bottom': '1px'}),
                html.Span('Enmin Ehou', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})], className="two columns row", href='https://github.com/Enmin')
])


page_1_layout = page_1.layout


page_2_layout = page_2.dynamic_layout(app)

about_layout = html.Div([about.about_page_header(), about.about_page()])

detail_layout = html.Div([detail.detail_header(), detail.detail_page()])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page_1':
        return page_1_layout
    elif pathname == '/page_2':
        return page_2_layout
    elif pathname == '/about':
        return about_layout
    elif pathname == '/detail':
        return detail_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=False)