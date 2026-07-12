from datetime import date, time

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session

from app.agent.graph import graph
from app.database import (
    Base,
    engine,
    get_db,
    test_database_connection,
)
from app.llm import get_llm
from app.models.interaction import Interaction
from app.schemas.chat import ChatRequest
from app.schemas.interaction import InteractionData


# ---------------------------------------------------------
# CREATE DATABASE TABLES
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="AI-First CRM HCP API",
    description=(
        "Backend API for the AI-powered "
        "HCP interaction logging system"
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def parse_date(value):
    if not value:
        return None

    if isinstance(value, date):
        return value

    return date.fromisoformat(str(value))


def parse_time(value):
    if not value:
        return None

    if isinstance(value, time):
        return value

    return time.fromisoformat(str(value))


def interaction_to_dict(interaction: Interaction):
    return {
        "interaction_id": interaction.id,
        "hcp_name": interaction.hcp_name,
        "interaction_type": interaction.interaction_type,
        "interaction_date": (
            interaction.interaction_date.isoformat()
            if interaction.interaction_date
            else None
        ),
        "interaction_time": (
            interaction.interaction_time.strftime("%H:%M")
            if interaction.interaction_time
            else None
        ),
        "attendees": interaction.attendees or [],
        "topics_discussed": interaction.topics_discussed,
        "materials_shared": (
            interaction.materials_shared or []
        ),
        "samples_distributed": (
            interaction.samples_distributed or []
        ),
        "sentiment": interaction.sentiment,
        "outcomes": interaction.outcomes,
        "follow_up_actions": (
            interaction.follow_up_actions or []
        ),
        "ai_suggested_follow_ups": (
            interaction.ai_suggested_follow_ups or []
        ),
    }


def apply_interaction_data(
    db_interaction: Interaction,
    interaction_data: dict,
):
    db_interaction.hcp_name = interaction_data.get(
        "hcp_name"
    )

    db_interaction.interaction_type = (
        interaction_data.get("interaction_type")
        or "Meeting"
    )

    db_interaction.interaction_date = parse_date(
        interaction_data.get("interaction_date")
    )

    db_interaction.interaction_time = parse_time(
        interaction_data.get("interaction_time")
    )

    db_interaction.attendees = (
        interaction_data.get("attendees") or []
    )

    db_interaction.topics_discussed = (
        interaction_data.get("topics_discussed")
    )

    db_interaction.materials_shared = (
        interaction_data.get("materials_shared") or []
    )

    db_interaction.samples_distributed = (
        interaction_data.get("samples_distributed") or []
    )

    db_interaction.sentiment = interaction_data.get(
        "sentiment"
    )

    db_interaction.outcomes = interaction_data.get(
        "outcomes"
    )

    db_interaction.follow_up_actions = (
        interaction_data.get("follow_up_actions") or []
    )

    db_interaction.ai_suggested_follow_ups = (
        interaction_data.get(
            "ai_suggested_follow_ups"
        )
        or []
    )


# ---------------------------------------------------------
# BASIC ROUTES
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI-First CRM HCP API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/interactions/test")
def test_interaction(
    interaction: InteractionData,
):
    return {
        "message": (
            "Interaction data received successfully"
        ),
        "interaction": interaction,
    }


@app.get("/api/llm/test")
def test_llm():
    llm = get_llm()

    response = llm.invoke(
        "Reply with exactly: Groq connection successful"
    )

    return {
        "response": response.content
    }


# ---------------------------------------------------------
# GET SAVED INTERACTIONS
# Useful for proving persistence during the demo
# ---------------------------------------------------------

@app.get("/api/interactions")
def get_interactions(
    db: Session = Depends(get_db),
):
    interactions = (
        db.query(Interaction)
        .order_by(Interaction.id.desc())
        .all()
    )

    return [
        interaction_to_dict(interaction)
        for interaction in interactions
    ]


# IMPORTANT:
# This static /latest route must come BEFORE
# the dynamic /{interaction_id} route.
@app.get("/api/interactions/latest")
def get_latest_interaction(
    db: Session = Depends(get_db)
):
    interaction = (
        db.query(Interaction)
        .order_by(Interaction.id.desc())
        .first()
    )

    if not interaction:
        return {
            "interaction_id": None,
            "interaction": None,
        }

    return {
        "interaction_id": interaction.id,
        "interaction": {
            "hcp_name": interaction.hcp_name or "",
            "interaction_type": (
                interaction.interaction_type or "Meeting"
            ),
            "interaction_date": (
                interaction.interaction_date.isoformat()
                if interaction.interaction_date
                else ""
            ),
            "interaction_time": (
                interaction.interaction_time.strftime("%H:%M")
                if interaction.interaction_time
                else ""
            ),
            "attendees": interaction.attendees or [],
            "topics_discussed": (
                interaction.topics_discussed or ""
            ),
            "materials_shared": (
                interaction.materials_shared or []
            ),
            "samples_distributed": (
                interaction.samples_distributed or []
            ),
            "sentiment": interaction.sentiment,
            "outcomes": interaction.outcomes or "",
            "follow_up_actions": (
                interaction.follow_up_actions or []
            ),
            "ai_suggested_follow_ups": (
                interaction.ai_suggested_follow_ups or []
            ),
        },
    }


@app.get("/api/interactions/{interaction_id}")
def get_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
):
    interaction = (
        db.query(Interaction)
        .filter(Interaction.id == interaction_id)
        .first()
    )

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found",
        )

    return interaction_to_dict(interaction)


