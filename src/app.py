from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np
from vega_datasets import data
alt.data_transformers.enable('data_server')
alt.renderers.enable('default')
import dash_bootstrap_components as dbc


data = pd.read_csv("vgsales.csv")

# wrangling data

# pivoting to have a region column 

pivoted = data[['Year', 'Genre','NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales' ,'Global_Sales']].melt(['Year', 'Genre'])

# assigning region names

pivoted['variable'] = pivoted['variable'].replace('NA_Sales', "North America")
pivoted['variable'] = pivoted['variable'].replace('EU_Sales', "Europe")
pivoted['variable'] = pivoted['variable'].replace('JP_Sales', "Japan")
pivoted['variable'] = pivoted['variable'].replace('Other_Sales', "Rest of the World")
pivoted['variable'] = pivoted['variable'].replace('Global_Sales', "Global")

# Transform Year to date
pivoted['Year'] =pd.to_datetime(pivoted['Year'], format='%Y')

# Changing variable names
pivoted.rename(columns={"variable": "Region", "value": "Sales"}, inplace=True)


# building the app

app = Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    #html.H1('Video Game Sales Dashboard'),
    dbc.Row([
        dbc.Col(
        html.Div([
        html.H3('Video Game Sales', style={'color':'#ffffff'}),
        html.Br(),
        html.H5('Genre', style={'color':'#ffffff'}),
        dcc.Dropdown(
            id='genre_f',
            value='Sports',
            options=[{'label': i, 'value': i} for i in pivoted['Genre'].unique()]),
        html.Br(),
        html.H5('Region', style={'color':'#ffffff'}),
        dcc.Dropdown(
            id='region_f',
            value='North America',
            options=[{'label': i, 'value': i} for i in pivoted['Region'].unique()])
            ],
            style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "18rem", "padding": "2rem 1rem", "background-color": "#505050",})
        ,md=4),
        dbc.Col( 
            html.Iframe(
        id='line_genre',
        style={"position": "fixed", "top": 60, "left": 320, "bottom": 0, 'border-width': '0', 'width': '120%', 'height': '550px', "background-color": "#505050"})),
        dbc.Col(html.Iframe(
        id='line_global',
        style={"position": "fixed", "top": 60, "left": 871, "bottom": 0,'border-width': '0', 'width': '150%', 'height': '555px', "background-color": "#505050"})),
        ])
], style={"background-color": "#505050"})

@app.callback(
    Output('line_global', 'srcDoc'),
    Input('genre_f', 'value'))
def plot_1(genre):
    alt.themes.enable("dark")
    lines = alt.Chart(pivoted.query("Genre == @genre"), title=f"Mean Sales {genre}").mark_line().encode(
    x=alt.X('Year:T', axis=alt.Axis(title='Year', grid=False)),
    y=alt.Y('mean(Sales)', axis=alt.Axis(title='Mean Sales in Millions', grid=True)),
    color=alt.Color('Region',
                   sort = ["Global" , "North America" , "Japan" , "Europe", "Rest of the World"],
                   legend=alt.Legend(title=None)))

    brush = alt.selection_interval(encodings=['x'])
    lower = lines.properties(height=60).add_selection(brush)
    upper = lines.encode(alt.X('Year:T', scale=alt.Scale(domain=brush)))
    chart = upper & lower
    return chart.to_html()

@app.callback(
    Output('line_genre', 'srcDoc'),
    Input('genre_f', 'value'),
    Input('region_f', 'value'))
def plot_2(genre, region):
    alt.themes.enable("dark")
    lines = alt.Chart(pivoted.query("Genre == @genre & Region == @region "), title=f"Mean Sales {genre} in {region}").mark_line().encode(
    x=alt.X('Year:T', axis=alt.Axis(title='Year', grid=False)),
    y=alt.Y('mean(Sales)', axis=alt.Axis(title='Mean Sales in Millions', grid=True)))

    brush = alt.selection_interval(encodings=['x'])
    lower = lines.properties(height=60).add_selection(brush)
    upper = lines.encode(alt.X('Year:T', scale=alt.Scale(domain=brush)))
    chart = upper & lower
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)