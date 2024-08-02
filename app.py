import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Minkowski Distance Dashboard'),

    html.Div(children='''
        Enter two sets of coordinates and a value for p to compute Minkowski distance.
    '''),

    html.Div([
        dcc.Input(id='input-coordinates-1', type='text', placeholder='Coordinates 1 (e.g., 1,2,3)'),
        dcc.Input(id='input-coordinates-2', type='text', placeholder='Coordinates 2 (e.g., 4,5,6)'),
        dcc.Input(id='input-p', type='number', placeholder='Value of p', min=1),
        html.Button('Calculate', id='submit-val', n_clicks=0)
    ]),

    html.Div(children=[
        html.H3(children='Minkowski Distance'),
        html.Div(id='distance-result')
    ])
])

# Function to calculate Minkowski distance
def minkowski_distance(x, y, p):
    return np.sum(np.abs(x - y) ** p) ** (1 / p)

# Callback to update the distance result based on user input
@app.callback(
    Output('distance-result', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-coordinates-1', 'value'),
    State('input-coordinates-2', 'value'),
    State('input-p', 'value')
)
def update_distance(n_clicks, coordinates1, coordinates2, p):
    if coordinates1 and coordinates2 and p is not None:
        try:
            x = np.array([float(i) for i in coordinates1.split(',')])
            y = np.array([float(i) for i in coordinates2.split(',')])
            distance = minkowski_distance(x, y, p)
            return f"Minkowski Distance: {distance}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Please enter valid coordinates and p."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
