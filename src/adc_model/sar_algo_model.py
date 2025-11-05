from src.adc_model.abstract_adc import AbstractADC
import random
import math

class SARAlgorithmModel(AbstractADC):

    def __init__(self, reference_voltage=1, bit_resolution=10, cmp_threshold=0):
        self.reference = reference_voltage
        self.cmp_threshold = cmp_threshold
        self.bit = bit_resolution
        self.bit_weight = [2**(self.bit - i - 1) for i in range(self.bit)]
        self.base_cap = 1
        self.sum_cap = sum(self.bit_weight) + self.base_cap

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
    def addMismatch(self, unit_relative_mismatch=0.05):
        for i in range(len(self.bit_weight)):
            mismatch_factor = random.gauss(1, unit_relative_mismatch/math.sqrt(self.bit_weight[i]))
            self.bit_weight[i] = self.bit_weight[i] * mismatch_factor
            print(f"Capacitor {i}: Weight = {self.bit_weight[i]}, Mismatch Factor = {1-mismatch_factor}")
        mismatch_factor = random.gauss(1, unit_relative_mismatch/math.sqrt(self.base_cap))
        self.base_cap = self.base_cap * mismatch_factor
        print(f"Base Capacitor: Weight = {self.base_cap}, Mismatch Factor = {1-mismatch_factor}")
        self.sum_cap = sum(self.bit_weight) + self.base_cap

    '''
        convert(input_data):
        Convert the input data using SAR algorithm parameters.
        Parameters:
            input_data (float): The voltage to be convertered.
        Returns:
            bit_stream (list[ len(bit_weight) ]): The converted bit stream with MSB first. The length will be identical to the size of the bit_stream. Uses reference voltage defined in the class.
    '''
    def convert(self, input_data):
        r_bit_stream = [0] * len(self.bit_weight)
        # Set the comparator threashold
        for i in range(len(self.bit_weight)):
            if input_data >= self.cmp_threshold:
                r_bit_stream[i] = 1
                input_data -= self.reference * self.bit_weight[i] / self.sum_cap
            else:
                r_bit_stream[i] = 0
                input_data += self.reference * self.bit_weight[i] / self.sum_cap
        return r_bit_stream
    
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
        for i in range(len(self.bit_weight)):
            voltage += (2 * bit_stream[i] - 1) * self.reference * self.bit_weight[i] / self.sum_cap
        return voltage