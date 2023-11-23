import pyudev
import subprocess
import logging
import time

# Constants
LOG_FILE_PATH = './log/logfile.log'
DESTINATION_PATH = ' /mnt/media-drive/Media/blu-ray-archive/'  # Replace with desired destination path

def detect_blu_ray_insertion():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='disk')

    for device in iter(monitor.poll, None):
        if 'ID_CDROM' in device.get('ID_CDROM', ''):
            if device.action == 'add':
                logging.info("Blu-ray disk detected.")
                return device.device_node

def copy_blu_ray_contents(device_node, destination_path):
    

    try:
        logging.info(f"Copying Blu-ray contents from {device_node} to {destination_path}...")
        subprocess.run(['dd', f'if={device_node}', f'of={destination_path}'])

        logging.info(f"Blu-ray contents copied successfully to {destination_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while copying Blu-ray contents: {e}")
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")


def setupLogging():
    logger = logging.getLogger('blu_ray_copy')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    
if __name__ == "__main__":
    setupLogging()
    while True:
        logging.info("Waiting for a Blu-ray disk to be inserted...")
        inserted_device = detect_blu_ray_insertion()
        if inserted_device:
            copy_blu_ray_contents(inserted_device, DESTINATION_PATH)
        time.sleep(5)  # Adjust the delay as needed
