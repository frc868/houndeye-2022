import frc_vision.astra.driver


def main():
    d = frc_vision.astra.driver.Driver()
    d.run(enable_calibration=True)


if __name__ == "__main__":
    main()
