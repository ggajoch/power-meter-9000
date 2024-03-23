# Device usage

Device has `power-meter-9000.yaml` flashed by default.

This means that the device has captive portal by default with its WiFi in AP mode.

To change WiFi credentials and connect to home assistant:
 - power on the device
 - connect to the WiFi of the device (`power-meter-9000` with password `power-meter-9000`)
 - change WiFi credentials
 - device should be discovered in Home Assistant

# To flash

Use ESPHome -> new device -> prepare for first use -> modern format

Use https://adafruit.github.io/Adafruit_WebSerial_ESPTool/ tool to flash binary to address 0x0.

Then, using ESPHome flash firmware with sensors enabled.