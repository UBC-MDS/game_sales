from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from line_charts import *
from publishers import *

# alt.data_transformers.enable('data_server')
# alt.renderers.enable('default')

app = Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# Call backs
@app.callback(
    Output('line_global', 'srcDoc'),
    Input('genre_f', 'value'))
def lineGlobalCallback(genre):
    return plotLineGlobal(genre)

@app.callback(
    Output('line_genre', 'srcDoc'),
    Input('genre_f', 'value'),
    Input('region_f', 'value'))
def lineGenreCallback(genre, region):
    return plotLineGenre(genre, region)


@app.callback(
    Output('publishers', 'srcDoc'),
    Input('topn-slider', 'value'))
def update_output(value):
    return plotPublishers(value)


# Chart drawing functions
def lineGlobalFigure():
    return  html.Iframe(
                    id=f'line_global',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'},
                    srcDoc=plotLineGlobal(genre='Sports'))


def lineGenreFigure():
    return  html.Iframe(
                    id=f'line_genre',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'},
                    srcDoc=plotLineGenre(genre='Sports', region='North America'))

def publishersFigure():
    return  html.Div([
        html.Iframe(
                    id=f'publishers',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'},
                    srcDoc=plotPublishers(top_val='10')),
         dcc.Slider(0, 20, 5,
               value=10,
               id='topn-slider')
    ])

app.title = "Video Game Sales"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div([
        html.H2('Video Game Sales'),
        html.Br(),
        html.H5('Genre'),
        dcc.Dropdown(
            id='genre_f',
            value='Sports',
            options=[{'label': i, 'value': i} for i in getGenres()]),
        html.Br(),
        html.H5('Region'),
        dcc.Dropdown(
            id='region_f',
            value='North America',
            options=[{'label': i, 'value': i} for i in getRegions()])
        ],
    id="sidebar", style=SIDEBAR_STYLE)

content = html.Div([
                dbc.Row([
                        dbc.Col([
                            lineGlobalFigure()
                        ]),
                        dbc.Col([
                            lineGenreFigure()
                        ]),
                ]),

                dbc.Row([
                        dbc.Col([
                            publishersFigure()
                        ]),
                        dbc.Col([
                            # Heat map
                        ]),
                ]),
            ],
    id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == '__main__':
    app.run_server(debug=True)