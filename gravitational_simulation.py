import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Masses of Earth and Jupiter
M_earth = 5.972e24  # kg
M_jupiter = 1.898e27  # kg

# Initial positions (in meters)
# Assuming Earth starts at (1 AU, 0) and Jupiter at (5.2 AU, 0)
AU = 1.496e11  # Astronomical unit in meters
pos_earth = np.array([1 * AU, 0])
pos_jupiter = np.array([5.2 * AU, 0])

# Initial velocities (in meters per second)
# Rough estimates based on orbital speeds
vel_earth = np.array([0, 29.78e3])
vel_jupiter = np.array([0, 13.07e3])

# Initial state vector
state0 = np.concatenate((pos_earth, vel_earth, pos_jupiter, vel_jupiter))

# Time span
T = 365.25 * 24 * 3600 * 11.86  # 11.86 Earth years in seconds
t = np.linspace(0, T, 10000)

def derivatives(state, t):
    r_earth = state[0:2]
    v_earth = state[2:4]
    r_jupiter = state[4:6]
    v_jupiter = state[6:8]

    # Vector from Earth to Jupiter
    r = r_jupiter - r_earth
    r_mag = np.linalg.norm(r)

    # Gravitational force magnitude
    F_mag = G * M_earth * M_jupiter / r_mag**2

    # Force vectors
    F_earth = F_mag * (r / r_mag)
    F_jupiter = -F_earth

    # Accelerations
    a_earth = F_earth / M_earth
    a_jupiter = F_jupiter / M_jupiter

    # Return derivatives
    return np.concatenate((v_earth, a_earth, v_jupiter, a_jupiter))

# Solve the system of differential equations
solution = odeint(derivatives, state0, t)

# Extract positions
pos_earth_sol = solution[:, 0:2]
pos_jupiter_sol = solution[:, 4:6]

# Plot the orbits
plt.plot(pos_earth_sol[:, 0] / AU, pos_earth_sol[:, 1] / AU, label="Earth")
plt.plot(pos_jupiter_sol[:, 0] / AU, pos_jupiter_sol[:, 1] / AU, label="Jupiter")
plt.xlabel('x (AU)')
plt.ylabel('y (AU)')
plt.legend()
plt.title('Gravitational Simulation of Earth and Jupiter')
plt.grid(True)
plt.axis('equal')
plt.show()
