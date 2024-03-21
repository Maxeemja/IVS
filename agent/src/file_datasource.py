from csv import reader
from typing import List
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.parking import Parking

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str, user_id: int) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.user_id = user_id
        pass
        
        
    def read(self) -> List[AggregatedData]:
        dataList = []
        for i in range(5):
            parking = next(self.parking_data_reader)
            dataList.append(
                AggregatedData(
                    Accelerometer(*next(self.accelerometer_data_reader)),
                    Gps(*next(self.gps_data_reader)),
                    Parking(parking[0], parking[1], parking[2]),
                    datetime.now(),
                    self.user_id
                )
            )
        return dataList
        
    def startReading(self, *args, **kwargs):
        self.accelerometer_data_reader = self.file_reader(self.accelerometer_filename)
        self.gps_data_reader = self.file_reader(self.gps_filename)
        self.parking_data_reader = self.file_reader(self.parking_filename)
        
        
    def stopReading(self, *args, **kwargs):
        pass
    
    
    def file_reader(self, path: str):
        while True:
            file = open(path)
            data_reader = reader(file)
            next(data_reader)
            for row in data_reader:
                yield row
            file.close()