import argparse
import traceback

import frc_vision.astra.driver

parser = argparse.ArgumentParser(description="Run main driver program (on pi).")
parser.add_argument("--enable-calibration", action="store_true", dest="calibration")
parser.add_argument("--disable-networking", action="store_false", dest="networking")

args = parser.parse_args()


def main():
    d = frc_vision.astra.driver.Driver(
        enable_calibration=args.calibration, enable_networking=args.networking
    )
    d.run()


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()
        else:
            break
