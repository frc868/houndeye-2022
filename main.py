import frc_vision.astra.driver
# import frc_vision.recording
import frc_vision.webcam.driver

if __name__ == "__main__":
    d = frc_vision.astra.driver.Driver()
    d.run(view=False)
