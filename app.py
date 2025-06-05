import streamlit as st
import openai
import os

# Load your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Log Analyzer with LLM", layout="wide")
st.title("🔍 Log File Analyzer using OpenAI GPT")

uploaded_file = st.file_uploader("📁 Upload your log file", type=["log", "txt"])

if uploaded_file is not None:
    log_content = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Preview of Uploaded Log:")
    st.code(log_content[:1000])  # show preview

    if st.button("🧠 Analyze Logs"):
        with st.spinner("Analyzing using LLM..."):
            prompt = f"""
You are a cybersecurity analyst AI. Analyze the following log data and summarize any anomalies, suspicious activities, or patterns:

{log_content}

Your response should include:
1. A general summary.
2. Any signs of DoS attacks or suspicious IP addresses.
3. Any patterns that might need deeper investigation.
4. Suggested next steps for the analyst.
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant skilled in log analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000
                )
                analysis = response["choices"][0]["message"]["content"]
                st.subheader("✅ Analysis Result")
                st.text_area("LLM Output", analysis, height=300)

            except Exception as e:
                st.error(f"Error: {e}")
