import json

input_file_path = 'results/extracted_reports.json'   
output_file_path = 'results/transformed_reports.json'   

def transform_reports(input_file_path, output_file_path):
     with open (input_file_path,"r") as infile:
        data = json.load(infile)
        extracted_list = []
        description = ''
        for report in data.get("results", []):
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
            with open (output_file_path,"w") as outfile:
                json.dump(extracted_list, outfile, indent = 4)

if __name__ == "__main__":
    transform_reports(input_file_path, output_file_path)



