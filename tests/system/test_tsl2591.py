from src.hardware.tsl2591.manager import TSL2591Manager


def main():
    sensor = TSL2591Manager()

    sensor.connect()

    print(sensor.read())

    sensor.disconnect()


if __name__ == "__main__":
    main()