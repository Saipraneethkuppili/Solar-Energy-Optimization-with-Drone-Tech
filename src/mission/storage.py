"""
Mission Storage Utilities
"""

import shutil
from pathlib import Path


class MissionStorage:

    def copy_image(self, image, mission):

        destination = mission / "images"

        shutil.copy(
            image,
            destination
        )

    def copy_report(self, report, mission):

        destination = mission / "reports"

        shutil.copy(
            report,
            destination
        )

    def copy_annotated(self, annotated_folder, mission):

        annotated = mission / "annotated"

        for image in Path(annotated_folder).glob("*"):

            shutil.copy(
                image,
                annotated
            )