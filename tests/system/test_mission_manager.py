from src.core.mission_manager import MissionManager


def main():

    manager = MissionManager()

    mission = manager.create_mission()

    print()

    print("Mission Created")

    print(mission)


if __name__ == "__main__":
    main()