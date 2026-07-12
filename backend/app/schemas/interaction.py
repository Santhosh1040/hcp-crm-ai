from datetime import date, time
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class InteractionData(BaseModel):
    interaction_id: Optional[int] = None

    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = "Meeting"
    interaction_date: Optional[date] = None
    interaction_time: Optional[time] = None

    attendees: List[str] = Field(default_factory=list)
    topics_discussed: Optional[str] = None

    materials_shared: List[str] = Field(default_factory=list)
    samples_distributed: List[str] = Field(default_factory=list)

    sentiment: Optional[
        Literal["Positive", "Neutral", "Negative"]
    ] = None

    outcomes: Optional[str] = None

    follow_up_actions: List[str] = Field(
        default_factory=list
    )

    ai_suggested_follow_ups: List[str] = Field(
        default_factory=list
    )