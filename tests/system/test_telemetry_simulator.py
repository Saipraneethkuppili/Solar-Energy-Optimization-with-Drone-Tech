from src.telemetry.simulator import SimulatedTelemetry


def main():

    telemetry = SimulatedTelemetry()

    telemetry.connect()

    data = telemetry.read()

    print()
    print("SIMULATED TELEMETRY")
    print("=" * 40)

    print(data)

    telemetry.disconnect()


if __name__ == "__main__":
    main()