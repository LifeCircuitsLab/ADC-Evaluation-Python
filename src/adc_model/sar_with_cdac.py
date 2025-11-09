from src.adc_model.abstract_adc import AbstractADC
import random
import math

class SARWithCDAC(AbstractADC):

    def __init__(self, reference_voltage=1, bit_resolution=10, cmp_threshold=0):
        self.reference = reference_voltage # The ADC works between +/- reference_voltage
        self.cmp_threshold = cmp_threshold
        self.bit = bit_resolution

        # Two types of bit weights are constructed here:
        # 1. _bit_weight: The ideal bit weight used for reconstruction
        # 2. real_bit_weight: The real bit weight used for conversion including mismatch
        # Redundancy can be added by changing the bit_weight after initialization
        # To accommodate this, the bit_weight property needs to watch the setting process, and is renamed as _bit_weight internally
        self._bit_weight = [2**(self.bit - i - 1) for i in range(self.bit)]
        self.real_bit_weight = self._bit_weight.copy()

        # Base cap is the capacitor stay connected to ground.
        # By default, it is set to 1 unit cap, and subject to mismatch, captured by real_base_cap.
        self._base_cap = 1
        self.real_base_cap = self._base_cap

        # Sum cap is a helper variable to speed up calculation
        self.real_sum_cap = sum(self.real_bit_weight) + self.real_base_cap
        self.ideal_sum_cap = sum(self._bit_weight) + self._base_cap

    '''
    Getter and Setter for bit_weight property'''
    @property
    def bit_weight(self):
        return self._bit_weight
    
    @bit_weight.setter
    def bit_weight(self, new_bit_weight):
        # Call back to update all necessary variables
        self._bit_weight = new_bit_weight
        self.real_bit_weight = new_bit_weight.copy()
        self.ideal_sum_cap = sum(self._bit_weight) + self._base_cap
        self.real_sum_cap = sum(self.real_bit_weight) + self.real_base_cap

    '''
        setReference(ref_voltage):
        Set the reference voltage for the SAR algorithm.
        Parameters:
            ref_voltage (float): The reference voltage to be set. Note that the SAR will convert anything between -ref_voltage to +ref_voltage.
        Returns:
            None
    '''
    def setReference(self, ref_voltage):
        self.reference = ref_voltage

    '''
        addMismatch(unit_relative_mismatch=0.05):
        Add mismatch to the capacitor array based on a Gaussian distribution.
        Parameters:
            unit_relative_mismatch (float): The unit relative mismatch to be applied to the capacitor array.
        Returns:
            None
    '''
    def addMismatch(self, unit_relative_mismatch=0.05, verbose=False):
        # Using the ideal bit weight to generate mismatch
        for i in range(len(self._bit_weight)):
            mismatch_factor = random.gauss(1, unit_relative_mismatch/math.sqrt(self._bit_weight[i]))
            self.real_bit_weight[i] = self._bit_weight[i] * mismatch_factor
            if verbose: 
                print(f"Capacitor {i}: Weight = {self.real_bit_weight[i]}, Mismatch Factor = {1-mismatch_factor}")
        mismatch_factor = random.gauss(1, unit_relative_mismatch/math.sqrt(self._base_cap))
        self.real_base_cap = self._base_cap * mismatch_factor
        if verbose:
            print(f"Base Capacitor: Weight = {self.real_base_cap}, Mismatch Factor = {1-mismatch_factor}")
        self.real_sum_cap = sum(self.real_bit_weight) + self.real_base_cap

    '''
        convertToBitstream(input_data):
        Convert the input data using the CDAC based SAR. The SAR operates in a binary search manner.
        Parameters:
            input_data (float): The voltage to be convertered.
            test_vector (list, optional): A test vector to be used for debugging purposes. Defaults to None.
        Returns:
            bit_stream (list[ len(bit_weight) ]): The converted bit stream with MSB first. The length will be identical to the size of the bit_stream. Uses reference voltage defined in the class.
    '''
    def convertToBitstream(self, input_data):
        # The test_vector is used for debugging purposes only.
        # If provided, the SAR algorithm will use the test_vector as the starting point for conversion to carry debugging information
        r_bit_stream = [0] * len(self.real_bit_weight)
        for i in range(len(self.real_bit_weight)):
            if input_data >= self.cmp_threshold:
                r_bit_stream[i] = 1
                input_data -= self.reference * self.real_bit_weight[i] / self.real_sum_cap
            else:
                r_bit_stream[i] = 0
                input_data += self.reference * self.real_bit_weight[i] / self.real_sum_cap
        return r_bit_stream
    
    '''
        convertToDecimal(input_data):
        Convert the input data to decimal using SAR algorithm parameters.
        Parameters:
            input_data (float): The voltage to be convertered.
        Returns:
            decimal_value (int): The converted decimal value ranging from 0 to 2^N-1. 
    '''
    def convertToDecimal(self, input_data):
        # Convert to decimal do not support debugging mode.
        m_bit_stream = self.convertToBitstream(input_data)
        r_decimal_value = int(0)
        for i in range(len(m_bit_stream)):
            r_decimal_value += int(m_bit_stream[i] * self._bit_weight[i])
        return r_decimal_value
    
    '''
        reconstruct(bit_stream):
        Reconstruct the voltage from the bit stream using SAR algorithm parameters.
        Parameters:
            bit_stream (list[ len(bit_weight) ]): The bit stream to be reconstructed.
        Returns:
            voltage (float): The reconstructed voltage using reference voltage defined in the class.
    '''
    def reconstruct(self, bit_stream):
        voltage = 0
        for i in range(len(self._bit_weight)):
            voltage += (2 * bit_stream[i] - 1) * self.reference * self._bit_weight[i] / self.ideal_sum_cap
        return voltage