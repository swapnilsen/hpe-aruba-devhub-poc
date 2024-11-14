import argparse
import configparser
import json
import time
from urllib.parse import quote

import requests
from sqlalchemy import create_engine, text

config = configparser.ConfigParser()

config.read('config/settings.properties')


def load_config():
    # Load database configuration from the properties file
    config = configparser.ConfigParser()
    config.read('config/settings.properties')

    db_host = config.get('database', 'host')
    db_port = config.get('database', 'port')
    db_username = config.get('database', 'username')
    db_password = config.get('database', 'password')
    db_name = config.get('database', 'database_name')
    central_account = config.get('account', 'customer_id')

    return db_host, db_port, db_username, db_password, db_name, central_account


def connect_and_query():
    # Load database configurations
    db_host, db_port, db_username, db_password, db_name, central_account = load_config()

    # Create the SQLAlchemy engine for PostgreSQL
    connection_url = f"postgresql://{db_username}:%s@{db_host}:{db_port}/{db_name}" % quote(db_password)
    engine = create_engine(connection_url)
    query = text(
        "select * from si_central_details where central_custid = '" + central_account + "'")

    try:
        with engine.connect() as connection:
            print("Connection to PostgreSQL successful")

            query = text(
                "select * from si_central_details where central_custid = '" + central_account + "'")
            result = connection.execute(query)

            # Fetch and display results
            for row in result:
                print(row)

        return result

    except Exception as e:
        print("Error connecting to PostgreSQL:", e)


def connect_central_devices():
    try:
        db_obj = connect_and_query()
        token_file = getattr(db_obj[0], 'token_file')
        validation_status = getattr(db_obj[0], 'validation_status')
        if validation_status in 'Valid':
            token_file = json.loads(token_file)
            access_token = token_file["access_token"]
            return access_token
        else:
            raise Exception("Invalid Token from DB")
    except Exception as e:
        raise Exception("Unable to fetch value from DB", e)


def get_access_token(retries=3, delay=5):
    for attempt in range(retries):
        try:
            access_token = connect_central_devices()
            return access_token
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retry attempts failed.")
                raise Exception("Unable to fetch access token after multiple attempts.") from e


def call_api_with_token():
    try:
        config = configparser.ConfigParser()
        config.read('config/settings.properties')
        serial_number = config.get('account', 'serial_number')
        base_url = config.get('account', 'base_url')
        serial_number = serial_number.split(",")
        access_token = get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        api_responses = {}

        for serial in serial_number:
            url = f"{base_url}{serial.strip()}"

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()  # Parse JSON response
                api_responses.update({serial: data["status"]})
            else:
                print(
                    f"API request failed for serial {serial} with status code {response.status_code}: {response.text}")
                api_responses.update({serial: "No Response"})
        return api_responses
    except Exception as e:
        print(f"Error in API call: {e}")
        return None


def call_api_with_token_args(access_token, serial_numbers, base_url):
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        api_responses = {}

        base_url = f"https://{base_url}/monitoring/v1/switches/"

        for serial in serial_numbers:
            url = f"{base_url}{serial.strip()}"

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()  # Parse JSON response
                api_responses.update({serial: data["status"]})
            else:
                print(
                    f"API request failed for serial {serial} with status code {response.status_code}: {response.text}")
                api_responses.update({serial: "No Response"})
        return api_responses
    except Exception as e:
        print(f"Error in API call: {e}")
        return None


if __name__ == '__main__':
    script_name = sys.argv[0]
    base_url = sys.argv[1]
    api_token = sys.argv[2]
    serial_number_str = sys.argv[3]
    serial_numbers = serial_number_str.split(",")
    device_type = sys.argv[4]

    print(f"Script Name: {script_name}")
    print(f"Central Base URL: {base_url}")
    print(f"Central API Token: {api_token}")
    print(f"Serial Numbers: {serial_numbers}")
    print(f"Device Type: {device_type}")

    device_status = call_api_with_token_args(api_token, serial_numbers, base_url)
    email_recipients = "swapnil.sen@hpe.com,sumit.paul@hpe.com"

    html_table = """
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Serial Number</th>
                <th>Status</th>
            </tr>
        """

    # Add rows for each URL and status
    for serial, status in device_status.items():
        html_table += f"""
            <tr>
                <td>{serial}</td>
                <td>{status}</td>
            </tr>
            """

    # Close the table
    html_table += "</table>"

    email_url = "https://si-central-site-hc.arubaserviceinsights.com/send-email"

    json_data = {
        "subject": f"Dev Hub QA Central Device Status",
        "body": html_table,
        "receivers": email_recipients.split(",")
    }

    data = {'data': json.dumps(json_data)}

    response = requests.post(email_url, data=data)

    print(response.text)
 
