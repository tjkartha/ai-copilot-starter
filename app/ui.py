import streamlit as st
import sys
import os
import yaml

# Ensure imports work from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wrapper import CappedOllamaClient

st.title("AI Copilot - Baseline")

# Load externalized prompt
with open("prompts/v1_system.yaml", "r") as file:
    config = yaml.safe_load(file)
    system_prompt = config.get("system_prompt", "")

client = CappedOllamaClient(model_name="llama3")

user_input = st.text_input("Ask the copilot:")

if st.button("Send"):
    if user_input:
        with st.spinner("Processing..."):
            try:
                result = client.generate(user_input, system_prompt)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["text"])
                    st.caption(f"⏱️ Latency: {result['metrics']['latency_ms']:.2f}ms | 🪙 Tokens: {result['metrics']['simulated_prompt_tokens']} in / {result['metrics']['simulated_completion_tokens']} out")
            except Exception as e:
                st.error(str(e))
