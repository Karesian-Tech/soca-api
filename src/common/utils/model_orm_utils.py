from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped, mapped_column


class Utils:
    class CommonDateOrm:
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
        updated_at: Mapped[datetime] = mapped_column(
            DateTime, default=datetime.now, onupdate=datetime.now
        )
