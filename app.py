import dash
from dash import dcc
from dash import html
import plotly.express as px
import os

from etl_data import (
    non_market_dataframe, design_type_dataframe,
    clientele_type_dataframe)

app = dash.Dash(__name__)

server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
main_df = non_market_dataframe()
design_type_df = design_type_dataframe()
clientele_df = clientele_type_dataframe()

# Update me. Properly access the required token for mapbox for deployement.
token = os.environ['MAPBOX_TOKEN']


# TODO: Read the token form a text file. Easier
px.set_mapbox_access_token(token)

# All figures here.
fig = px.scatter_mapbox(
    main_df,
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
bar_fig = px.bar(
    design_type_df, x='Unit Type', y='Count',
    color_discrete_sequence=['#a32f28'],
)

pie_fig = px.pie(
  clientele_df, values='Count', names='Client', color_discrete_sequence=px.colors.sequential.RdBu
  )


# layout here.
app.layout = html.Div([
    html.H1('Exploring the Non Market Housing dataset.'),

    html.Div([
        html.H2('General information'),
        html.P([
            'The  ',
            html.A(
                'dataset ',
                href='https://opendata.vancouver.ca/explore/dataset/non-market-housing/information/'
            ),

            'is provided by the city of vancouver open data initiative. ',
            'The data is provided under the ',
            html.A('Open Government Licence.', href='https://opendata.vancouver.ca/pages/licence/'),
            html.Br(),
            '''
            The dataset provided information on non market housing developed and under development
            Between the year 1958 - 2020.
            '''
            ])
        ]),


    # Interacttive Map division
    html.Div([
        html.H2('Interactive map of the Non market Housing Dataset.'),
        html.P([
            '''The map shows locations and information of
            non market housing between the years 1958 - 2020.''',
            html.Br(),
            '''The projects are color coded depending on their phase
            and the scale reflects the capacity of the unit.''',
            html.Br(),
            '''
            Hover over the circles to get more information about the project.
            '''
            ]),
        dcc.Graph(
            id='interactive-map',
            figure=fig)
    ]),
    # Design type statistics.
    html.Div([
        html.H2('Unit counts for each Unit type.'),
        html.P([
            '''Here we look at the count of units per design type between 1958 - 2020.''',
            html.Br(),
            '''Note that we are only looking at completed and under construction projects in this stat.'''
            ]),
        dcc.Graph(
            id='unit-type-stats',
            figure=bar_fig)
    ]),

    # Pie chart by clientele
    html.Div([
        html.H2('Percentage of clientele 1958 and 2020'),
        html.P([
            '''Here we look at what percentage of the developments are for which clientele type.''',
            html.Br(),
            '''Note that here were looking as well at projects that were completed or under construction.''',
            html.Br(),
            '''\'Other\' here is a big umbrella and not will defined in the dataset.'''

            ]),
        dcc.Graph(
            id='clientele-percentage-stats',
            figure=pie_fig)
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)
