# Solar Energy Optimization with Drone Techpython3 -c 'from pathlib import Path; Path("README.md").write_text("""# Solar Energy Optimization with Drone Tech

A drone-based solar-panel inspection platform combining YOLOv8 computer vision, simulated Pixhawk telemetry, mission analytics, automated reporting, REST APIs, and an interactive monitoring dashboard.

## Overview

The system performs an end-to-end solar-panel inspection mission:

1. Loads a YOLOv8 inspection model.
2. Processes mission images.
3. Detects solar panels and visible defects.
4. Stores detection results in CSV format.
5. Records mission telemetry.
6. Generates mission metadata.
7. Calculates mission health.
8. Generates JSON and text inspection reports.
9. Exposes mission information through FastAPI.
10. Displays mission status and analytics through Streamlit.

## System Architecture

```text
                    SOLAR INSPECTION SYSTEM
                             |
                      Mission Runner
                             |
                      Mission Dataset
                             |
                           YOLOv8
                             |
                     Detection Engine
                             |
             +---------------+---------------+
             |               |               |
        Detections       Telemetry       Metadata
           CSV               CSV             JSON
             |               |               |
             +---------------+---------------+
                             |
                    Detection Analytics
                             |
                    Mission Health Engine
                             |
              +--------------+--------------+
              |                             |
       Inspection Reports              FastAPI REST API
                                            |
                                            v
                                  Streamlit Dashboard
