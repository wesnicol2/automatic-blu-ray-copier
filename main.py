import pyudev
import subprocess
import logging
import time

# Constants
LOG_FILE_PATH = './log/logfile.log'
DESTINATION_PATH = ' /mnt/media-drive/Media/blu-ray-archive/'  # Replace with desired destination path

logger = logging.getLogger('blu_ray_copy')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler and set the formatter
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



def detect_blu_ray_insertion():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='disk')

    for device in iter(monitor.poll, None):
        if 'ID_CDROM' in device.get('ID_CDROM', ''):
            if device.action == 'add':
                logger.info("Blu-ray disk detected.")
                return device.device_node

def copy_blu_ray_contents(device_node, destination_path):
    

    try:
        logger.info(f"Copying Blu-ray contents from {device_node} to {destination_path}...")
        subprocess.run(['dd', f'if={device_node}', f'of={destination_path}'])

        logger.info(f"Blu-ray contents copied successfully to {destination_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while copying Blu-ray contents: {e}")
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")

    
if __name__ == "__main__":
    while True:
        logger.info("Waiting for a Blu-ray disk to be inserted...")
        inserted_device = detect_blu_ray_insertion()
        if inserted_device:
            copy_blu_ray_contents(inserted_device, DESTINATION_PATH)
        time.sleep(5)  # Adjust the delay as needed
