from src.gb2ds import Gamebanana2Discord


if __name__ == "__main__":
    try:
        gb2ds = Gamebanana2Discord()
        gb2ds.start()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)