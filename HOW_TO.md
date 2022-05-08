# How To Use This Repository

If you're reading this, you're probably trying to figure out how to calibrate the Astra and use it for path-finding. If so, this guide is here to help!

Note: in any commands, do not type the `$` part. That signifies that the command should be run in a normal terminal. `#` signifies a root terminal.

## Introduction

### How the project works

Here's a quick rundown of what goes on when the program(s) are running, along with a wiring guide.

The Raspberry Pi is powered via a DC-DC converter that is plugged in to the PDP/PDH. Since the DC-DC converter does not supply enough power for the Astra and Raspberry Pi combined, we use a powered USB hub that connects to one of the 5v/2a ports on the VRM. The Astra is connected to that hub, and by extension to the Raspberry Pi.

As for software, the image feed from the Astra is read through OpenNI and is processed with OpenCV. Data of each ball that is detected by the camera is published to a NetworkTables table named "HoundEye" in order of distance. `main.py` runs on the Raspberry Pi and is responsible for the main (as the name implies) driver. The process _should_ automatically revive itself if there is a problem. It also has networking capabilities, where it's responding to connection requests in the background. This allows the image with all relevant annotations (FPS, balls on the field highlighted, distances, etc) to be sent to the driver's station.

On the driver's station, `client.py` is run to connect simultaneously to the Raspberry Pi to display the Astra camera feed and to the Limelight to display its feed. Press `ESC` to exit the client window, and `x` (currently) to change inputs.

### Command-line Arguments (`main.py`)

`--enable-calibration` enables the viewer where you can change HSV values.

`--disable-networking` disables connections to the Raspberry Pi. Helpful when not connected to the radio and in testing.

### Connecting to the Pi

The Pi is on `10.8.68.150`. To log in via SSH, run `$ ssh pi@10.8.68.150` and type `techhounds` as the password.

To log in via VNC, open VNC Viewer and open `10.8.68.150` (it should already be on the Driver Station).

## Calibration

You need to use VNC Viewer on the Driver Station computer in order to access a display on the Pi. Once logged in via VNC, run `$ cd open-cv-2022`, then `python3 main.py --enable-calibration`. If you get any socket errors, try `python3 main.py --enable-calibration --disable-networking`.

Once in the interface, you should see several windows with images, along with sliders for the HSV values.

### HSV

Here's a quick crash course on HSV. HSV is just another color system, like RGB (like you're probably used to) and CMYK (on printers).

    H: Hue
    S: Saturation
    V: Value

#### Hue

Hue is the color portion of the model, expressed as a number from 0 to 360 degrees (we use 0 to 179, which scales linearly to 0-360):

    Red falls between 0 and 60 degrees.
    Yellow falls between 61 and 120 degrees.
    Green falls between 121 and 180 degrees.
    Cyan falls between 181 and 240 degrees.
    Blue falls between 241 and 300 degrees.
    Magenta falls between 301 and 360 degrees.

#### Saturation

Saturation describes the amount of gray in a particular color, from 0 to 100 percent (0-255 for us). Reducing this component toward zero introduces more gray and produces a faded effect.

#### Value (or Brightness)

Value works in conjunction with saturation and describes the brightness or intensity of the color, from 0 to 100 percent, where 0 is completely black, and 100 is the brightest and reveals the most color.

### Circle Comparison Threshold

In order to detect whether or not something is a circle, we need to first detect all objects in the frame, then decide whether or not they are circles. The first step is done by `cv2.findContours()`, which uses the Canny edge detector in the background. After that is the cool stuff. We run `cv2.minEnclosingCircle` to find the x, y, and r values of the minimum circle that can enclose the contour. Intuitively, if the contour is a circle, the minimum enclosing circle around that contour has to be pretty similar to the contour itself. As such, we can divide the area of the minimum enclosing circle and the contour and make a comparison. If that proportion is within a certain threshold, then we know that that contour (object) is a circle. If you increase this threshold, you will detect more circles.

### Actually Calibrating Things

To begin, set all of the minimum sliders to 0, and all of the maximum sliders to
