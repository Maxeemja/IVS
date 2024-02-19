from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config



class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str
    ) -> None:
        pass

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        return AggregatedData(
            Accelerometer(1, 2, 3),
            Gps(4, 5),
            Parking(1, Gps(10, 5)),
            datetime.now(),
            config.USER_ID,
        )

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
