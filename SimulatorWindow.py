from DrawPendulum import DrawPendulum
import threading
import math
from RK4Simulator import RK4Simulator
import numpy as np
import time


class SimulatorWindow:

    def __init__(self, canvas):
        self.draw_canvas = DrawPendulum(canvas, 0.4)
        self.draw_canvas.draw([0, 0])
        self.end_program = False
        self.not_running = threading.Event()
        self.data_iter = 0
        self.settings = None
        self.data = None
        self.thread = threading.Thread(target=self.mainloop)
        self.thread.start()

    def apply(self, settings):
        self.settings = settings
        self.generate_data()
        self.draw_next_position()
        self.not_running.set()
        self.not_running.clear()

    def run(self):
        self.not_running.set()

    def pause(self):
        self.not_running.clear()

    def stop(self):
        self.generate_data()
        self.draw_next_position()
        self.not_running.set()
        self.not_running.clear()

    def close(self):
        self.end_program = True
        if self.not_running.is_set():
            self.not_running.clear()
        else:
            self.not_running.set()

    def create_derivative_function(self):
        def derivatives(state, time):
            # Returns the derivative of variables as functions of original state variables. For use in RK4 simulator.
            # Define variables
            m_p = self.settings['Cart mass']
            l_p = self.settings['Pendulum length']
            m_c = self.settings['Cart mass']
            I_p = 1 / 3 * m_p * pow(l_p, 3)
            g = 9.81
            x, v, theta, omega = state
            if self.settings['Forcing type'] == 'Sinusoidal':
                amplitude = self.settings['Forcing amplitude']
                freq = self.settings['Forcing frequency'] * 2 * math.pi
                phase = self.settings['Forcing phase shift'] * math.pi / 180
                u = amplitude * math.cos(freq * time + phase)
            else:
                u = 0
            x_dot = v
            v_dot = (pow(m_p * l_p, 2) * g * math.sin(theta) * math.cos(theta) / (I_p + m_p * pow(l_p, 2)) - m_p * l_p *
                     math.sin(theta) * omega ** 2 + u) / (m_c + m_p - pow(m_p * l_p * math.cos(theta), 2) /
                                                          (I_p + m_p * l_p ** 2))
            theta_dot = omega
            omega_dot = (u - m_p * l_p * math.sin(theta) * pow(omega, 2) + (m_c + m_p) * g * math.tan(theta)) / \
                        ((I_p + m_p * pow(l_p, 2)) * (m_c + m_p) / (m_p * l_p * math.cos(theta)) - m_p * l_p * math.cos(
                            theta))
            return np.array([x_dot, v_dot, theta_dot, omega_dot])

        return derivatives

    def generate_data(self):
        self.data_iter = 0
        s = [
            self.settings['Cart position'],
            self.settings['Cart velocity'],
            self.settings['Pendulum position'] * math.pi / 180,
            self.settings['Pendulum velocity'] * math.pi / 180
        ]
        if self.settings['Timed simulation']:
            self.data = RK4Simulator(s, self.create_derivative_function(),
                                     self.settings['Time step']).run_simulation(self.settings['End time'])
        else:
            self.data = RK4Simulator(s, self.create_derivative_function(),
                                     self.settings['Time step'])

    def draw_next_position(self):
        if self.settings['Timed simulation']:
            pos = self.data[self.data_iter][1][0]
            ang = self.data[self.data_iter][1][2]
            self.data_iter += 1
            if self.data_iter >= len(self.data):
                self.data_iter = 0
            self.draw_canvas.draw([pos, ang])
        else:
            pos, _, ang, _ = next(self.data)
            self.draw_canvas.draw([pos, ang])

    def mainloop(self):
        while not self.end_program:
            if self.not_running.is_set():
                try:
                    self.draw_next_position()
                except RuntimeError:
                    self.end_program = True
                time.sleep(self.settings['Time step'])
            else:
                self.not_running.wait()
