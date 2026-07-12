from typing import List, Optional
import json

from langchain_core.tools import tool

from app.llm import get_llm


@tool
def log_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[List[str]] = None,
    samples_distributed: Optional[List[str]] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[List[str]] = None,
):
    """
    Log a new interaction with a Healthcare Professional (HCP).

    Use this tool when the user describes a new meeting, call, email,
    or other interaction with an HCP.
    """

    interaction = {
        "hcp_name": hcp_name or "",
        "interaction_type": interaction_type or "Meeting",
        "interaction_date": interaction_date or "",
        "interaction_time": interaction_time or "",
        "attendees": attendees or [],
        "topics_discussed": topics_discussed or "",
        "materials_shared": materials_shared or [],
        "samples_distributed": samples_distributed or [],
        "sentiment": sentiment,
        "outcomes": outcomes or "",
        "follow_up_actions": follow_up_actions or [],
        "ai_suggested_follow_ups": [],
    }

    return {
        "success": True,
        "action": "log_interaction",
        "message": "Interaction logged successfully.",
        "interaction": interaction,
    }


@tool
def edit_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[List[str]] = None,
    samples_distributed: Optional[List[str]] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[List[str]] = None,
):
    """
    Edit specific fields of the current HCP interaction.

    Use this tool when the user corrects or changes previously logged
    information. Only include fields that the user explicitly wants changed.
    """

    updates = {}

    values = {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "interaction_date": interaction_date,
        "interaction_time": interaction_time,
        "attendees": attendees,
        "topics_discussed": topics_discussed,
        "materials_shared": materials_shared,
        "samples_distributed": samples_distributed,
        "sentiment": sentiment,
        "outcomes": outcomes,
        "follow_up_actions": follow_up_actions,
    }

    for field, value in values.items():
        if value is not None:
            updates[field] = value

    return {
        "success": True,
        "action": "edit_interaction",
        "message": "Interaction updated successfully.",
        "updates": updates,
    }


@tool
def add_materials_samples(
    materials_shared: Optional[str] = None,
    samples_distributed: Optional[str] = None,
):
    """
    Add one material and/or one product sample to the current HCP interaction.

    Use this tool when the user says that an additional brochure, PDF,
    clinical document, educational material, or product sample was shared
    or distributed.

    Pass materials_shared as a single string.
    Pass samples_distributed as a single string.
    """

    return {
        "success": True,
        "action": "add_materials_samples",
        "message": "Materials and samples added successfully.",
        "materials_shared": [materials_shared] if materials_shared else [],
        "samples_distributed": [samples_distributed] if samples_distributed else [],
    }

@tool
def suggest_followups(
    hcp_name: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
):
    """
    Generate AI-suggested follow-up actions based on the current HCP interaction.

    Use this tool when the user asks what to do next, asks for recommendations,
    or requests suggested follow-up actions.
    """

    llm = get_llm()

    prompt = f"""
You are assisting a pharmaceutical field representative.

Generate exactly 3 specific, practical, and context-aware follow-up actions
based only on the HCP interaction information provided below.

HCP Name: {hcp_name or "Not provided"}
Topics Discussed: {topics_discussed or "Not provided"}
Sentiment: {sentiment or "Not provided"}
Outcomes: {outcomes or "Not provided"}

Requirements:
- Each suggestion must be directly relevant to this specific interaction.
- Use the HCP name when it is available and natural to do so.
- Refer to specific products, topics, requests, concerns, or outcomes when available.
- Consider the HCP sentiment when deciding the appropriate next step.
- Do not invent product names, clinical claims, requests, dates, or interaction details.
- Avoid generic suggestions that could apply to any HCP interaction.
- Make the 3 suggestions meaningfully different from one another.
- Keep each suggestion concise and actionable.

Return ONLY a valid JSON array containing exactly 3 strings.

Do not include markdown.
Do not include explanations.
"""

    response = llm.invoke(prompt)

    # Clean possible Markdown code fences returned by the LLM
    content = response.content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    try:
        suggestions = json.loads(content)

        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]

        suggestions = [
            str(suggestion).strip()
            for suggestion in suggestions
            if str(suggestion).strip()
        ]

        suggestions = suggestions[:3]

    except json.JSONDecodeError:
        suggestions = [content]

    return {
        "success": True,
        "action": "suggest_followups",
        "message": "Follow-up suggestions generated successfully.",
        "suggestions": suggestions,
    }

@tool
def summarize_voice_note(
    transcript: str,
):
    """
    Summarize a transcribed HCP interaction voice note.

    Use this tool when the user provides a voice-note transcript,
    meeting transcript, or long interaction note and asks for it
    to be summarized.

    Extract:
    - topics_discussed: a concise summary of the main discussion topics
    - outcomes: a concise summary of decisions, requests, agreements,
      concerns, or important results from the interaction
    """

    llm = get_llm()

    prompt = f"""
You are assisting a pharmaceutical field representative.

Summarize the following HCP interaction voice-note transcript.

VOICE NOTE TRANSCRIPT:
{transcript}

Extract exactly these two fields:

1. topics_discussed
   A concise summary of the main topics discussed.

2. outcomes
   A concise summary of important decisions, requests, agreements,
   concerns, or results from the interaction.

Return ONLY a valid JSON object in exactly this format:

{{
  "topics_discussed": "concise summary here",
  "outcomes": "concise outcome summary here"
}}

Do not include markdown.
Do not include explanations.
"""

    response = llm.invoke(prompt)

    # Clean possible Markdown code fences returned by the LLM
    content = response.content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    try:
        summary = json.loads(content)

    except json.JSONDecodeError:
        return {
            "success": False,
            "action": "summarize_voice_note",
            "message": "Could not parse the voice-note summary.",
            "topics_discussed": "",
            "outcomes": "",
        }

    return {
        "success": True,
        "action": "summarize_voice_note",
        "message": "Voice note summarized successfully.",
        "topics_discussed": summary.get(
            "topics_discussed",
            ""
        ),
        "outcomes": summary.get(
            "outcomes",
            ""
        ),
    }


ALL_TOOLS = [
    log_interaction,
    edit_interaction,
    add_materials_samples,
    suggest_followups,
    summarize_voice_note,
]