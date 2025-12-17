import requests
import json
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

URL = "https://helpdesk.estrategias.co:9010/api/v3/requests/5939449"
TOKEN = "0A6475A1-D3A4-4B74-B608-01D75A14B307"

headers = {
    "TECHNICIAN_KEY": TOKEN,
    "Content-Type": "application/json"
}

try:
    response = requests.get(
        URL,
        headers=headers,
        timeout=30,
        verify=False
    )
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))
except Exception as e:
    print(f"Error: {e}")
    if 'response' in locals():
         print(response.text)
