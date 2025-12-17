import requests, json

url = "https://helpdesk.estrategias.co:9010/api/v3/technicians/me"

headers = {
    "TECHNICIAN_KEY": "0A6475A1-D3A4-4B74-B608-01D75A14B307",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, verify=False)

print(response.status_code)
print(response.text)
