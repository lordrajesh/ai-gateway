from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(__file__))

from router import route_and_execute
from logger import log_request, get_stats

app = FastAPI(title="AI API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "AI Gateway running"}

@app.post("/prompt")
async def handle_prompt(payload: dict):
    """
    Main gateway endpoint.
    Receives prompt, routes to right model, logs result.
    """
    prompt = payload.get("prompt", "")
    if not prompt:
        return {"error": "No prompt provided"}

    # Route and execute
    result = route_and_execute(prompt)

    # Log to Redis
    try:
        log_request(prompt, result)
    except Exception as e:
        print(f"Logging failed (Redis might be down): {e}")

    return result

@app.get("/stats")
async def get_gateway_stats():
    """
    Returns analytics from Redis.
    Called by Streamlit dashboard.
    """
    try:
        return get_stats()
    except Exception as e:
        return {"error": f"Could not fetch stats: {e}"}