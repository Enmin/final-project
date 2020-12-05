import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import main_page

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
main_page.register_callbacks(app)

app.layout = html.Div([
    html.H1("Welcome to Data Secrets"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Main', href='/main'),
    html.Br(),
    dcc.Link('unFinished', href='/unfinished'),
])


page_1_layout = main_page.layout


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.Link('Go back to home', href='/')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/main':
        return page_1_layout
    elif pathname == '/unfinished':
        return page_2_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)