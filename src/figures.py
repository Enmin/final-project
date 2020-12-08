from mongodb import connect
import pandas as pd
import plotly.express as px


def index_visual():
    ind_dict = {"technology": ["AAPL", "MSFT"],
                "communication services":["GOOG", "FB"],
                "consumer cyclical": ["AMZN", "WMT"],
                "industrials": ["GE", "MMM"],
                "real estate": ["AMT"],
                "health care": ["JNJ", "PFE"],
                "financial": ["JPM", "V"]}
    industries = []
    stocks = []
    db_stock = connect('stock')
    collection_stock = db_stock.get_collection("historical")
    data_stock = list(collection_stock.find())
    df_stock = pd.DataFrame.from_records(data_stock)
    for key,values in ind_dict.items():
        for v in values:
            industries.append(key)
            stocks.append(v)
    value = []
    for i in stocks:
        data = df_stock[df_stock.code == i].drop('_id', axis=1)
        value.append(*data['close'].tail(1).values)
    data = pd.DataFrame(dict(stock=stocks,industry=industries, close=value))
    fig = px.sunburst(data,path=['industry', 'stock'],values='close')
    fig.update_layout(template='plotly_dark',
                      title=None,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c')
    return fig