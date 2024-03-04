from datetime import datetime
from sqlalchemy import Date
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped, mapped_column


class Utils:
    class CommonDateOrm:
        created_at: Mapped[datetime] = mapped_column(Date, server_default=func.now())
        updated_at: Mapped[datetime] = mapped_column(
            Date, server_default=func.now(), onupdate=func.now()
        )
