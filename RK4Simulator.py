import math


class RK4Simulator:

    def __init__(self, u, f, dt, t_0=0):
        """
        :param u: Numpy vector containing state variables
        :param f: Function relating derivatives to original variables
        :param dt: Time step
        """

        self.u = u
        self.f = f
        self.dt = dt
        self.t = t_0

    def __next__(self):
        u = self.u
        t = self.t
        k_1 = self.f(self.u, t)
        k_2 = self.f(self.u + self.dt / 2 * k_1, t + self.dt / 2)
        k_3 = self.f(self.u + self.dt / 2 * k_2, t + self.dt / 2)
        k_4 = self.f(self.u + self.dt * k_3, t + self.dt)
        self.u = self.u + self.dt / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        self.t = self.t + self.dt
        return u

    def run_simulation(self, time_stop):
        data = [[self.dt * i, self.__next__()] for i in range(0, math.floor(time_stop / self.dt) + 1)]
        return data
