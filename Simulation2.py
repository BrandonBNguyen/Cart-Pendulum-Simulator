import math
import numpy as np
from RK4Simulator import RK4Simulator
from DrawPendulum import DrawPendulum

# System Properties
m_c = 5  # Mass of kart in kilograms
m_p = 5  # Mass of pendulum in kilograms
l_p = 0.4  # Length of pendulum in meters
I_p = 1 / 3 * m_p * pow(l_p, 3)  # Moment of inertia of pendulum in kilograms times meters cubed
g = 9.81  # Gravitational acceleration in meters per second squared

# Initial Conditions
x_0 = 0  # Initial position in meters
v_0 = 0  # Initial velocity in meters per second
theta_0 = math.pi  # Initial pendulum angular position in radians
omega_0 = 0  # Initial pendulum angular velocity in radians per second

# Simulation Properties
dt = 0.00093  # Time step of simulation in seconds
time_end = 10  # Time at which to stop simulation
s = np.array([x_0, v_0, theta_0, omega_0])  # State variables


def derivatives(state, time):
    # Returns the derivative of variables as functions of original state variables. For use in RK4 simulator.
    x, v, theta, omega = state
    freq = 1  # Frequency of input force in Hz
    u = 20 * math.cos(freq * 2 * math.pi * time)
    x_dot = v
    v_dot = (pow(m_p * l_p, 2) * g * math.sin(theta) * math.cos(theta) / (I_p + m_p * pow(l_p, 2)) - m_p * l_p *
             math.sin(theta) * omega ** 2 + u) / (m_c + m_p - pow(m_p * l_p * math.cos(theta), 2) /
                                                  (I_p + m_p * l_p ** 2))
    theta_dot = omega
    omega_dot = (u - m_p * l_p * math.sin(theta) * pow(omega, 2) + (m_c + m_p) * g * math.tan(theta)) / \
                ((I_p + m_p * pow(l_p, 2)) * (m_c + m_p) / (m_p * l_p * math.cos(theta)) - m_p * l_p * math.cos(theta))
    return np.array([x_dot, v_dot, theta_dot, omega_dot])


pendulum_simulation = RK4Simulator(s, derivatives, dt)
results = pendulum_simulation.run_simulation(time_end)

# Draw Results in Turtle
drawing = DrawPendulum(l_p)
for result in results:
    pos = result[1][0]
    ang = result[1][2]
    drawing.draw([pos, ang])
