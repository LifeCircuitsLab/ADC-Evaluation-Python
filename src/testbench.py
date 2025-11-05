import matplotlib.pyplot as pg
import numpy as np

import src.utilities as utilities

class testbench:
    def __init__(self, resolution=10, reference_voltage=1):
        self.resolution = resolution
        self.reference_voltage = reference_voltage
        self.over_resolution = 4
    
    '''
        setOverResolution(over_resolution):
        Set the over resolution for the test bench.
        Parameters:
            over_resolution (int): The over resolution to be set.
        Returns:
            None
    '''
    def setOverResolution(self, over_resolution):
        self.over_resolution = over_resolution


    def measure_static_nonlinearity(self, _instance, verbose=False):
        # Sub-resolution step size
        m_lsb = self.reference_voltage * 2 / (2 ** self.resolution)
        m_codes = [i for i in range(2 ** self.resolution)]
        m_step_size = m_lsb / self.over_resolution
        m_input_voltage = [i * m_step_size - self.reference_voltage for i in range((2 ** self.resolution) * self.over_resolution + 1)]
        m_output_code = [0] * len(m_input_voltage)

        # There should be one more stair value than the number of codes
        m_stairs = [0] * (len(m_codes) + 1)
        r_dnl = [0] * len(m_codes)
        for i in range(len(m_input_voltage)):
            m_dec = _instance.convertToDecimal(m_input_voltage[i])
            m_output_code[i] = m_dec
            if i == 0:
                m_stairs[0] = m_input_voltage[0]
            elif m_output_code[i] > m_output_code[i - 1]:
                m_stairs[m_dec] = m_input_voltage[i]
                r_dnl[m_dec - 1] = (m_stairs[m_dec] - m_stairs[m_dec - 1]) / m_lsb - 1
            elif m_output_code[i] < m_output_code[i - 1]:
                if verbose:
                    print("[Error]: Testbench.measure_static_nonlinearity: Output voltage did not increase monotonically.")
            else:
                continue
        r_inl = np.cumsum(r_dnl)
        return r_dnl, r_inl
    '''
        plot_static_nonlinearity(m_instance):
        Measure and plot the nonlinearity figures.
        Parameters:
            _instance (AbstractADC): The ADC instance to be tested.
        Returns:
            None
    '''
    def plot_static_nonlinearity(self, _instance, verbose=False):
        m_dnl, m_inl = self.measure_static_nonlinearity(_instance, verbose=verbose)
        m_codes = [i for i in range(2 ** self.resolution)]
        pg.plot(m_codes, m_dnl)
        pg.xlabel("Code")
        pg.ylabel("DNL/INL (LSB)")
        pg.title("SAR ADC DNL/INL Plot")
        pg.plot(m_codes, m_inl, color='orange')
        pg.grid()
        pg.show()