import pickle
import os
import flask
from flask import Flask, send_from_directory
import dash
from dash_table import DataTable
from dash.dependencies import Output, Input, State 
from gold_physical import get_all, html_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title='GOLD'

server = app.server

DIRNAME = os.path.dirname(os.path.abspath(__file__))

app.layout = html.Div([

    html.Div([
        html.Button(id='fake_button'),
    ],style={'display': 'none'}),

    html.H1('Gold Best Physical Price'),
    
    
    html.Div([
        dcc.Interval(id='interval_pull', interval=600000),
        html.Div('Last Update:'),
        
        html.Div(
            id='fast_load', 
        style={'display': 'inline-block'}),
        
        html.Div(id='last_update'),
    ]),
    
    html.Div(
        id='tbl_gold',
    ),
])


@app.server.route('/favicon.ico')
def favicon():
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    return send_from_directory(fp, 'favicon.ico')
    
@app.server.route('/apple-touch-icon.png')
def applePng():
  return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets'),'apple-icon.png', mimetype='image/png')

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
@server.route('/assets/<resource>')
def serve_static(resource):
    return send_from_directory(STATIC_PATH, resource)
    

@app.callback(
    
    Output('fast_load','children'),
    [
        Input('fake_button', 'n_clicks'),
    ],
)
def fast_load_table(fake_button):

    print('running fast load')
    fp  = os.path.join(DIRNAME, 'gold_table.p')
    
    if os.path.exists(fp):
        print('reading from file')
        
        data = pickle.load(open( fp, mode='rb' ) )
        
        df = data['df']
        last_update = data['last_update']
        tbl = [
            html.Div(last_update),
            html_table(df, 'title'),
        ]
        
    else:
        tbl = []
        
        
    print('finished fast load')
    return tbl

@app.callback(
    [
        Output('tbl_gold', 'children'),
        Output('last_update', 'children'),
        Output('fast_load', 'style'),
    ],
    [
        Input('interval_pull', 'n_intervals'),
    ],
)
def download_gold_data(interval_pull):
    print('running long pull')
    df = get_all(cash_back=0)
    tbl = html_table(df, 'title')
    last_update_datetime = pd.datetime.today()
    fp  = os.path.join(DIRNAME, 'gold_table.p')
    data = {
        'df': df,
        'last_update': last_update_datetime,
    }
    try:
        pickle.dump(data, open( fp, mode='wb' ))
    except:
        pass
    style = {'display': 'none'}
    print('finished long pull')
    return tbl, last_update_datetime, style




if __name__ == '__main__':
    app.run_server(debug=False)