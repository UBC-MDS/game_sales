# game_sales

An interactive dashboard for Visualization of Video Game Sales

# Dashboard

The following sketch of the dashboard is an outline how the implementation will look like:

### Sketch

<img src="doc/img/dashboard_sketch.png" width="700"/>

## App description

The `game_sales` app contains a landing page that displays crucial information of the [Video Game Sales](https://www.kaggle.com/gregorut/videogamesales) dataset. The app focuses on analyzing sales trends and the ranking of the most popular video game publishers.

The visualizations shown by the app include :

- A line plot showing the evolution of global video game sales by its genre. The sales(lines) in the chart will be coloured according to the genre.

- Similarly, another line plot that shows the evolution of video game sales by region. Our dashboard analyzes sales by four regions; North America, Japan, Europe and the Rest of the world. The user can select global sales as well. The sales in the chart will be coloured according to the region.

- A bar chart showing the top publishers with the highest sales of video games.

The app includes a panel to help the user to filter the data and add functionality to the dashboard. 

The panel includes:

- Multiple selection boxes to filter out the video game sales by genre and region.

- Multiple selection box that allows the user to change the number of publishers considered in the ranking of the bar plot.

Users will be able to observe the evolution of sales of the video game industry and get insights into its trends by genre, publisher and region.
