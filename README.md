# OpenPaw SlimeVR Tracker Firmwares
In this repo you can find compiled firmware for OpenPaw Labs DIY SlimeVR Tracker Boards as well as instructions for manually flashing.

## Automatic updating through SlimeVR Desktop
Currently automated updating the trackers to the latest version in SlimeVR Desktop is not supported for 3rd party trackers. We are working to add this functionality to SlimeVR Desktop, however for now you will need to manually update your trackers by following the steps below.

## Manually updating Trackers using SlimeVR Desktop
To update your trackers to the latest SlimeVR Tracker versions follow the steps below.

1. Open SlimeVR Desktop
2. Click on "Settings" in the bottom left corner.
3. Scroll down and under the "Utilities" section select the "DIY Firmware Tool"
4. Configure the firmware settings as defined below for the specific tracker you are updating. You can check the bottom of the tracker PCB to find the product identifier.
5. Once you have selected the firmware and configured the board settings, click "Looks good" to go to the next step.
6. The firmware will build with our selected settings, this may take a few minutes.
7. Select Flashing Method.
* Power on your tracker. If your tracker has already been setup in SlimeVR and is connected over WiFi, you can select `Wi-Fi` as your flashing method.
    - Your tracker(s) should show up under "Detected OTA Devices". Select the ones you want to update, then click "Next Step".
    - The firmware will be uploaded to all your trackers at the same time, then you should get a success message saying "Update Complete!
    - You are done!
* If your tracker is not connected to Wi-Fi you will need to plug it into your computer directly, power it on, and then select `USB` as your flashing method.
    - Enter in your WiFi network name and Password
    - Click the dropdown for "Detected Serial Devices" and select `USB-SERIAL CH340 (COM...)`.
    - Click "Next Step"
    - It will upload the firmware over the USB connection and apply the update. It will then connect the tracker to your configured WiFi network. 
    - If you have more trackers you want to flash select "Flash more trackers" and plug in your next tracker to update it.
8. You should be done! If you are having issues, check the troubleshooting steps below.

### OpenPaw DIY SlimeVR ESP Tracker (BB-LSM6DSV) (Blueberry Cheesecake)
We mostly use the defaults for this board, but they are provided here for exact reference! We have highlighted the settings that are different from the default here for clarity, but be sure to double check each setting!

1. Select the firmware to flash
- Firmware Source: `SlimeVR-Tracker-ESP`
- **Board Type: `NodeMCU` (scroll down to find)**
- Firmware Version: The version number you would like to flash, generally select the latest one.
2. Configure your board
- I2C Imu (1)
    - Protocol: `I2C`
    - **Imu Type: `IMU_LSM6DSV`**
    - SDA Pin: `D2`
    - SCL Pin: `D1`
    - INT Pin: `D5`
    - IMU Address: **leave blank**
    - **IMU Rotation: `DEG_0` - NOTE: This is different than the default!**
- I2C Imu (2)
    - Click the trash can icon to delete the second IMU, this board only supports a single IMU.
- Led Settings
    - Led Pin: `2`
    - Led Inverted: `Enabled` 
- Battery Settings
    - Type: `BAT_EXTERNAL`
    - Battery Shield Resistor (Ohms): `180`
    - R1 (Ohms): `100`
    - R2 (Ohms): `220`
    - Battery Pin: `A0`

## Troubleshooting
Having issues with flashing, running the setup wizard, or issues with your tracker not connecting to your WiFi? Try to follow these troubleshooting steps. If you are still having issues, join our Discord server to get direct help!

1. Factory Reset your Tracker
    1. Open SlimeVR Desktop
    2. Select `Settings` in the lower left corner
    3. Scroll down and select `Serial Console` under the `Utilities` section.
    4. Plug in your tracker with a USB-C cable and power it on.
    5. Click on the dropdown under the command box that says "Auto" and select the `USB-SERIAL CH340 (COM...)` device from the list.
    6. Click the `Reboot` button and wait a few seconds. You should see the serial console list information about the tracker once it reboots.
    7. Click the `Factory Reset` button, then select "I know what I'm doing"
    8. In the left menu select the `Setup Wizard` under the `Utilities` section
    9. Follow the setup wizard to connect your tracker to WiFi again.
2. If you are still unable to flash or connect your tracker to WiFi, please reach out to us on the OpenPaw Discord server and we will try to help you!