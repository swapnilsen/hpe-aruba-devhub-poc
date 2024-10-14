import sys

def main():
    if len(sys.argv) != 5:
        print("Usage: python script_name.py <input_param>")
        sys.exit(1)
    
    script_name = sys.argv[0]
    base_url = sys.argv[1]
    central_api_token = sys.argv[2]
    serial_num = sys.argv[3]
    device_type = sys.argv[4]

    print(f"Script Name: {script_name}")
    print(f"Central Base URL: {base_url}")
    print(f"Central API Token: {central_api_token}")
    print(f"Serial Number: {serial_num}")
    print(f"Device Type: {device_type}")
    

if __name__ == "__main__":
    main()
