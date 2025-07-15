import sys
from pathlib import Path
import streamlit as st
from src.process import parse_chat
from io import StringIO
from llm_engine.models.feedback_engine import get_feedback_from_chat

# Initialize
raw_data = None

# Taking User Inputs
with st.sidebar:
    st.title("Upload a Chat")
    st.write("Multi-file upload is not supported at the moment.")

    input_text = st.text_area("Paste your chat here...")

    submitted = st.button("Analyze")

    st.subheader("Or")

    text_file = st.file_uploader(
        label="Upload a file",
        type="txt",
        accept_multiple_files=False
    )

# Tabs
tab1, tab2, tab3 = st.tabs(["Home", "Raw", "Processed Data"])

# Tab 1: Home
with tab1:
    col1, col2 = st.columns(2, gap='small', border=True)

    # column 1
    with col1:
        if input_text.strip():
            cleaned_chat = parse_chat(input_text)
            feedback = get_feedback_from_chat(cleaned_chat)
            st.write(feedback)
        else:
            st.info("No text input provided.")
    
    # column 1
    with col2:
        if text_file is not None:
            content = text_file.read().decode("utf-8").strip()
            if content:
                cleaned_chat = parse_chat(content)
                feedback = get_feedback_from_chat(cleaned_chat)
                st.write(feedback)
            else:
                st.warning("Uploaded file is empty.")
        else:
            st.info("No file uploaded.")

# Tab 2: Raw Data
with tab2:
    st.title("Raw Data")

    if input_text.strip():
        raw_data = input_text.strip()
        st.write(raw_data)

    elif text_file is not None:
        stringio = StringIO(text_file.getvalue().decode("utf-8"))
        content = stringio.read().strip()
        if content:
            raw_data = content
            st.write(raw_data)
        else:
            st.warning("Uploaded file is empty.")
    else:
        st.write("Upload chat data for analysis.")

# Tab 3: Processed Data
with tab3:
    st.title("Processed Data")

    if raw_data:
        parsed = parse_chat(raw_data)
        st.json(parsed)
    else:
        st.write("Upload chat data for analysis.")
