# Vertex AI RAG + ADK Conversational Assistant

A production-ready conversational Retrieval-Augmented Generation (RAG) solution built with Google’s Agent Development Kit (ADK) and Vertex AI RAG / Search capabilities. This project has been customized for a client workflow that uses Google Drive as the knowledge base, ADC-only authentication, and a Google-hosted tester URL for end-user validation.

## Overview

This solution provides:
- A conversational user interface.
- RAG-based retrieval from Google Drive-backed knowledge sources.
- Vertex AI-powered reasoning and generation.
- ADC-only authentication.
- A modular workflow aligned with the technical architecture shown in the reference diagram [file:181].

The design follows a component-and-data-flow model:
1. User interacts with the chatbot UI.
2. The agent classifies the request.
3. The system decides whether to retrieve context or answer directly.
4. If retrieval is needed, the RAG pipeline fetches relevant context from connected sources.
5. The model generates a grounded response.
6. The answer is returned to the UI.

## Architecture

The workflow is organized into the following layers:

### 1. User Interface
The front end is a conversational chat interface that supports:
- user messages,
- assistant responses,
- quick actions,
- file/context display.

### 2. Agent Orchestration
ADK manages the interaction flow:
- intent understanding,
- retrieval decision,
- orchestration of tools,
- response generation,
- return of the final answer.

### 3. Retrieval Pipeline
When retrieval is needed, the pipeline performs:
- query transformation,
- retrieval from connected knowledge sources,
- filtering and ranking,
- chunking and context assembly,
- grounding of the response.

### 4. Knowledge Sources
The knowledge base is centered on:
- Google Drive documents,
- connected repository data,
- existing RAG corpus content.

### 5. Authentication
Authentication uses:
- Application Default Credentials (ADC) only,
- no API key,
- Google Cloud permissions already approved for the project.

## Business Goal

The customized solution is intended to:
- answer user questions conversationally,
- retrieve grounded answers from Drive-backed content,
- provide a tester-friendly hosted Google URL,
- keep the custom UI separate from the hosted test experience,
- preserve the client’s workflow and permissions constraints.

## Current Project Configuration

- **Google Cloud Project ID:** `corpbs-cdl-ai`
- **Google Cloud Location:** `us-central1`
- **RAG Corpus ID:** `projects/corpbs-cdl-ai/locations/us-central1/ragCorpora/bizguidegemini2-0-cdl-datastore-extensive_1748609021959`
- **Knowledge base:** Google Drive
- **Authentication:** ADC only
- **Model:** `gemini-3.1-flash-preview-001`
- **Embedding model:** `text-embedding-004`
- **Agent name:** `bizguide_rag_corpus_manager`

## Technical Workflow

The implementation follows this sequence:

1. **User asks a question** in the chat UI.
2. **Agent understands the request** and classifies it.
3. **Retrieval decision is made**:
   - if the request needs context, the retrieval flow runs,
   - if not, the agent can answer directly.
4. **RAG retrieval runs** against the connected Drive-backed corpus.
5. **Relevant chunks are assembled** into context.
6. **Gemini generates the response** using the retrieved context.
7. **Final answer is shown** in the UI.

## Repository Structure

```text
VertexAIRAGCDLADC/
  .venv/
  .env
  requirements.txt
  config.py
  ingest_rag.py
  ui/
    index.html
    styles.css
    app.js
```

## Local Development Setup

### 1. Create the virtual environment

```bash
cd /Users/ravikarra/Documents/VertexAIRAGCDLADC
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install google-adk google-cloud-aiplatform python-dotenv fastapi uvicorn[standard]
```

### 2. Configure ADC

```bash
gcloud auth application-default login
gcloud config set project corpbs-cdl-ai
```

If Drive access is needed in local code:

```bash
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive
```

### 3. Create the `.env` file

```env
GOOGLE_CLOUD_PROJECT=corpbs-cdl-ai
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS_ID=projects/corpbs-cdl-ai/locations/us-central1/ragCorpora/bizguidegemini2-0-cdl-datastore-extensive_1748609021959
GOOGLE_GENAI_USE_VERTEXAI=True
AGENT_MODEL=gemini-3.1-flash-preview-001
AGENT_NAME=bizguide_rag_corpus_manager
RAG_DEFAULT_EMBEDDING_MODEL=text-embedding-004
RAG_DEFAULT_TOP_K=10
RAG_DEFAULT_SEARCH_TOP_K=5
RAG_DEFAULT_VECTOR_DISTANCE_THRESHOLD=0.5
RAG_DEFAULT_PAGE_SIZE=50
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Console Setup

In Google Cloud Console:
1. Open the project `corpbs-cdl-ai`.
2. Open the Vertex AI Search / RAG app.
3. Confirm the corpus is connected to Google Drive.
4. Verify preview responses in the hosted Google experience.
5. Use the integration widget only if a custom UI shell is needed.
6. Share the hosted `vertexaisearch.cloud.google.com/...` URL with testers.

## Ingestion Script

Use the ingestion script to import Drive files into the corpus.

```python
import asyncio
import logging
import os
import vertexai
from vertexai import rag
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
CORPUS_ID = os.getenv("RAG_CORPUS_ID")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT")

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)

async def ingest_drive_files():
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    drive_paths = [
        "https://drive.google.com/file/d/YOUR_FILE_ID_1",
        "https://drive.google.com/file/d/YOUR_FILE_ID_2",
    ]

    response = await rag.import_files(
        corpus_name=CORPUS_ID,
        paths=drive_paths,
        max_embedding_requests_per_min=900,
    )
    result = await response.result()
    print(f"Imported {result.imported_rag_files_count} files.")

if __name__ == "__main__":
    asyncio.run(ingest_drive_files())
```

Run it with:

```bash
source .venv/bin/activate
python3 ingest_rag.py
```

## Custom UI

The `ui/index.html` file is used only for the custom front-end shell. It can mirror the reference diagram’s conversational flow and should support:
- user input,
- assistant messages,
- retrieval status,
- document/context cards,
- quick actions.

This UI is separate from the hosted Google tester URL.

## Tester Experience

End users should test the solution using the hosted Google URL, not a local file path. The hosted URL provides the production-like experience for validation while the custom UI remains available for branding or embedding.

## Implementation Notes

- No API key is used.
- ADC is the only authentication method.
- Google Drive is the knowledge base.
- The workflow is conversational and RAG-based.
- The architecture should align with the provided component/data-flow diagram [file:181].

## License

This project is customized for a client implementation and should preserve attribution and licensing requirements from any upstream source code that was reused.
