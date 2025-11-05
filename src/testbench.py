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

    '''
        run(m_instance):
        Run the test bench on the given ADC instance.
        Parameters:
            m_instance (AbstractADC): The ADC instance to be tested.
        Returns:
            None
    '''
    def plot_static_nonlinearity(self, m_instance):
        # Sub-resolution step size
        m_lsb = self.reference_voltage * 2 / (2 ** self.resolution)
        m_codes = [i for i in range(2 ** self.resolution)]
        m_step_size = m_lsb / self.over_resolution
        m_input_voltage = [i * m_step_size - self.reference_voltage for i in range((2 ** self.resolution) * self.over_resolution + 1)]
        m_output_code = [0] * len(m_input_voltage)

        # There should be one more stair value than the number of codes
        m_stairs = [0] * (len(m_codes) + 1)
        m_dnl = [0] * len(m_codes)
        for i in range(len(m_input_voltage)):
            m_dec = m_instance.convertToDecimal(m_input_voltage[i])
            m_output_code[i] = m_dec
            if i == 0:
                m_stairs[0] = m_input_voltage[0]
            elif m_output_code[i] > m_output_code[i - 1]:
                m_stairs[m_dec] = m_input_voltage[i]
                m_dnl[m_dec - 1] = (m_stairs[m_dec] - m_stairs[m_dec - 1]) / m_lsb - 1
            elif m_output_code[i] < m_output_code[i - 1]:
                print("Error: Output voltage did not increase monotonically.")
            else:
                continue
        # Plot the results
        m_inl = np.cumsum(m_dnl)
        pg.plot(m_codes, m_dnl)
        pg.xlabel("Code")
        pg.ylabel("DNL/INL (LSB)")
        pg.title("SAR ADC DNL/INL Plot")
        pg.plot(m_codes, m_inl, color='orange')
        pg.grid()
        pg.show()