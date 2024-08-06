- Import the classes Input, Output, State in addition to the ones already imported at line 2.
- Replace the function definition of update_graph from line 37 to line 41 by the following function definition:
def update_output(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if isinstance(df, pd.DataFrame):
            # Process the uploaded data
            event_log = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
            process_model = pm4py.discover_petri_net_alpha(event_log)
            gviz = pm4py.visualization.petrinet.visualizer.apply(process_model[0], process_model[1], process_model[2])
            fig = go.Figure(go.Image(z=gviz))
            return html.Div(['File processed successfully.']), fig
        else:
            return df, {}
    return html.Div(['Please upload a file.']), {}
- Replace the code at line 34 and 35 with the following code:
[Output('output-data-upload', 'children'),
Output('process-model', 'figure')],
[Input('upload-data', 'contents')],
[State('upload-data', 'filename')]
- Replace the code from line 7 to 23 with the following code:
import base64
import io
- Replace the code at line 15 with the following one:
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        }
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='process-model')
- Insert the following function definition at line 31:
  def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div(['Unsupported file format. Please upload a CSV or Excel file.'])

        return df
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])
