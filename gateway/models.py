# This file defines which models are available and what they are good at
# In production this would come from a config database or AWS Parameter Store

MODELS = {
    "summarization": {
        "model": "llama-3.1-8b-instant",
        "description": "Fast and cheap - good for summarization",
        "max_tokens": 1024,
    },
    "coding": {
        "model": "mixtral-8x7b-32768",
        "description": "Mixtral - strong at code generation",
        "max_tokens": 2048,
    },
    "general": {
        "model": "llama-3.3-70b-versatile",
        "description": "Large model - good for complex reasoning",
        "max_tokens": 1024,
    }
}

# Fallback model if routing fails
FALLBACK_MODEL = "llama-3.3-70b-versatile"