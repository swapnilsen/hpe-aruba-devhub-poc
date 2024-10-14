import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_param>")
        sys.exit(1)
    
    script_name = sys.argv[0]
    central_api_token = sys.argv[1]
    serial_num = sys.argv[2]
    device_type = sys.argv[3]

    print(f"Script Name: {script_name}")
    print(f"Central API Token: {central_api_token}")
    print(f"Serial Number: {central_api_token}")
    print(f"Device Type: {central_api_token}")
    

if __name__ == "__main__":
    main()
