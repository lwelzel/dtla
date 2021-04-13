import numpy as np
import matplotlib.pyplot as plt


# class HeterodyneDetector:
#     def __init__(self, wavelength, kappa, diameter, w_depletion, impedance):
#         self.wavelength = wavelength
#         self.kappa=kappa
#         self.diameter= diameter
#         self.w_depletion =w_depletion
#         self.impedance= impedance
#
#         self.freqency= 1/ self.wavelength
#
#         self.if_bandwidth =


if __name__ == "__main__":
    wavelength= 210E-6
    kappa = 10
    diameter = 85E-6
    radius = diameter/2
    depletion_width = 1.5E-6
    resistance = 140
    T1 = 3000
    T2 =200
    V1 = 3.7
    V2 = 1.2
    c = 299792458
    vac_permittivity = 8.8541878128E-12
    h = 6.62607015E-34
    k = 1.380649E-23
    bb_emissivity = 1
    eff = 0.55
    delta_f_frac = 0.15



    # a
    frequency= c/wavelength
    C = np.pi * radius**2 *kappa * vac_permittivity / depletion_width
    tau = resistance * C
    f_cutoff = 1/(2*np.pi*tau)

    print(f"C = {C:.2e}\n"
          f"tau = {tau:.2e}\n"
          f"Cutoff frequency = {f_cutoff:.2e}\n")

    # b i
    Y = V1 / V2
    T_N = (T1- Y*T2)/(Y-1)

    print(f"Y = {Y:.2e}\n"
          f"T_N = {T_N:.2e}\n")

    # b ii
    T_B = T_N

    hv = h*frequency
    k_T_B = k* T_B

    thermal_limit = hv < k_T_B

    print(f"T_B = {T_B:.2e}\n"
          f"hv = {hv:.2e}\n"
          f"kT_B = {k_T_B:.2e}\n"
          f"thermal limit: {thermal_limit}\n"
          f"quantum limit: {not thermal_limit}\n")

    # b iii (since thermal limit)
    # assume emissivity is bb_emissivity

    IA2 = (4*k*T_N*f_cutoff)/resistance
    rms_mp_noise = np.sqrt(IA2)

    print(f"IA^2 = {IA2:.2e}\n"
          f"RMS Amp Noise = {rms_mp_noise:.2e}\n")

    # c i
    delta_f_IF = delta_f_frac * f_cutoff
    eta_delta_f = eff * delta_f_frac * frequency

    heterodyne_rec_better = delta_f_IF > eta_delta_f

    print(f"delta_f_IF = {delta_f_IF:.2e}\n"
          f"eta delta_f = {eta_delta_f:.2e}\n"
          f"heterodyne receiver better: {heterodyne_rec_better}\n")

    # c ii
    delta_f = delta_f_IF / eff

    print(f"delta f = {delta_f:.2e}\n")

    # c iii
    spec_res = c / (wavelength * delta_f)

    print(f"spectral resolution = {spec_res:.2e}")

