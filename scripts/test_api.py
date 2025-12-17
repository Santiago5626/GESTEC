import requests
import json

url = "https://helpdesk.estrategias.co:9010/api/v3/tasks"

payload = {
    "list_info": {
        "row_count": 25,
        "start_index": 1,
        "get_total_count": True
    },
    "search_fields": {
        "owner.id": "333630"
    },
    "fields_required": [
        "id",
        "title",
        "status",
        "priority",
        "group",
        "owner",
        "scheduled_start_time"
    ]
}

headers = {
    "TECHNICIAN_KEY": "0A6475A1-D3A4-4B74-B608-01D75A14B307",
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    data=json.dumps({"input_data": payload}),
    headers=headers,
    verify=False
)

print("Status:", response.status_code)
print("Response:", response.text)
