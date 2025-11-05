from src.adc_model.sar_algo_model import SARAlgorithmModel
from src.testbench import testbench

# Test metadata
g_dut_data = {
    "adc_resolution": 12,
    "adc_type": "SAR",
    "mismatch_level": 0.005
}

g_tb_config = {
    "voltage_sub_resolution": 32
}

def wrapper():
    m_sar_model = SARAlgorithmModel(bit_resolution=g_dut_data["adc_resolution"])
    m_sar_model.addMismatch(unit_relative_mismatch = g_dut_data["mismatch_level"])
    m_test_bench = testbench(resolution=g_dut_data["adc_resolution"])
    m_test_bench.setOverResolution(g_tb_config["voltage_sub_resolution"])
    m_test_bench.plot_static_nonlinearity(m_sar_model)

if __name__ == "__main__":
    wrapper()