from src.hardware.sht31.manager import SHT31Manager

sensor = SHT31Manager()

sensor.connect()

print(sensor.read())

sensor.disconnect()
