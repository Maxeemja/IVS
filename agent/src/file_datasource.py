from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        
    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        try:
            x,y,z = self.ax.__next__()
        except:
            self.accelerometer_file.seek(0,0)
            x,y,z = self.ax.__next__()
            x,y,z = self.ax.__next__()
        try:
            lg, lt = self.gps.__next__()
        except:
            self.gps_file.seek(0,0)
            lg, lt = self.gps.__next__()
            lg, lt = self.gps.__next__()
        return AggregatedData(
            Accelerometer(x,y,z),
            Gps(lg,lt),
            datetime.now(),
            config.USER_ID,
        )
        
        
    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file =  open(self.accelerometer_filename, newline='')
        self.gps_file = open(self.gps_filename, newline='')
        self.ax = reader(self.accelerometer_file, delimiter=',', quotechar='|')
        self.gps = reader(self.gps_file, delimiter=',', quotechar='|')
        self.ax.__next__()
        self.gps.__next__()
        
    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.accelerometer_file.close
        self.gps_file.close

def go():
    accelerometer_file =  open("data/accelerometer.csv", 'r')
    gps_file = open("data/gps.csv", 'r')
    ax = reader(accelerometer_file, delimiter=',', quotechar='|')
    gps = reader(gps_file, delimiter=',', quotechar='|')
    print(ax.__next__())
    print(ax.__next__())

if __name__ == "__main__":
    go()