# Multi-Model AI API Gateway 🤖

A production-inspired AI gateway that automatically routes prompts to the best LLM based on task type.

## How It Works

Every prompt is classified first, then routed to the most suitable model:

| Task Type | Model | Why |
|---|---|---|
| Summarization | llama-3.1-8b-instant | Fast and cheap |
| Coding | mixtral-8x7b-32768 | Strong at code |
| General | llama-3.3-70b-versatile | Best reasoning |

## Architecture

    ai-gateway/
    ├── gateway/
    │   ├── main.py       # FastAPI gateway + endpoints
    │   ├── router.py     # Task classification + model routing
    │   ├── models.py     # Model definitions and config
    │   └── logger.py     # Redis request logging
    ├── dashboard/
    │   └── app.py        # Streamlit analytics dashboard
    ├── docker-compose.yml # Redis container
    └── requirements.txt

## Key Concepts Demonstrated
- **Model routing** — right model for right task
- **Observability** — every request logged to Redis
- **Fallback handling** — if model fails, gateway recovers
- **Cost optimization** — cheap models for simple tasks
- **Gateway pattern** — single entry point for all AI calls

## Production Equivalent
| Free (This Project) | Production |
|---|---|
| FastAPI | AWS API Gateway + Lambda |
| Groq multi-model | AWS Bedrock / Azure OpenAI |
| Redis (Docker) | AWS ElastiCache / Azure Cache |
| Streamlit | Grafana / Azure Monitor |

## Run Locally

### Prerequisites
- Python 3.10+
- Docker Desktop
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Setup
```bash
git clone https://github.com/YOUR_USERNAME/ai-gateway.git
cd ai-gateway
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Configure

GROQ_API_KEY=your_groq_api_key_here

### Start
```bash
docker-compose up -d        # Start Redis
cd gateway && uvicorn main:app --reload    # Terminal 1
cd dashboard && streamlit run app.py      # Terminal 2
```
