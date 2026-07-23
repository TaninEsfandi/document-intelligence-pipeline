import requests

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
        return responds.json()
    else:
        return None


print(fetch_reports("insulin pump", limit=3))