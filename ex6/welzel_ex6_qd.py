import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


class Circ:
    def __init__(self, R0, R_L, V_bias, T0, c_v_lat, c_v_e, px_a, l_lead, L, T, sigma, NEP_th, q_eff, G=None):
        # b)
        self.l_lead = l_lead # in cm
        self.L = L
        self.T = T
        self.sigma = sigma # in cm-1
        self.NEP_th = NEP_th
        self.q_eff = q_eff

        self.G = G

        self.th_cond = None
        self.r_lead = None # in cm
        # i hate units
        # all my homies use natural units

        # or something
        self.px_a = px_a  # in cm

        # d)
        self.R0 = R0
        self.R_L = R_L
        self.V_bias = V_bias
        self.V_out = 0
        self.T0 = T0

        self.I = self.V_bias / self.R_L  # initial guess


        self.R_detector = None
        self.diss_P = None

        # e)
        self.NEP_J=None

        # f)
        self.c_v_lat = c_v_lat
        self.c_v_e = c_v_e

        self.C_v_lat = None
        self.C_v_e = None
        self.C_v_total = None

    def set_th_cond(self):
        self.th_cond = self.L * self.T * self.sigma

    def set_G(self):
        self.G = self.NEP_th ** 2 * self.q_eff ** 2 / (4 * 1.380649e-23 * self.T ** 2)

    def set_r_lead(self):
        # th_cond is in cm convert to m
        self.r_lead = np.sqrt(self.G * self.L / (self.th_cond*100 * np.pi * self.T))*100

    def set_diss_power(self):
        self.diss_P = self.V_out * self.I

    def find_load_curve_stupid_but_working(self):
        for i in np.arange(1000):
            self.V_out=(self.R0*self.I)/((1+(self.I*self.V_out/(self.G*self.T)))**4)
            self.I=(self.V_bias-self.V_out)/self.R_L

    def get_load_curve(self, x):
        (V, I) = (x[0], x[1])
        I = (self.V_bias - self.V_out) /(self.R_L)# V /(self.R0 + self.R_L)
        return abs(V / self.R0 * (1 + (I * V / (self.G * self.T0))) ** 4 - I)

    def find_load_curve(self):
        x0 = np.array([self.V_bias, self.I])
        res = minimize(self.get_load_curve, x0, method='Nelder-Mead', tol=1e-3)
        print(f"N_iter: {res.nit}, " + res.message)
        self.V_out = res.x[0]
        self.I = (self.V_bias - self.V_out) /(self.R_L) # res.x[1]

    def set_NEP_J(self):
        self.NEP_J=self.G*self.T**(3/2)

    def set_total_heat_cap_rat(self):
        self.C_v_lat = self.c_v_lat * self.px_a ** 3
        self.C_v_e = 2 * self.c_v_e * self.r_lead ** 2 * np.pi * self.l_lead
        self.C_v_total=self.C_v_lat/self.C_v_e


if __name__ == "__main__":
    BoloCirc = Circ(R0=1e6, R_L=1e7, V_bias=1.5, T0=2.7,
                    c_v_lat=7e-6, c_v_e=1.3e-4, px_a=0.05, L=2.44e-8,T=2.7, sigma=3.1e5, NEP_th=4.5e-15,
                    q_eff=0.5,l_lead=1)
    if True:
        BoloCirc = Circ(R0=1e6, R_L=1e7, V_bias=1.5, T0=2.7,
                        c_v_lat=7e-6, c_v_e=1.3e-4, px_a=0.05, L=2.44e-8, T=2.7, sigma=3.1e5, NEP_th=4.5e-15,
                        q_eff=0.5, l_lead=1, G=0.22e-6)

    # b)
    print("\n--=== Q b) ===---")
    if type(BoloCirc.G)==type(None):
        BoloCirc.set_th_cond()
        BoloCirc.set_G()
        BoloCirc.set_r_lead()

    try:
        print(f"th_cond: {BoloCirc.th_cond:.3E} W K cm-1\n"
              f"G:       {BoloCirc.G:.3E} S m-1\n"
              f"r_lead:  {BoloCirc.r_lead:.3E} cm")
    except TypeError:
        print(f"G:       {BoloCirc.G:.3E} S m-1\n")

    try:
        print("\n--=== Q d) ===---")
        # d)
        BoloCirc.find_load_curve_stupid_but_working()
        BoloCirc.set_diss_power()
        print(f"V_out:   {BoloCirc.V_out:.3E} V\n"
              f"I:       {BoloCirc.I:.3E} A\n"
              f"diss. P: {BoloCirc.diss_P:.3E} W")

        # V_axis=np.linspace(0,2,100)
        # I_axis=np.linspace(0,1e-6,100)
        # grid_xx, grid_yy = np.meshgrid(V_axis, I_axis, indexing='xy')

        # e)
        print("\n--=== Q e) ===---")
        BoloCirc.set_NEP_J()
        print(f"NEP_J: {BoloCirc.NEP_J:.3E} A Hz-1/2")

        # f)
        print("\n--=== Q f) ===---")
        BoloCirc.set_total_heat_cap_rat()
        print(f"C_v_total_ratio: {BoloCirc.C_v_total:.3E} [-]")
    except TypeError:
        print("\nRunning test code. No further outputs.")