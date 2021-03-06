import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd

from app import app

from tabs import sidepanel, tab1, tab2, tab3, navbar
from database import transforms


app.layout = html.Div([navbar.Navbar()
                        , sidepanel.layout
            ])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    
    elif tab == 'tab-2':
        return tab2.layout

    elif tab == 'tab-3':
        return tab3.layout


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value
    
    return [None] * 3


@app.callback(
    Output('table-sorting-filtering', 'data')
    , [Input('table-sorting-filtering', "page_current")
     , Input('table-sorting-filtering', "page_size")
     , Input('table-sorting-filtering', 'sort_by')
     , Input('table-sorting-filtering', 'filter_query')
     , Input('rating-95', 'value')
     , Input('price-slider', 'value')
     , Input('country-drop', 'value')
     , Input('province-drop', 'value')
     , Input('variety-drop', 'value') 
     ])
def update_table(page_current, page_size, sort_by, filter, ratingcheck, prices, country, province, variety):
    filtering_expressions = filter.split(' && ')
    dff = transforms.df
    low = prices[0]
    high = prices[1]
    dff = dff.loc[(dff['price'] >= low) & (dff['price'] <= high)]
    if province is None:
            province = []
    if variety is None:
            variety = []

    if len(country) > 0 and len(province) > 0 and len(variety) > 0:
            dff = dff.loc[dff['country'].isin(country) & dff['province'].isin(province) & dff['variety'].isin(variety)]
    elif len(country) > 0 and len(province) > 0 and len(variety) == 0:
            dff = dff.loc[dff['country'].isin(country) & dff['province'].isin(province)]
    elif len(country) > 0 and len(province)== 0 and len(variety) > 0:
            dff = dff.loc[dff['country'].isin(country) & dff['variety'].isin(variety)]
    elif len(country) > 0 and len(province)== 0 and len(variety) == 0:
            dff = dff.loc[dff['country'].isin(country)]
    else:
            dff
            
    if ratingcheck == ['Y']:
            dff = dff.loc[dff['rating'] >= 95]
    else:
            dff
            
    for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
            
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
                
    if len(sort_by):
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )
    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')

########### TO LAUNCH APP #############
import webbrowser
from threading import Timer
port = 8050
def open_browser():
    '''
    to open browser server page automatically on app start-up
    '''
    webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(port=port, host="0.0.0.0")
    
'''    
# SIMPLE LAUNCH FORMAT - NEED TO OPEN WINDOW
if __name__ == '__main__':
    app.run_server(debug = True)'''