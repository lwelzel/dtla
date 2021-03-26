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
        self.alpha = None
        self.NEP_J=None

        # f)
        self.c_v_lat = c_v_lat
        self.c_v_e = c_v_e

        self.C_v_lat = None
        self.C_v_e = None
        self.C_v_total = None

    def set_th_cond(self):
        self.th_cond = self.L * self.T * self.sigma
        # self.th_cond = np.pi**2 * (1.380649e-23)**2 /(3* (1.602e-19)**2)* self.T * self.sigma

    def set_G(self):
        self.G = self.NEP_th ** 2 * self.q_eff ** 2 / (4 * 1.380649e-23 * self.T ** 2)

    def set_r_lead(self):
        self.r_lead = np.sqrt(self.G * self.l_lead / (self.th_cond * np.pi * 2))

    def set_diss_power(self):
        self.diss_P = self.V_out * self.I

    def find_load_curve_stupid_but_working(self):
        for i in np.arange(100):
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

    def set_alpha(self):
        self.alpha = -4/self.T

    def set_NEP_J(self):
        # self.NEP_J = self.G*self.T**(3/2)
        self.set_alpha()
        self.NEP_J = np.sqrt(4*1.380649e-23*self.T/self.diss_P)*self.G/(self.q_eff*abs(self.alpha))

    def set_total_heat_cap_rat(self):
        self.C_v_lat = self.c_v_lat * self.px_a ** 3
        self.C_v_e = 2 * self.c_v_e * self.r_lead ** 2 * np.pi * self.l_lead
        self.C_v_total=self.C_v_lat/self.C_v_e


if __name__ == "__main__":
    BoloCirc = Circ(R0=1e6, R_L=1e7, V_bias=1.5, T0=2.7,
                    c_v_lat=7e-6, c_v_e=1.3e-4, px_a=0.05, L=2.44e-8, T=2.7, sigma=3.1e5, NEP_th=4.5e-15,
                    q_eff=0.5,l_lead=1)

    # check code with exercise example
    unit_test = False
    if unit_test:
        BoloCirc = Circ(R0=1e6, R_L=1e7, V_bias=1.5, T0=1.5,
                        c_v_lat=7e-6, c_v_e=1.3e-4, px_a=0.053, L=2.44e-8, T=1.5, sigma=3.1e5, NEP_th=5.8e-15,
                        q_eff=0.9, l_lead=0.5)

    # b)
    print("\n--=== Q b) ===---")
    if type(BoloCirc.G)==type(None):
        BoloCirc.set_th_cond()
        BoloCirc.set_G()
        BoloCirc.set_r_lead()

    try:
        print(f"th_cond: {BoloCirc.th_cond:.3E} W K cm-1\n"
              f"G:       {BoloCirc.G:.3E} W K-1\n"
              f"r_lead:  {BoloCirc.r_lead:.3E} cm (D = {2* BoloCirc.r_lead/100*1e6:.3E} micron)")
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

        # e)
        print("\n--=== Q e) ===---")
        BoloCirc.set_NEP_J()
        print(f"NEP_J: {BoloCirc.NEP_J:.3E} A Hz-1/2")

        # f)
        print("\n--=== Q f) ===---")
        BoloCirc.set_total_heat_cap_rat()
        print(f"C_v_total_ratio at 2.7 K: {BoloCirc.C_v_total*(2.7)**(3-1):.3E} [-]")
        print(f"C_v_total_ratio is unity at: {np.sqrt(1/BoloCirc.C_v_total):.3E} K")

        T_range=np.linspace(1e-1,4,10000)
        C_v_total_ratio=BoloCirc.C_v_total*(T_range)**(3-1)


        fig, ax1, = plt.subplots(1, 1, constrained_layout=False)

        point = ax1.scatter(x=T_range, y=C_v_total_ratio, s=1, label=r"general curve")
        unity = ax1.scatter(x=2.7, y=BoloCirc.C_v_total*(2.7)**(3-1), s=80, marker='+',c="red", label=r"ratio @ 2.7 K" )
        ax1.scatter(x=np.sqrt(1/BoloCirc.C_v_total), y=1, s=80, marker='+', c="green", label=r"ratio is unity")

        plt.rc('text', usetex=True)
        ax1.set_title(f'Ratio of total heat capacities vs Temperature', fontsize=12)
        ax1.set_ylabel(r'Ratio of total heat capacities [$C_{v}^{{lat }} / C_{v}^{e}$]')
        ax1.set_xlabel('Temperature [$T$]')

        ax1.loglog()
        ax1.grid(which="both", alpha=0.5, )
        ax1.set_axisbelow(True)
        # plt.legend() idk why it doesnt want to print tex in legend

        plt.tight_layout()
        fig.set_dpi(500)
        plt.savefig("./welzel_ex6_qf_plot.png", dpi=500)
        plt.show()
        plt.clf()

    except TypeError:
        print("\nRunning test code. No further outputs.")