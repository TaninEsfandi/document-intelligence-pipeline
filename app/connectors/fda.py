import requests
import json

# Define the base URL
api_url = "https://api.fda.gov/device/event.json"

# Pass the dictionary to the params arguments
def fetch_reports(device_name, limit = 10):
    query_params = {
        "search": f"device.generic_name:{device_name}",
        "limit": limit
    }
    responds = requests.get(api_url, params = query_params)
    if responds.status_code == 200:
        data = responds.json()
        with open ("results/extracted_reports.json", "w") as file:
            json.dump(data, file, indent=4)
            return data
    else:
        print(responds.status_code, responds.text)
        return None

if __name__ == "__main__":
    fetch_reports("pacemaker")