# ---------------------------------------------------------
# LANGGRAPH CHAT + DATABASE PERSISTENCE
# ---------------------------------------------------------

@app.post("/api/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    initial_state = {
        "messages": [
            HumanMessage(content=request.message)
        ],
        "interaction": request.interaction,
        "active_tool": None,
        "tool_result": None,
    }

    result = graph.invoke(initial_state)

    active_tool = result.get("active_tool")
    updated_interaction = result.get(
        "interaction",
        {},
    )
    tool_result = result.get(
        "tool_result",
        {},
    )

    interaction_id = request.interaction_id

    try:
        # -------------------------------------------------
        # LOG INTERACTION -> INSERT NEW DATABASE ROW
        # -------------------------------------------------

        if active_tool == "log_interaction":
            db_interaction = Interaction()

            apply_interaction_data(
                db_interaction,
                updated_interaction,
            )

            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)

            interaction_id = db_interaction.id

        # -------------------------------------------------
        # OTHER 4 TOOLS -> UPDATE EXISTING DATABASE ROW
        # -------------------------------------------------

        elif active_tool in {
            "edit_interaction",
            "add_materials_samples",
            "suggest_followups",
            "summarize_voice_note",
        }:
            if interaction_id is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No interaction_id found. "
                        "Log an interaction first."
                    ),
                )

            db_interaction = (
                db.query(Interaction)
                .filter(
                    Interaction.id == interaction_id
                )
                .first()
            )

            if db_interaction is None:
                raise HTTPException(
                    status_code=404,
                    detail="Interaction not found.",
                )

            apply_interaction_data(
                db_interaction,
                updated_interaction,
            )

            db.commit()
            db.refresh(db_interaction)

    except HTTPException:
        raise

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Database operation failed: "
                f"{str(error)}"
            ),
        )

    return {
        "message": tool_result.get(
            "message",
            "Request processed successfully.",
        ),
        "active_tool": active_tool,
        "interaction_id": interaction_id,
        "interaction": updated_interaction,
        "tool_result": tool_result,
    }


# ---------------------------------------------------------
# DATABASE CONNECTION TEST
# ---------------------------------------------------------

@app.get("/api/database/test")
def test_database():
    result = test_database_connection()

    return {
        "status": "connected",
        "database": "PostgreSQL",
        "result": result,
    }