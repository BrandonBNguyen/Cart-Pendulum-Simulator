from DrawPendulum import DrawPendulum
import math
import numpy as np
from RK4Simulator import RK4Simulator
import time


class ThreadTransmitter():

    def __init__(self):
        self.message = None

    def send(self, message):
        self.message = message

    def read(self):
        if self.message:
            message = self.message
            self.message = None
            return message


class PendulumTurtleCanvas:

    def __init__(self, canvas, pendulum_length, position):
        self.canvas = canvas
        self.draw_canvas = DrawPendulum(canvas, pendulum_length)
        self.update_position(position)

    def update_position(self, position, pendulum_length=None, convert_to_radian=True):
        if convert_to_radian:
            position[1] = position[1] * math.pi / 180
        if pendulum_length:
            self.draw_canvas.change_pendulum_length(pendulum_length)
        self.draw_canvas.draw(position)


class Simulator():

    def __init__(self, settings, canvas, transmitter, until_button_pushed):
        self.turtle = PendulumTurtleCanvas(
            canvas,
            settings['Pendulum length'],
            [settings['Initial cart position'], settings['Initial pendulum position']]
        )
        paused = True
        end_program = False
        while not end_program:
            transmitter_message = transmitter.read()
            if transmitter_message:
                if transmitter_message[0] == 'apply':
                    settings = transmitter_message[1]
                    self.generate_data(settings)
                    self.turtle.update_position(self.get_next_position(settings), settings['Pendulum length'],convert_to_radian=False)
                    until_button_pushed.clear()
                    paused = True
                elif transmitter_message[0] == 'run':
                    paused = False
                elif transmitter_message[0] == 'pause':
                    until_button_pushed.clear()
                    paused = True
                elif transmitter_message[0] == 'stop':
                    until_button_pushed.clear()
                    self.generate_data(settings)
                    self.turtle.update_position(self.get_next_position(settings), settings['Pendulum length'],
                                                convert_to_radian=False)
                    paused = True
                elif transmitter_message[0] == 'close':
                    until_button_pushed.clear()
                    end_program = True
            else:
                if paused:
                    until_button_pushed.wait()
                else:
                    time.sleep(settings['Time step'])
                    self.turtle.update_position(self.get_next_position(settings), convert_to_radian=False)

    @staticmethod
    def create_derivative_function(settings):
        def derivatives(state, time):
            # Returns the derivative of variables as functions of original state variables. For use in RK4 simulator.
            # Define variables
            m_p = settings['Cart mass']
            l_p = settings['Pendulum length']
            m_c = settings['Cart mass']
            I_p = 1 / 3 * m_p * pow(l_p, 3)
            g = 9.81
            x, v, theta, omega = state
            if settings['Forcing type'] == 'Sinusoidal':
                amplitude = settings['Forcing amplitude']
                freq = settings['Forcing frequency'] * 2 * math.pi
                phase = settings['Forcing phase shift'] * math.pi / 180
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

    def generate_data(self, settings):
        self.data_iter = 0
        s = [
            settings['Initial cart position'],
            settings['Initial cart velocity'],
            settings['Initial pendulum position'] * math.pi / 180,
            settings['Initial pendulum velocity'] * math.pi / 180
        ]
        if settings['Timed simulation']:
            self.data = RK4Simulator(s, Simulator.create_derivative_function(settings),
                            settings['Time step']).run_simulation(settings['End time'])
        else:
            self.data = RK4Simulator(s, Simulator.create_derivative_function(settings),
                            settings['Time step'])

    def get_next_position(self, settings):
        if settings['Timed simulation']:
            pos = self.data[self.data_iter][1][0]
            ang = self.data[self.data_iter][1][2]
            self.data_iter += 1
            if self.data_iter >= len(self.data):
                self.data_iter = 0
            return (pos, ang)
        else:
            pos, _, ang, _ = next(self.data)
            return (pos, ang)