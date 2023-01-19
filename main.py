import argparse
import traceback

import houndeye.drivers
import houndeye.runner

parser = argparse.ArgumentParser(description="Run HoundEye.")
parser.add_argument("--enable-calibration", action="store_true", dest="calibration")
parser.add_argument("--disable-networking", action="store_false", dest="networking")

args = parser.parse_args()


def main():
    runner = houndeye.runner.Runner(
        [houndeye.drivers.j5Create()], args.enable_calibration, args.enable_networking
    )
    runner.run()


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
