from src.adc_model.sar_with_cdac import SARWithCDAC
from src.testbench import testbench
import matplotlib.pyplot as pg
import numpy as np

# Test metadata
g_dut_data = {
    "adc_resolution": 12,
    "adc_type": "SAR",
    "mismatch_level": 0.01
}

g_tb_config = {
    "voltage_sub_resolution": 32
}

def wrapper():
    m_sar_model = SARWithCDAC(bit_resolution=g_dut_data["adc_resolution"])
    m_sar_model_wredundancy = SARWithCDAC(bit_resolution=g_dut_data["adc_resolution"])
    m_sar_model_wredundancy.bit_weight = [2**11, 2**10, 2**8, 2**8, 2**8, 2**7, 2**6, 2**4, 2**4, 2**4, 2**3, 2**2, 1, 1, 1]
    m_test_bench = testbench(resolution=g_dut_data["adc_resolution"])
    m_test_bench.setOverResolution(g_tb_config["voltage_sub_resolution"])
    m_max_iterations = 100
    m_max_dnl_regular = [0] * m_max_iterations
    m_max_inl_regular = [0] * m_max_iterations
    m_max_dnl_redundancy = [0] * m_max_iterations
    m_max_inl_redundancy = [0] * m_max_iterations
    for i in range(m_max_iterations):
        m_sar_model.addMismatch(unit_relative_mismatch = g_dut_data["mismatch_level"])
        i_dnl, i_inl = m_test_bench.measure_static_nonlinearity(m_sar_model)
        m_max_dnl_regular[i] = max(np.abs(i_dnl))
        m_max_inl_regular[i] = max(np.abs(i_inl))
    for i in range(m_max_iterations):
        m_sar_model_wredundancy.addMismatch(unit_relative_mismatch = g_dut_data["mismatch_level"])
        i_dnl, i_inl = m_test_bench.measure_static_nonlinearity(m_sar_model_wredundancy)
        m_max_dnl_redundancy[i] = max(np.abs(i_dnl))
        m_max_inl_redundancy[i] = max(np.abs(i_inl))
    
    m_bins = np.linspace(0, 1, 21)
    pg.figure(1)
    pg.hist(m_max_dnl_regular, bins=m_bins, alpha=0.5, label="Regular SAR")
    pg.hist(m_max_dnl_redundancy, bins=m_bins, alpha=0.5, label="SAR with Redundancy")
    pg.xlabel("Max DNL (LSB)")
    pg.ylabel("Occurrences")
    pg.title("Max DNL Distribution Comparison")
    pg.legend()

    pg.figure(2)
    pg.hist(m_max_inl_regular, bins=m_bins, alpha=0.5, label="Regular SAR")
    pg.hist(m_max_inl_redundancy, bins=m_bins, alpha=0.5, label="SAR with Redundancy")
    pg.xlabel("Max INL (LSB)")
    pg.ylabel("Occurrences")
    pg.title("Max INL Distribution Comparison")
    pg.legend()
    pg.show()

if __name__ == "__main__":
    wrapper()