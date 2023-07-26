import numpy as np


def gon_factor(gon_value, theta_z_value):
    return gon_value * (np.cos(theta_z_value)) ** 1.2
