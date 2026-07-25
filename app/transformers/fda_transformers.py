import json
def transform_reports(data):
    extracted_list = []
    for report in data.get("results", []):
        description = ''
        for entry in report.get('mdr_text', []):
            if entry.get("text_type_code") == "Description of Event or Problem":
                description = entry["text"]
                break
            new_records= {
                "report_number": report.get("report_number"),
                "date_received" : report.get("date_received"),
                "device_name" : report.get("device")[0]["generic_name"],
                "event_type" : report.get("event_type"),
                "text" : description
                }
            
            extracted_list.append(new_records)
        return extracted_list
    
if __name__ == "__main__":
    with open("results/extracted_reports.json", "r") as f:
        data = json.load(f)
    result = transform_reports(data)         # data = loaded from file
    print(result)                            # file data gets passed in as data

