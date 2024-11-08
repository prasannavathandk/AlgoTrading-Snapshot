from Shop import Shop

def main() -> None:
    print("Starting Trading System...")
    mySystem = Shop()
    mySystem.open()
    print("Trading System is shut down.")

if __name__ == "__main__":
    main()    