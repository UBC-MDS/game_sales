from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


from src.line_charts import *
from src.publishers import *
from src.platforms import *

#alt.data_transformers.enable('data_server')
# alt.renderers.enable('default')

app = Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Video Game Sale Dashboard"
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


@app.callback(
    Output('platforms', 'srcDoc'),
    Input('platforms-slider', 'value'))
def update_output(value):
    return plotPlatforms(value)


# Chart drawing functions
def lineGlobalFigure():
    return  html.Iframe(
                    id=f'line_global',
                    srcDoc=plotLineGlobal(genre='Sports'))

def lineGenreFigure():
    return  html.Iframe(
                    id=f'line_genre',
                    srcDoc=plotLineGenre(genre='Sports', region='North America'))

def publishersFigure():
    return  html.Div([
        html.Iframe(
                    id=f'publishers',
                    srcDoc=plotPublishers(top_val='10'))
    ])

def platformsFigure():
    return  html.Div([
        html.Iframe(
                    id=f'platforms',
                    srcDoc=plotPublishers(top_val='15'))
    ])

app.title = "Video Game Sales"

sidebar = html.Div([
        html.H1('Menu'),
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
            options=[{'label': i, 'value': i} for i in getRegions()]),
        html.Br(),
        html.H5('Number of Publishers'),  
        dcc.Slider(0, 20, 5,
               value=10,
               id='topn-slider'),
        html.Br(),
        html.H5('Number of Platforms'),       
        dcc.Slider(0, 25, 5,
               value=15,
               id='platforms-slider'),
        html.Br(),
        html.H5('Date range'),       
        dcc.RangeSlider(1980, 2016,
               value=[1980, 2016],
               marks={1980:'1980', 1985:'1985', 1990:'1990', 1995:'1995', 2000:'2000', 2005:'2005', 2010:'2010', 2016:'2016'},
               id='year-slider'),
        ],
    id="sidebar")

content = html.Div([
                html.H1("Video Game Sales", id='title'),
                html.Hr(),
                dbc.Row([
                        dbc.Col([
                            lineGlobalFigure()
                        ]),
                        dbc.Col([
                            lineGenreFigure()
                        ]),
                ]),
                html.Hr(),
                dbc.Row([
                        dbc.Col([
                            publishersFigure()
                        ]),
                        dbc.Col([
                            platformsFigure()
                        ]),
                ]),
            ],
    id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == '__main__':
    app.run_server(debug=True)