from abc import ABC, abstractmethod

class AbstractADC(ABC):
    @abstractmethod
    def setReference(self, ref_voltage) -> None:
        pass

    @abstractmethod
    def convertToBitstream(self, input_data) -> list:
        pass

    @abstractmethod
    def convertToDecimal(self, input_data) -> int:
        pass

    @abstractmethod
    def reconstruct(self, bit_stream) -> float:
        pass