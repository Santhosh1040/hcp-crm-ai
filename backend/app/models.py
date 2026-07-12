from sqlalchemy import Column, Date, Integer, String, Text, Time
from sqlalchemy.dialects.postgresql import JSON

from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    hcp_name = Column(
        String(255),
        nullable=True,
    )

    interaction_type = Column(
        String(100),
        nullable=True,
        default="Meeting",
    )

    interaction_date = Column(
        Date,
        nullable=True,
    )

    interaction_time = Column(
        Time,
        nullable=True,
    )

    attendees = Column(
        JSON,
        nullable=False,
        default=list,
    )

    topics_discussed = Column(
        Text,
        nullable=True,
    )

    materials_shared = Column(
        JSON,
        nullable=False,
        default=list,
    )

    samples_distributed = Column(
        JSON,
        nullable=False,
        default=list,
    )

    sentiment = Column(
        String(20),
        nullable=True,
    )

    outcomes = Column(
        Text,
        nullable=True,
    )

    follow_up_actions = Column(
        JSON,
        nullable=False,
        default=list,
    )

    ai_suggested_follow_ups = Column(
        JSON,
        nullable=False,
        default=list,
    )