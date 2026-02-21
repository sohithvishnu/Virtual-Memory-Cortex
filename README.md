# Virtual-Memory-Cortex
Its a biological memory hierarchy (Hot/warm/cold) and a reactive loop to proactively manage the user's life.

---

## 1. System Requirements

* **Active State MCP (Hot Memory):** The system must maintain a highly compressed, constantly updated JSON state of the user’s immediate context (e.g., current mood, today's goals). This is injected into every base prompt to eliminate redundant database queries.
* **Vectorized Episodic Memory (Warm Memory):** The system must support sub-100ms semantic search over recent conversation history to provide seamless conversational continuity.
* **Federated Data Stores (Cold Memory):** Distinct, strictly typed database collections for specific "Apps" (e.g., Calendar, Persona, Mood), accessed only via explicit AI tool calling.
* **Subconscious Consolidation (The Dream Loop):** An asynchronous background worker that runs periodically to extract permanent facts from Warm Memory, write them to Cold Memory, and re-compress the Hot Memory state for the next session.
* **Multi-Agent Routing:** A lightweight Supervisor AI that evaluates initial user input and routes execution to specialized Expert Agents (e.g., Calendar Agent, Memory Agent) to prevent context bloat and hallucination.
* **Offline-Capable Path:** The architecture must decouple the LLM layer so the cloud-based model (Mac mini) can eventually be seamlessly swapped for an on-device SLM (Small Language Model) on iOS.

---

## 2. Tech Stack

### The Frontend (iOS Client)
* **Language & UI:** Swift & SwiftUI.
* **Local State:** Native JSON storage engine (architected to migrate to Couchbase Lite/MongoDB Realm for true offline sync).
* **Design System:** Apple Native (ultra-thin materials, Liquid Glass UI).

### The Backend (Mac Mini / Server)
* **Orchestration:** Python + FastAPI (Async execution, automatic OpenAPI documentation).
* **Background Workers:** Celery + Redis (or FastAPI `BackgroundTasks` for V1) to power the "Subconscious" consolidation loop and trigger Apple Push Notifications.
* **Agent Framework:** LangGraph or Letta (formerly MemGPT) for stateful, cyclical graph execution and tool routing.

### The Database (The Memory Engine)
* **Primary Database:** MongoDB (via Motor Async). Document-based NoSQL is mandatory for the dynamic JSON structures of the federated "Apps."
* **Vector Search:** MongoDB Atlas Vector Search (or local pgvector) for semantic querying of the "Warm" episodic memory layer.

### The AI / LLM Layer
* **Local Execution:** Ollama.
* **Models:** Llama 3.2 (or Qwen) for complex reasoning and extraction tasks, paired with a highly quantized, fast model dedicated strictly to Supervisor routing.

---

## 3. Development Roadmap

### Stage 1: The Foundation (CRUD & Comms)
**Goal:** Establish the bulletproof pipeline between the iOS client, the FastAPI server, and MongoDB.
* Stand up FastAPI and configure the async MongoDB connection (`motor`).
* Create the `app_messages` collection to act as the raw UI transcript.
* Build the iOS UI with Liquid Glass styling and pure JSON data fetching.
* **Milestone:** End-to-end communication where the user texts the server, it saves to Mongo, Ollama replies, and the iOS UI updates asynchronously.

### Stage 2: The Multi-Agent Router (The CPU)
**Goal:** Implement the Supervisor/Worker architecture to handle complex tool calling.
* Define strict Pydantic schemas for the federated "Apps" (`app_calendar`, `app_persona`).
* Integrate LangGraph to construct the Supervisor router.
* Write pure Python functions (Tools) for MongoDB read/write operations and bind them to specific Expert Agents.
* **Milestone:** The user issues a complex command ("Reschedule my meeting"), and the Supervisor accurately routes it to the Calendar Agent without hallucinating changes to the Persona database.

### Stage 3: The Biological Memory (Hot/Warm/Cold)
**Goal:** Embed contextual awareness without exploding the token limit.
* Implement Vector Embeddings for the `app_messages` collection (Warm Memory).
* Create the highly compressed `current_state` document in MongoDB (Hot Memory).
* Update the FastAPI endpoint to silently retrieve and inject the Hot Memory into the System Prompt before passing the message to the Supervisor.
* **Milestone:** The AI accurately infers the user's current mood and priorities before the user finishes their sentence, eliminating the need for brute-force database searches on every message.

### Stage 4: The Subconscious Loop & Proactivity
**Goal:** Enable autonomous learning and proactive task initiation.
* Deploy the background worker engine.
* Engineer the extraction prompt: *"Review today's logs. Update the user's Persona, and rewrite tomorrow's Hot Memory state."*
* Implement Apple Push Notifications (APN) triggered by the background worker.
* **Milestone:** The system operates autonomously—identifying an early morning meeting, noting the user's logged exhaustion, and pushing a notification suggesting a schedule change without user prompting.
