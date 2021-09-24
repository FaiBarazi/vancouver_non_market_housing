"""
Returns non market dataframe extracted from the data folder,
cleaned-ish and transformed
"""
from pathlib import Path
import json
import pandas as pd


repo_path = Path.cwd()
data_path = repo_path/'data'
non_market_path = data_path/'non-market-housing.csv'


def non_market_dataframe():
    non_market_df = pd.read_csv(non_market_path, delimiter=';')

    # Cleaning and Wrangling non_market_df
    design_columns = {
        column: 0 for column in non_market_df.columns if column.startswith('Design')
        }
    # Update design type
    non_market_df.fillna(value=design_columns, inplace=True)
    non_market_df.fillna(value={'Operator': 'not specified'}, inplace=True)
    # Turn json/str to a dictionary to extract coordiantes
    # Note the coordinates are written as [long, lat]
    geometry_series = non_market_df['Geom'].apply(lambda x: json.loads(x))
    non_market_df['longitude'] = geometry_series.apply(lambda x: x['coordinates'][0])
    non_market_df['latitude'] = geometry_series.apply(lambda x: x['coordinates'][1])

    # Add a column with the total number of units for each project
    units_per_housing = non_market_df[list(design_columns.keys())].sum(axis=1)
    non_market_df['Total Units'] = units_per_housing
    return non_market_df
