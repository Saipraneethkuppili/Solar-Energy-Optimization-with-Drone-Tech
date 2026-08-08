from src.telemetry.simulator import SimulatedTelemetry
from src.telemetry.recorder import TelemetryRecorder


def main():

    telemetry = SimulatedTelemetry()

    telemetry.connect()

    recorder = TelemetryRecorder(
        "reports/telemetry.csv"
    )

    recorder.start()

    for _ in range(5):

        data = telemetry.read()

        recorder.record(data)

    recorder.close()

    telemetry.disconnect()

    print()
    print("Telemetry recording completed.")
    print("Output: reports/telemetry.csv")


if __name__ == "__main__":
    main()