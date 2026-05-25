import numpy as np
from scipy.constants import c


# - General cavity formulas -- #
def Finesse(T, Loss=0.):
    """
    Cavity Finesse for a bow-tie ring cavity.
    :param T: Transmission coefficient
    :param Loss: Intra-cavity Loss
    :return:
    """
    return np.pi * ((1 - T) * (1 - Loss))**(1/4) / (1 - np.sqrt((1 - T) * (1 - Loss)))


def FSR_bowtie(L):
    """
    Free Spectral Range (frequency domain) for a bow-tie ring cavity
    :param L: Cavity length
    :return:
    """
    return c / L


def FSR_linear(L):
    """
    Free Spectral Range for a linear cavity.
    :param L: Cavity length
    :return:
    """
    return c / (2 * L)


def bandwidth(fsr, finesse):
    """
    Calculate bandwidth of bow-tie ring cavity (frequency domain)
    :param fsr: Free Spectral Range
    :param finesse: Finesse
    :return:
    """
    return fsr / finesse