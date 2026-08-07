from src.mission.manager import MissionManager
from src.mission.metadata import MissionMetadata


def main():

    manager = MissionManager()

    mission = manager.create()

    metadata = MissionMetadata()

    metadata.save(mission)

    print()

    print("Mission Created Successfully")

    print(mission)


if __name__ == "__main__":
    main()