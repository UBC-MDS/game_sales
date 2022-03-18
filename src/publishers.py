import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()

sales = pd.read_csv("data/raw/vgsales.csv")
def plotPublishers(top_val, daterange=[1980, 2016]):
    top_publishers = sales["Publisher"].value_counts().head(int(top_val)).index.tolist()
    top_publishers_df = sales.query("Publisher in @top_publishers").head(4900)
    top_publishers_df = top_publishers_df.loc[(top_publishers_df['Year'] > daterange[0]) & (top_publishers_df['Year'] < daterange[1])]
    chart = alt.Chart(top_publishers_df, title='Game Copies Sold by Publisher').mark_bar().encode(
            x=alt.X("count()", title='Copies Sold (M)'),
            y=alt.Y("Publisher", sort="-x")
        )
    return chart.to_html()