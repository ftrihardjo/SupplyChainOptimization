import dash
from dash import dcc, html
import dash.dependencies as dd
import pandas as pd
import plotly.graph_objs as go
import pm4py

# Sample event log data (can be replaced with real data)
data = {
    'case_id': [1, 1, 1, 2, 2, 3, 3, 3, 3],
    'activity': ['Start', 'A', 'End', 'Start', 'A', 'Start', 'B', 'C', 'End'],
    'timestamp': pd.to_datetime(['2022-01-01 08:00:00', '2022-01-01 08:05:00', '2022-01-01 08:10:00',
                                 '2022-01-01 09:00:00', '2022-01-01 09:05:00', '2022-01-01 10:00:00',
                                 '2022-01-01 10:05:00', '2022-01-01 10:10:00', '2022-01-01 10:15:00'])
}

df = pd.DataFrame(data)

# Converting to an event log
event_log = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')

# Discover process model
process_model = pm4py.discover_petri_net_alpha(event_log)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Process Mining Dashboard"),
    dcc.Graph(id='process-model', figure={})
])

@app.callback(
    dd.Output('process-model', 'figure'),
    [dd.Input('process-model', 'id')]
)
def update_graph(_):
    # Generate visualization using pm4py
    gviz = pm4py.visualization.petrinet.visualizer.apply(process_model[0], process_model[1], process_model[2])
    fig = go.Figure(go.Image(z=gviz))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
