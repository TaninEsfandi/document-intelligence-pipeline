import requests
import json
import os
from app.config import FDA_API_URL

# Pass the dictionary to the params arguments
def fetch_reports(device_name, limit = 10):
    query_params = {
        "search": f"device.generic_name:{device_name}",
        "limit": limit
    }
    responds = requests.get(FDA_API_URL, params = query_params)
    if responds.status_code == 200:
        data = responds.json()
        os.makedirs("results", exist_ok=True)
        with open ("results/extracted_reports.json", "w") as file:
            json.dump(data, file, indent=4)
            return data
    else:
        print(responds.status_code, responds.text)
        return None

if __name__ == "__main__":
    fetch_reports("pacemaker")
