import redis
import json
import time

# Connect to Redis - will run as Docker container
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def log_request(prompt: str, result: dict):
    """
    Log every AI request to Redis.
    In production this would go to CloudWatch, Azure Monitor, or Datadog.
    """
    log_entry = {
        "timestamp": time.time(),
        "prompt_preview": prompt[:100],  # first 100 chars only
        "task_type": result["task_type"],
        "model_used": result["model_used"],
        "tokens_used": result["tokens_used"],
        "latency_seconds": result["latency_seconds"],
        "success": result["success"]
    }

    # Push to a Redis list - acts as our log stream
    r.lpush("gateway:logs", json.dumps(log_entry))

    # Keep only last 100 logs
    r.ltrim("gateway:logs", 0, 99)

    # Increment counters per model
    r.hincrby("gateway:model_counts", result["model_used"], 1)

    # Increment counters per task type
    r.hincrby("gateway:task_counts", result["task_type"], 1)

    print(f"Logged request: {log_entry}")


def get_stats() -> dict:
    """
    Retrieve analytics from Redis.
    Called by the dashboard.
    """
    logs_raw = r.lrange("gateway:logs", 0, -1)
    logs = [json.loads(log) for log in logs_raw]

    model_counts = r.hgetall("gateway:model_counts")
    task_counts = r.hgetall("gateway:task_counts")

    return {
        "total_requests": len(logs),
        "model_counts": model_counts,
        "task_counts": task_counts,
        "recent_logs": logs[:10]  # last 10 requests
    }