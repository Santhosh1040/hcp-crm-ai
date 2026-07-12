from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    interaction: Dict[str, Any] = Field(default_factory=dict)
    interaction_id: Optional[int] = None