# AI-First CRM HCP Interaction Logger

A full-stack CRM application for logging Healthcare Professional (HCP) interactions through an AI assistant.

Instead of manually filling out the interaction form, users describe an HCP interaction in natural language through the chat interface. The AI assistant interprets the message, selects the appropriate tool, and updates the structured interaction form automatically.

The application supports creating and editing interactions, adding materials and samples, generating follow-up suggestions, and summarizing voice-note transcripts.

## Live Application

Frontend: [Add your Vercel deployment URL here]

Backend API: [Add your Railway deployment URL here]

## Features

- Log HCP interactions using natural language
- Automatically populate structured interaction details
- Edit previously logged interaction information through chat
- Add shared materials and distributed samples
- Infer and record HCP sentiment
- Generate AI-suggested follow-up actions
- Summarize voice-note transcripts into discussion topics and outcomes
- Persist interaction data in PostgreSQL
- Restore the latest interaction after a page refresh
- AI-controlled, read-only interaction form

## How It Works

The application follows an AI-first interaction model.

The user communicates with the AI assistant through the chat panel. The backend processes the request using a LangGraph-based agent and determines which tool should be executed.

The available tools are:

1. `log_interaction`  
   Creates and stores a new HCP interaction.

2. `edit_interaction`  
   Updates specific fields of the current interaction.

3. `add_materials_samples`  
   Adds shared materials or distributed product samples.

4. `suggest_followups`  
   Generates context-aware follow-up suggestions based on the interaction.

5. `summarize_voice_note`  
   Summarizes a voice-note transcript into discussion topics and outcomes.

After a tool is executed, the updated interaction is persisted in the database and returned to the frontend. Redux updates the application state, which automatically reflects the changes in the interaction form.

## Tech Stack

### Frontend

- React
- Vite
- Redux Toolkit
- Axios
- CSS

### Backend

- Python
- FastAPI
- LangChain
- LangGraph
- Groq LLM API
- SQLAlchemy
- PostgreSQL

### Deployment

- Vercel for the frontend
- Railway for the backend
- Neon PostgreSQL for the database

## Project Structure

```text
hcp-crm-ai/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── database.py
│   │   ├── llm.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── store/
│   │   ├── styles/
│   │   └── App.jsx
│   │
│   └── package.json
│
├── .gitignore
└── README.md
