import json
from datetime import date

from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.state import AgentState
from app.agent.tools import ALL_TOOLS
from app.llm import get_llm


# ---------------------------------------------------------
# LLM + TOOLS
# ---------------------------------------------------------

llm = get_llm()

# Give the Groq LLM access to all five tools
llm_with_tools = llm.bind_tools(ALL_TOOLS)

# LangGraph node responsible for executing the selected tool
tool_node = ToolNode(ALL_TOOLS)


# ---------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an AI assistant for a pharmaceutical CRM used by field representatives
to manage interactions with Healthcare Professionals (HCPs).

You have exactly five tools:

1. log_interaction
   Use when the user describes a NEW HCP interaction.

2. edit_interaction
   Use when the user corrects or changes information already present
   in the current interaction.

3. add_materials_samples
   Use when the user adds materials, brochures, PDFs, documents,
   or product samples to the current interaction.

4. suggest_followups
   Use when the user asks for recommended next steps or follow-up actions.
   Use the current interaction state as context when calling this tool.

5. summarize_voice_note
   Use when the user provides a transcript or long note and asks for it
   to be summarized.

Important rules:
- Use the appropriate tool for the user's request.
- Do not invent interaction details.
- For edits, include only the fields that should change.
- Preserve existing interaction information unless the user explicitly changes it.
- When suggesting follow-ups, use the current interaction information.
- Use YYYY-MM-DD for dates.
- Use HH:MM for times.
- Sentiment should be Positive, Neutral, or Negative.
"""


# ---------------------------------------------------------
# AGENT NODE
# ---------------------------------------------------------

def agent_node(state: AgentState):
    """
    The LLM reads the user's message and the current interaction state,
    then decides which of the five tools should be called.
    """

    current_interaction = state.get("interaction", {})

    context_message = SystemMessage(
        content=f"""
{SYSTEM_PROMPT}

Today's date is {date.today().isoformat()}.

Current interaction state:
{json.dumps(current_interaction, indent=2)}
"""
    )

    response = llm_with_tools.invoke(
        [context_message] + state["messages"]
    )

    return {
        "messages": [response]
    }


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

def should_use_tool(state: AgentState):
    """
    If the LLM generated a tool call, route execution to ToolNode.
    Otherwise, end the workflow.
    """

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


# ---------------------------------------------------------
# PROCESS TOOL RESULT
# ---------------------------------------------------------

def process_tool_result(state: AgentState):
    """
    Read the result returned by the executed tool and update the
    shared HCP interaction state according to which tool was used.
    """

    # Copy the current interaction so existing fields are preserved
    interaction = dict(state.get("interaction", {}))

    active_tool = None
    result = {}

    # Find the most recent ToolMessage produced by ToolNode
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage):
            active_tool = message.name

            try:
                result = json.loads(message.content)

            except json.JSONDecodeError:
                result = {
                    "success": False,
                    "message": message.content,
                }

            break

    # -----------------------------------------------------
    # TOOL 1: LOG INTERACTION
    # Replace the current interaction with the newly logged one
    # -----------------------------------------------------

    if active_tool == "log_interaction":
        interaction = result.get(
            "interaction",
            interaction
        )

    # -----------------------------------------------------
    # TOOL 2: EDIT INTERACTION
    # Update only the fields returned by the edit tool
    # -----------------------------------------------------

    elif active_tool == "edit_interaction":
        updates = result.get(
            "updates",
            {}
        )

        interaction.update(updates)

    # -----------------------------------------------------
    # TOOL 3: ADD MATERIALS / SAMPLES
    # Append new values without deleting existing values
    # -----------------------------------------------------

    elif active_tool == "add_materials_samples":
        existing_materials = interaction.get(
            "materials_shared",
            []
        )

        new_materials = result.get(
            "materials_shared",
            []
        )

        existing_samples = interaction.get(
            "samples_distributed",
            []
        )

        new_samples = result.get(
            "samples_distributed",
            []
        )

        interaction["materials_shared"] = (
            existing_materials + new_materials
        )

        interaction["samples_distributed"] = (
            existing_samples + new_samples
        )

    # -----------------------------------------------------
    # TOOL 4: SUGGEST FOLLOW-UPS
    # Store the AI-generated suggestions in the form state
    # -----------------------------------------------------

    elif active_tool == "suggest_followups":
        interaction["ai_suggested_follow_ups"] = result.get(
            "suggestions",
            []
        )

    # -----------------------------------------------------
    # TOOL 5: SUMMARIZE VOICE NOTE
    # We will implement the actual state update next
    # -----------------------------------------------------

    elif active_tool == "summarize_voice_note":

      if result.get("success"):
        interaction["topics_discussed"] = result.get(
            "topics_discussed",
            interaction.get("topics_discussed", "")
        )

        interaction["outcomes"] = result.get(
            "outcomes",
            interaction.get("outcomes", "")
        )

    # -----------------------------------------------------
    # RETURN UPDATED LANGGRAPH STATE
    # -----------------------------------------------------

    return {
        "interaction": interaction,
        "active_tool": active_tool,
        "tool_result": result,
    }


# ---------------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# ---------------------------------------------------------

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node(
    "agent",
    agent_node
)

workflow.add_node(
    "tools",
    tool_node
)

workflow.add_node(
    "process_tool_result",
    process_tool_result
)


# START → AGENT
workflow.add_edge(
    START,
    "agent"
)


# AGENT → TOOLS or END
workflow.add_conditional_edges(
    "agent",
    should_use_tool,
    {
        "tools": "tools",
        END: END,
    },
)


# TOOLS → PROCESS RESULT
workflow.add_edge(
    "tools",
    "process_tool_result"
)


# PROCESS RESULT → END
workflow.add_edge(
    "process_tool_result",
    END
)


# Compile the LangGraph workflow
graph = workflow.compile()