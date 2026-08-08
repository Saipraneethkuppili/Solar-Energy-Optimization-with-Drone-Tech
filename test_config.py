from src.config.config_loader import ConfigLoader


def main():
    config = ConfigLoader()
    config.load()

    print("Project :", config.get("project", "name"))
    print("Version :", config.get("project", "version"))
    print("Pixhawk:", config.get("pixhawk", "port"))
    print("Camera FPS:", config.get("camera", "fps"))


if __name__ == "__main__":
    main()
