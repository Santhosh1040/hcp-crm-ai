from typing import Annotated, Any, Dict, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from typing import Annotated, Any, Dict, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    interaction: Dict[str, Any]

    active_tool: Optional[str]

    tool_result: Optional[Dict[str, Any]]


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    interaction: Dict[str, Any]

    active_tool: Optional[str]

    tool_result: Optional[Dict[str, Any]]