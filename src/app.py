import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import page_1
import page_2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
page_1.register_callbacks(app)

app.layout = html.Div([
    html.H1("Welcome to Data Secrets"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Page 1', href='/page_1'),
    html.Br(),
    dcc.Link('Page 2', href='/page_2'),
])


page_1_layout = page_1.layout


page_2_layout = page_2.dynamic_layout(app)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page_1':
        return page_1_layout
    elif pathname == '/page_2':
        return page_2_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)