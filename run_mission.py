"""
Solar Energy Optimization - Mission Runner

Complete simulated solar-panel inspection mission.

Pipeline:
    MissionManager
        |
        +-- Input images
        |
        +-- YOLOv8 detection
        |
        +-- Telemetry recording
        |
        +-- MissionStorage
        |
        +-- MissionMetadata

Output:
    missions/
    └── mission_YYYYMMDD_HHMMSS/
        ├── images/
        ├── annotated/
        ├── reports/
        │   └── detections.csv
        ├── telemetry/
        │   └── telemetry.csv
        └── metadata.json
"""

import csv
from pathlib import Path

from ultralytics import YOLO

from src.mission.manager import MissionManager
from src.mission.storage import MissionStorage
from src.mission.metadata import MissionMetadata
from src.telemetry.simulator import SimulatedTelemetry
from src.telemetry.recorder import TelemetryRecorder
from src.reporting.inspection_report import InspectionReport


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = Path("models/weights/best.pt")

IMAGE_DIRECTORY = Path("datasets/mission")

CONFIDENCE_THRESHOLD = 0.25

IMAGE_SIZE = 640


# ============================================================
# DETECTION CSV
# ============================================================

def create_detection_csv(mission):
    """Create the detection CSV file and return file + writer."""

    output_file = mission / "reports" / "detections.csv"

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file = output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    )

    writer = csv.writer(file)

    writer.writerow(
        [
            "Image",
            "Class",
            "Confidence",
            "X1",
            "Y1",
            "X2",
            "Y2",
        ]
    )

    return file, writer


# ============================================================
# MAIN MISSION
# ============================================================

