import os
from dotenv import load_dotenv

load_dotenv()

import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse


# Import to schema kai ton agent
from api.schemas import ChatRequest
from core.graph import app as agent_app

app = FastAPI(title="Agentic Planner API", version="1.0.0")


# Rythmish CORS gia na mhn mplokarei o browser me thn React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Edo tha mpei to URL ths React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Δέχεται το μήνυμα του χρήστη και επιστρέφει streaming events (SSE) 
    για κάθε βήμα της εκτέλεσης (Plan -> Execution -> Final Response).
    """
    
    async def event_generator():
        initial_state = {
            "input": request.message,
            "plan": [],
            "current_step_index": 0,
            "final_response": ""
        }

        try:
            # To agent_app.stream() trexei komvo komvo kai leei thn katastash kathe se vhma
            for output in agent_app.stream(initial_state):
                
                for node_name, state_update in output.items():
                    
                    if node_name == "planner":
                        # Stelno to plano
                        yield {
                            "event": "plan_generated",
                            "data": json.dumps({"plan": state_update["plan"]}, ensure_ascii=False)
                        }
                        
                    elif node_name == "executor":
                        # Stelno to ananeomeno plano
                        yield {
                            "event": "step_executed",
                            "data": json.dumps({"plan": state_update["plan"]}, ensure_ascii=False)
                        }
                        
                    elif node_name == "finalizer":
                        # Stelno thn telikh apanthsh
                        yield {
                            "event": "final_response",
                            "data": json.dumps({"response": state_update["final_response"]}, ensure_ascii=False)
                        }
                
                # Mikro delay gia mellontika UI animations
                await asyncio.sleep(0.1)

        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"detail": str(e)}, ensure_ascii=False)
            }

    return EventSourceResponse(event_generator())

# Elegxo an o server einai zontanos
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Agentic Planner Backend is running!"}