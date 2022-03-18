import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()

sales = pd.read_csv("data/raw/vgsales.csv")
def plotPlatforms(top_val, daterange):
    top_platforms = sales["Platform"].value_counts().head(int(top_val)).index.tolist()
    top_platforms_df = sales.query("Platform in @top_platforms").head(4900)
    top_platforms_df = top_platforms_df.loc[(top_platforms_df['Year'] > daterange[0]) & (top_platforms_df['Year'] < daterange[1])]
    chart = alt.Chart(top_platforms_df, title='Game Copies Sold by Platform').mark_bar().encode(
            x=alt.X("Platform", sort="-y"),    
            y=alt.Y("count()", title='Copies Sold (M)')
        )
    return chart.to_html()
