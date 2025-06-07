from abc import ABC, abstractmethod

class WeightSensorInterface(ABC):
    @abstractmethod
    def read_weight(self) -> float:
        pass
