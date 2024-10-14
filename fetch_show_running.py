import json
import sys
from pycentral import Central

def get_running_config(token, serial_number, device_type):
    central = Central(token=token)
    
    params = {
        "serial_number": serial_number,
        "device_type": device_type
    }

    try:
        running_config = central.device.get_running_config(**params)
        print(json.dumps(running_config, indent=4))
    
    except Exception as e:
        print(f"Error retrieving running config: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <token> <serial_number> <device_type>")
        sys.exit(1)

    script_name = sys.argv[0]
    token = sys.argv[1]
    serial_number = sys.argv[2]
    device_type = sys.argv[3]

    print(f"Script Name: {script_name}")
    print(f"Central API Token: {token}")
    print(f"Serial Number: {serial_number}")
    print(f"Device Type: {device_type}")

    get_running_config(token, serial_number, device_type)
