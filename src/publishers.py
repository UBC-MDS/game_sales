import altair as alt
import pandas as pd
import numpy as np

sales = pd.read_csv("../data/raw/vgsales.csv")
def plotPublishers(top_val):
    top_publishers = sales["Publisher"].value_counts().head(int(top_val)).index.tolist()
    top_publishers_df = sales.query("Publisher in @top_publishers").head(4900)
    chart = alt.Chart(top_publishers_df).mark_bar().encode(
            x="count()",
            y=alt.Y("Publisher", sort="-x")
        )
    return chart.to_html()