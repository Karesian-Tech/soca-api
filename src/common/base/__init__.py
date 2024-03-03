from datetime import datetime


class CommonDate:
    created_at: datetime
    updated_at: datetime


class CommonField(CommonDate):
    created_by: str
    updated_by: str
