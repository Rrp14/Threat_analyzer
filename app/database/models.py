from datetime import datetime, timezone

from sqlalchemy import DateTime,String,Text
from sqlalchemy.orm import Mapped,mapped_column

from app.database.db import Base

class Analysis(Base):
    __tablename__="analysis"

    id:Mapped[int]=mapped_column(primary_key=True)

    analysis_id:Mapped[str]=mapped_column(
        String(30),
        unique=True,
        index=True,
    )

    timestamp:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    input_type:Mapped[str] =mapped_column(
        String(20)
    )

    raw_input:Mapped[str]=mapped_column(
        Text
    )

    result_json:Mapped[str]=mapped_column(
        Text
    )


