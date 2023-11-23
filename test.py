import pyudev
from pprint import pprint

# Create a device monitor
monitor = pyudev.Monitor()

# Watch for device events
for event in monitor.poll():
  # Check if the event is a device added event
  if event.action == "add" and event.devtype == "block":
    # Get the device object
    device = event.device
    pprint(device)

    # Check if the device is a blu ray drive
    if device.get("ID_MODEL") == "Samsung BL-LC22N70":
      # Do something when a blu ray disk is inserted
      print("A blu ray disk has been inserted")