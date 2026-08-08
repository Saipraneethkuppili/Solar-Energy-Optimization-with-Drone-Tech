from src.telemetry.pixhawk_telemetry import PixhawkTelemetry


def main():

    telemetry = PixhawkTelemetry()

    print("Pixhawk telemetry module loaded successfully.")

    print(f"Port     : {telemetry.connection_string}")
    print(f"Baudrate : {telemetry.baud}")


if __name__ == "__main__":
    main()
