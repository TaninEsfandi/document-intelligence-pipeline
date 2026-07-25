from pydantic import BaseModel

class ReportOutput(BaseModel):
    report_number: str
    date_received: str
    device_name: str
    event_type: str
    text: str
