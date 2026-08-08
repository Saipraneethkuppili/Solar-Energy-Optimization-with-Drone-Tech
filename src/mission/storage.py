"""
Mission Storage Utilities

Handles copying images, reports and annotated
results into the mission directory.
"""

import shutil
from pathlib import Path


class MissionStorage:
    """Store mission-related files."""

    def copy_image(
        self,
        image,
        mission: Path,
    ) -> Path:
        """Copy an input image into the mission."""

        image = Path(image)

        destination = (
            mission / "images" / image.name
        )

        shutil.copy2(
            image,
            destination,
        )

        return destination

    def copy_report(
        self,
        report,
        mission: Path,
    ) -> Path:
        """Copy a report into the mission."""

        report = Path(report)

        destination = (
            mission / "reports" / report.name
        )

        shutil.copy2(
            report,
            destination,
        )

        return destination

    def copy_annotated(
        self,
        annotated_folder,
        mission: Path,
    ):
        """Copy annotated images into the mission."""

        annotated_folder = Path(
            annotated_folder
        )

        destination = (
            mission / "annotated"
        )

        copied_files = []

        for image in annotated_folder.iterdir():

            if not image.is_file():
                continue

            target = (
                destination / image.name
            )

            shutil.copy2(
                image,
                target,
            )

            copied_files.append(target)

        return copied_files