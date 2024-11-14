import json
import requests


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
 
