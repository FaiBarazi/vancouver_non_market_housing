import dash
from dash import dcc
from dash import html
import plotly.express as px
import os

from etl_data import non_market_dataframe

app = dash.Dash(__name__)

server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = non_market_dataframe()

# Update me. Properly access the required token for mapbox for deployement.
token = os.environ['MAPBOX_TOKEN']


# TODO: Read the token form a text file. Easier
px.set_mapbox_access_token(token)
fig = px.scatter_mapbox(
    df,
    lat='latitude',
    lon='longitude',
    mapbox_style='carto-positron',
    hover_name='Name',
    hover_data=['Operator', 'Local Area', 'Total Units'],
    color='Project Status',
    color_discrete_sequence=['#5b606d', '#689626', '#c78d00', '#a42726'],
    size='Total Units',
    zoom=10
)

app.layout = html.Div(children=[
    html.H1(children='Interactive map of Non Market Housing in Vancouver.'),

    html.Div(children='''
        The map shows locations and information of non market housing
        between the years 1958 - 2020.
    '''),
    html.Div(
        children='''
        The projects are color coded depending
        on their phase and the scale reflects the capacity of the unit.
        '''),

    dcc.Graph(
        id='interactive-map',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
