import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Initial empty DataFrame
df = pd.DataFrame(columns=["Category", "Values"])

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Interactive Dashboard'),

    html.Div(children='''
        Enter data to display on the graph.
    '''),

    html.Div([
        dcc.Input(id='input-category', type='text', placeholder='Category'),
        dcc.Input(id='input-value', type='number', placeholder='Value'),
        html.Button('Add', id='submit-val', n_clicks=0)
    ]),

    dcc.Graph(
        id='example-graph'
    ),

    html.Div(children=[
        html.H3(children='Statistics'),
        html.Div(id='statistics')
    ])
])

# Callback to update the graph and statistics based on user input
@app.callback(
    Output('example-graph', 'figure'),
    Output('statistics', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-category', 'value'),
    State('input-value', 'value'),
    State('example-graph', 'figure')
)
def update_graph(n_clicks, category, value, existing_figure):
    global df

    if category and value is not None:
        df = df.append({"Category": category, "Values": value}, ignore_index=True)

    fig = px.bar(df, x="Category", y="Values", title="Category vs Values")

    statistics = [
        f"Total Sum: {df['Values'].sum()}",
        f"Average: {df['Values'].mean()}",
    ]

    return fig, statistics

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
