import streamlit as st
import openai
import os

# Title and description
st.title("🔍 Log File Analyzer using OpenAI GPT")
st.write("Upload your log file (e.g., .log or .txt) and let GPT analyze it.")

# File uploader
uploaded_file = st.file_uploader("Upload your log file", type=["log", "txt"])

# Process file
if uploaded_file is not None:
    log_content = uploaded_file.read().decode("utf-8")

    with st.spinner("Analyzing log file with GPT..."):
        # Ensure API key is in environment variable
        # export OPENAI_API_KEY="your_key_here" . # This command should add in terminal to set API Key in your environment
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            st.error("❌ OpenAI API key not found. Please set it as an environment variable.")
        else:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert in log file analysis. "
                                "You will receive raw log content and must extract key insights, security warnings, anomalies, and suggestions. "
                                "Format your response clearly using markdown with sections: Summary, Issues Found, Recommendations."
                            ),
                        },
                        {
                            "role": "user",
                            "content": f"Here is the log file content:\n\n{log_content[:4000]}"
                        }
                    ],
                    temperature=0.3
                )

                result = response.choices[0].message.content
                st.markdown("### ✅ Analysis Result")
                st.markdown(result)

                # Optional: Save to file
                with open("output_analysis.md", "w") as f:
                    f.write(result)

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")