def main():

    print()
    print("=" * 60)
    print("SOLAR PANEL INSPECTION MISSION")
    print("=" * 60)

    # --------------------------------------------------------
    # Validate YOLO model
    # --------------------------------------------------------

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"YOLO model not found: {MODEL_PATH}"
        )

    # --------------------------------------------------------
    # Validate mission images
    # --------------------------------------------------------

    if not IMAGE_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Mission image directory not found: "
            f"{IMAGE_DIRECTORY}"
        )

    images = sorted(
        [
            image
            for image in IMAGE_DIRECTORY.iterdir()
            if image.is_file()
            and image.suffix.lower()
            in {
                ".jpg",
                ".jpeg",
                ".png",
            }
        ]
    )

    if not images:
        raise RuntimeError(
            f"No mission images found in "
            f"{IMAGE_DIRECTORY}"
        )

    # --------------------------------------------------------
    # Create mission
    # --------------------------------------------------------

    mission_manager = MissionManager()

    mission = mission_manager.create()

    print()
    print(
        f"Mission directory: {mission}"
    )

    # --------------------------------------------------------
    # Initialize storage
    # --------------------------------------------------------

    storage = MissionStorage()

    # --------------------------------------------------------
    # Initialize metadata
    # --------------------------------------------------------

    metadata = MissionMetadata()

    metadata.save(
        mission=mission,
        image_count=len(images),
        detection_count=0,
        telemetry_source="simulation",
        status="running",
    )

    # --------------------------------------------------------
    # Load YOLO model
    # --------------------------------------------------------

    print()
    print("Loading YOLOv8 model...")

    model = YOLO(
        str(MODEL_PATH)
    )

    print(
        "YOLOv8 model loaded successfully."
    )

    # --------------------------------------------------------
    # Start simulated Pixhawk
    # --------------------------------------------------------

    telemetry = SimulatedTelemetry()

    telemetry.connect()

    # --------------------------------------------------------
    # Start telemetry recorder
    # --------------------------------------------------------

    telemetry_file = (
        mission
        / "telemetry"
        / "telemetry.csv"
    )

    telemetry_recorder = TelemetryRecorder(
        str(telemetry_file)
    )

    telemetry_recorder.start()

    # --------------------------------------------------------
    # Create detection report
    # --------------------------------------------------------

    detection_file, detection_writer = (
        create_detection_csv(mission)
    )

    total_detections = 0

    # --------------------------------------------------------
    # Process mission images
    # --------------------------------------------------------

    try:

        for index, image in enumerate(
            images,
            start=1,
        ):

            print()
            print(
                f"[{index}/{len(images)}] "
                f"{image.name}"
            )

            # ------------------------------------------------
            # Copy original image
            # ------------------------------------------------

            storage.copy_image(
                image,
                mission,
            )

            # ------------------------------------------------
            # Record telemetry
            # ------------------------------------------------

            telemetry_data = telemetry.read()

            telemetry_recorder.record(
                telemetry_data
            )

            # ------------------------------------------------
            # Run YOLO detection
            # ------------------------------------------------

            results = model.predict(
                source=str(image),
                conf=CONFIDENCE_THRESHOLD,
                imgsz=IMAGE_SIZE,
                save=True,
                verbose=True,
            )

            # ------------------------------------------------
            # Extract detections
            # ------------------------------------------------

            for result in results:

                if result.boxes is None:
                    continue

                for box in result.boxes:

                    class_id = int(
                        box.cls[0].item()
                    )

                    confidence = float(
                        box.conf[0].item()
                    )

                    x1, y1, x2, y2 = (
                        box.xyxy[0]
                        .tolist()
                    )

                    class_name = model.names[
                        class_id
                    ]

                    detection_writer.writerow(
                        [
                            image.name,
                            class_name,
                            round(
                                confidence,
                                3,
                            ),
                            round(x1, 2),
                            round(y1, 2),
                            round(x2, 2),
                            round(y2, 2),
                        ]
                    )

                    total_detections += 1

            detection_file.flush()

    finally:

        # ----------------------------------------------------
        # Close detection report
        # ----------------------------------------------------

        detection_file.close()

        # ----------------------------------------------------
        # Close telemetry recorder
        # ----------------------------------------------------

        telemetry_recorder.close()

        # ----------------------------------------------------
        # Disconnect simulated Pixhawk
        # ----------------------------------------------------

        telemetry.disconnect()

    # --------------------------------------------------------
    # Copy YOLO annotated results
    # --------------------------------------------------------

    prediction_directory = Path(
        "runs/detect"
    )

    if prediction_directory.exists():

        prediction_runs = sorted(
            [
                path
                for path in prediction_directory.iterdir()
                if path.is_dir()
                and path.name.startswith(
                    "predict"
                )
            ],
            key=lambda path: path.stat().st_mtime,
        )

        if prediction_runs:

            latest_run = prediction_runs[-1]

            storage.copy_annotated(
                latest_run,
                mission,
            )

    # --------------------------------------------------------
    # Update metadata
    # --------------------------------------------------------

    metadata.save(
        mission=mission,
        image_count=len(images),
        detection_count=total_detections,
        telemetry_source="simulation",
        status="completed",
    )

    # --------------------------------------------------------
    # Generate inspection report
    # --------------------------------------------------------

    print()
    print("Generating inspection report...")

    inspection_report = InspectionReport(
        mission
    )

    json_report = inspection_report.save_json()
    text_report = inspection_report.save_text()

    print(
        f"Inspection JSON   : {json_report}"
    )

    print(
        f"Inspection report : {text_report}"
    )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("MISSION COMPLETED")
    print("=" * 60)

    print(
        f"Images processed    : {len(images)}"
    )

    print(
        f"Objects detected    : {total_detections}"
    )

    print(
        f"Mission directory   : {mission}"
    )

    print()
    print("Mission files:")

    print(
        f"  {mission}/images/"
    )

    print(
        f"  {mission}/annotated/"
    )

    print(
        f"  {mission}/reports/detections.csv"
    )

    print(
        f"  {mission}/telemetry/telemetry.csv"
    )

    print(
        f"  {mission}/metadata.json"
    )

    print("=" * 60)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
