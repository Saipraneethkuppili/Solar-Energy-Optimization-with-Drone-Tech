from pprint import pprint

from src.hub.sensor_hub import SensorHub


def main():
    hub = SensorHub()

    hub.initialize()

    pprint(hub.read_all())

    hub.shutdown()


if __name__ == "__main__":
    main()