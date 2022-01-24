# open-cv-2022

OpenCV and OpenNI gamepiece detection code to be used on the 2022 robot.

Features NetworkTables integration to send various datapoints to driver's station and robot.

## Contributing

### Dependencies

Dependencies are in `requirements.txt`.
Commands to install these:

Windows: `py -3 -m pip install -r requirements.txt` (while working directory is set to project directory)

macOS/Linux: `pip3 install -r requirements.txt` (while working directory is set to project directory)

It is highly recommended to install dependencies in a virtual environment. If you need help creating this, refer to the [Python documentation](https://docs.python.org/3/library/venv.html).

On macOS, make sure you install Python 3 separately and do not use the system install (package installation will fail when not run as root).

In order to use this project with an Astra camera, you must have Orbbec's flavor of OpenNI installed. See [Orbbec's develop page](https://orbbec3d.com/index/Download.html) and move all the way to the bottom to install their `Orbbec OpenNI SDK`. Follow the instructions in the README for your system.

### Constants and Config

Do not commit changes to the `constants.py` file. These values have been calibrated for individual cameras and game pieces and need not be changed. You may, however, edit the `config.py` file (on your local machine, again do not commit this) to change the project's function (i.e. switching to your computer's webcam instead of using the Astra, disabling NetworkTables when not connected to a robot/testbench, or enabling a video feed).

### Code Quality and Standards

Refer to the TechHOUNDS coding style guide. Although this is for Java, there is still valuable information for other languages. If your question is not answered by that, use the Google style guide for Python. Documentation is expected for all modules, classes, and functions, and all functions should be type-hinted. For all difficult to understand code, either simplify it or add comments.

Note: for consistency's sake, whenever using both blue and red detection in the same function the order for params and return vars should be `blue, red`.
