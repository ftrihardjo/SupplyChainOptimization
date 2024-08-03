import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

# Gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Masses of Earth and Jupiter
M_earth = 5.972e24  # kg
M_jupiter = 1.898e27  # kg

# Astronomical unit in meters
AU = 1.496e11

# Initial state vector: [x_earth, y_earth, vx_earth, vy_earth, x_jupiter, y_jupiter, vx_jupiter, vy_jupiter]
def init_state():
    pos_earth = [1 * AU, 0]
    vel_earth = [0, 29.78e3]
    pos_jupiter = [5.2 * AU, 0]
    vel_jupiter = [0, 13.07e3]
    return np.concatenate((pos_earth, vel_earth, pos_jupiter, vel_jupiter))

# Define derivatives for odeint
def derivatives(state, t):
    r_earth = state[0:2]
    v_earth = state[2:4]
    r_jupiter = state[4:6]
    v_jupiter = state[6:8]

    r = r_jupiter - r_earth
    r_mag = np.linalg.norm(r)
    
    # Gravitational force
    F_mag = G * M_earth * M_jupiter / r_mag**2
    F_earth = F_mag * (r / r_mag)
    F_jupiter = -F_earth
    
    a_earth = F_earth / M_earth
    a_jupiter = F_jupiter / M_jupiter

    return np.concatenate((v_earth, a_earth, v_jupiter, a_jupiter))

# Time span for simulation
T = 365.25 * 24 * 3600 * 11.86  # 11.86 Earth years in seconds
t = np.linspace(0, T, 10000)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gravitational Simulator: Earth and Jupiter"),

    dcc.Input(id='input-vel-earth', type='number', value=29.78e3, placeholder='Initial Earth Velocity (m/s)'),
    dcc.Input(id='input-vel-jupiter', type='number', value=13.07e3, placeholder='Initial Jupiter Velocity (m/s)'),
    html.Button('Simulate', id='simulate-button', n_clicks=0),

    dcc.Graph(id='orbit-graph')
])

@app.callback(
    Output('orbit-graph', 'figure'),
    Input('simulate-button', 'n_clicks'),
    State('input-vel-earth', 'value'),
    State('input-vel-jupiter', 'value')
)
def update_orbits(n_clicks, vel_earth, vel_jupiter):
    # Update initial velocities based on user input
    initial_state = init_state()
    initial_state[3] = vel_earth
    initial_state[7] = vel_jupiter

    # Solve the ODE
    solution = odeint(derivatives, initial_state, t)

    # Extract positions
    pos_earth_sol = solution[:, 0:2]
    pos_jupiter_sol = solution[:, 4:6]

    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pos_earth_sol[:, 0] / AU, y=pos_earth_sol[:, 1] / AU, mode='lines', name='Earth'))
    fig.add_trace(go.Scatter(x=pos_jupiter_sol[:, 0] / AU, y=pos_jupiter_sol[:, 1] / AU, mode='lines', name='Jupiter'))
    fig.update_layout(title="Orbital Paths", xaxis_title="x (AU)", yaxis_title="y (AU)", showlegend=True)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
