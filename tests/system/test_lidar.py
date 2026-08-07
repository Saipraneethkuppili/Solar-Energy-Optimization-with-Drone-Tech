from src.hardware.lidar.manager import TFLunaManager

driver = TFLunaManager()

print("TF-LUNA Driver Imported Successfully")
print("Default Port :", driver.port)
print("Baudrate     :", driver.baudrate)