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
app.layout = html.Div([
    html.H1('Gold Best Physical Price'),
    
    html.Div([
        dcc.Interval(id='interval_pull', interval=600000),
        html.Div('Last Update:'),
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
  return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets'),'apple-touch-icon.png', mimetype='image/png')

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
@server.route('/assets/<resource>')
def serve_static(resource):
    return send_from_directory(STATIC_PATH, resource)
    

@app.callback(
    [
        Output('tbl_gold', 'children'),
        Output('last_update', 'children'),
    ],
    [
        Input('interval_pull', 'n_intervals'),
    ],
)
def download_gold_data(interval_pull):
    data, cols = [], []
    
    
        
        
    df = get_all(cash_back=0)
    tbl = html_table(df, 'title')
    last_update_datetime = pd.datetime.today()
        
        
    return tbl, last_update_datetime

if __name__ == '__main__':
    app.run_server()