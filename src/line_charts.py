import altair as alt
import pandas as pd
import numpy as np


alt.data_transformers.disable_max_rows()

# data = pd.read_csv("data/raw/vgsales.csv")
data = pd.read_csv("data/raw/vgsales.csv")

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


def plotLineGlobal(genre):
    # alt.themes.enable("dark")
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


def plotLineGenre(genre, region):
    # alt.themes.enable("dark")
    lines = alt.Chart(pivoted.query("Genre == @genre & Region == @region "), title=f"Mean Sales {genre} in {region}").mark_line().encode(
    x=alt.X('Year:T', axis=alt.Axis(title='Year', grid=False)),
    y=alt.Y('mean(Sales)', axis=alt.Axis(title='Mean Sales in Millions', grid=True)))

    brush = alt.selection_interval(encodings=['x'])
    lower = lines.properties(height=60).add_selection(brush)
    upper = lines.encode(alt.X('Year:T', scale=alt.Scale(domain=brush)))
    chart = upper & lower
    return chart.to_html()

def getGenres():
    return pivoted['Genre'].unique()

def getRegions():
    return pivoted['Region'].unique()