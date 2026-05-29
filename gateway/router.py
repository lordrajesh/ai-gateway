from groq import Groq
from models import MODELS, FALLBACK_MODEL
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_task(prompt: str) -> str:
    """
    Use a small LLM to classify what type of task the prompt is.
    In production this could be a fine-tuned classifier or rule-based system.
    Returns: 'summarization', 'coding', or 'general'
    """
    classification_prompt = f"""Classify the following user prompt into exactly one of these categories:
- summarization (summarizing, condensing, tldr, key points)
- coding (writing code, debugging, programming, scripts)
- general (everything else)

Respond with just the category name, nothing else.

User prompt: {prompt}

Category:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # cheapest model for classification
        messages=[{"role": "user", "content": classification_prompt}],
        max_tokens=10,  # we only need one word back
    )

    task_type = response.choices[0].message.content.strip().lower()

    # Validate — if LLM returns something unexpected, fall back to general
    if task_type not in MODELS:
        print(f"Unknown task type '{task_type}', falling back to general")
        task_type = "general"

    print(f"Classified as: {task_type}")
    return task_type


def route_and_execute(prompt: str) -> dict:
    """
    Main routing function:
    1. Classify the task
    2. Pick the right model
    3. Execute the prompt
    4. Return response with metadata
    """
    import time

    # Step 1: Classify
    task_type = classify_task(prompt)

    # Step 2: Pick model
    model_config = MODELS[task_type]
    model_name = model_config["model"]

    print(f"Routing to model: {model_name}")

    # Step 3: Execute
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=model_config["max_tokens"],
        )
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        success = True

    except Exception as e:
        # Fallback if model fails
        print(f"Model {model_name} failed: {e}. Falling back...")
        response = client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        model_name = FALLBACK_MODEL
        success = True

    latency = round(time.time() - start_time, 2)

    return {
        "answer": answer,
        "task_type": task_type,
        "model_used": model_name,
        "tokens_used": tokens_used,
        "latency_seconds": latency,
        "success": success
    }