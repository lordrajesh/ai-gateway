import streamlit as st
import requests

GATEWAY_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Gateway Dashboard", page_icon="🤖")
st.title("🤖 AI API Gateway Dashboard")

# --- Section 1: Send a prompt ---
st.header("1. Test the Gateway")
prompt = st.text_area("Enter a prompt:", placeholder="Write a Python function to sort a list...")

if st.button("Send to Gateway"):
    with st.spinner("Routing to best model..."):
        response = requests.post(
            f"{GATEWAY_URL}/prompt",
            json={"prompt": prompt}
        )
        result = response.json()

    st.subheader("Response")
    st.write(result.get("answer"))

    col1, col2, col3 = st.columns(3)
    col1.metric("Task Type", result.get("task_type"))
    col2.metric("Model Used", result.get("model_used", "").split("-")[0])
    col3.metric("Latency", f"{result.get('latency_seconds')}s")

    st.caption(f"Tokens used: {result.get('tokens_used')} | Full model: {result.get('model_used')}")

# --- Section 2: Analytics ---
st.header("2. Gateway Analytics")

if st.button("Refresh Stats"):
    stats = requests.get(f"{GATEWAY_URL}/stats").json()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Requests by Model")
        st.bar_chart(stats.get("model_counts", {}))

    with col2:
        st.subheader("Requests by Task Type")
        st.bar_chart(stats.get("task_counts", {}))

    st.subheader("Recent Requests")
    for log in stats.get("recent_logs", []):
        st.markdown(f"**{log['task_type']}** → `{log['model_used']}` | {log['latency_seconds']}s | {log['tokens_used']} tokens")
        st.caption(f"Prompt: {log['prompt_preview']}")
        st.divider()