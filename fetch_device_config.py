import sys
from pycentral.base import ArubaCentralBase
from pycentral.configuration import Devices

def collect_running_config(base_url, api_token, serial_number, device_type):
    central = ArubaCentralBase(
        central_info={
            "base_url": base_url,
            "token": {"access_token": api_token}
        }
    )

    devices = Devices()

    if device_type in ['Switch-AOS-CX', 'Switch-AOS', 'IAP', 'Gateway']:
        response = devices.get_devices_configuration(
            central,
            device_serial=serial_number
        )

        if response['code'] == 200:
            print(f"=====######=====<<< Running Config for {serial_number} >>>=====######=====")
            print(response['msg'])
            print(f"=====######=====<<< END >>>=====######=====")
        else:
            print(f"Failed to fetch running config: {response}")
    else:
        print(f"Device type {device_type} not supported.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 <script_name>.py <base_url> <api_token> <serial_number> <device_type>")
        sys.exit(1)

    script_name = sys.argv[0]
    base_url = sys.argv[1]
    api_token = sys.argv[2]
    serial_number = sys.argv[3]
    device_type = sys.argv[4]

    print(f"Script Name: {script_name}")
    print(f"Central Base URL: {base_url}")
    print(f"Central API Token: {api_token}")
    print(f"Serial Number: {serial_number}")
    print(f"Device Type: {device_type}")
    
    collect_running_config(base_url, api_token, serial_number, device_type)
