import streamlit as st
import pandas as pd
from io import StringIO
import json
from src.process import parse_chat
from llm_engine.models.feedback_engine import get_feedback_from_chat

# Page config
st.set_page_config(page_title="SelfQA Analyst", page_icon="🤖")
st.title("👋 I'm your QA Analyst")

# Initialize state
if "raw_data" not in st.session_state:
    st.session_state.raw_data = None
    st.session_state.parsed = None
    st.session_state.feedback = None

# Sidebar

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 600px;
            max-width: 600px;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-right: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("Paste or Upload your chat here")
    input_text = st.text_area(label="Paste your chat here")
    submit_button = st.button("Analyze")

    st.subheader("Or")

    text_file = st.file_uploader("Upload a .txt file", type="txt", accept_multiple_files=False)

    # Handle input
    if submit_button:
        if input_text.strip():
            st.session_state.raw_data = input_text.strip()
        else:
            st.warning("You submitted a blank input.")

    elif text_file is not None:
        uploaded_text = text_file.read().decode("utf-8").strip()
        if uploaded_text:
            st.session_state.raw_data = uploaded_text
        else:
            st.warning("Did you upload a blank file?")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Chat Analysis", "Raw Data", "Processed Data", "Report Card"])

# Tab 2: Raw Data
with tab2:
    if st.session_state.raw_data:
        st.write(st.session_state.raw_data)
    else:
        st.info("Upload chat data for analysis.")

# Tab 3: Parsed Chat
with tab3:
    if st.session_state.raw_data:
        try:
            st.session_state.parsed = parse_chat(st.session_state.raw_data)
            for d in st.session_state.parsed:
                for speaker, msg in d.items():
                    st.markdown(f"**{speaker}**: {msg}")
        except Exception:
            st.error("Something went wrong while parsing the chat.")
    else:
        st.info("Upload chat data for analysis.")

# Tab 1: QA Summary
with tab1:
    if not st.session_state.raw_data:
        st.info("Upload chat data for analysis.")
    else:
        st.subheader("🕵️‍♂️ QA Evaluation")
        with st.spinner("Analyzing chat and generating feedback..."):
            try:
                if st.session_state.parsed:
                    st.session_state.feedback = get_feedback_from_chat(st.session_state.parsed)
                    feedback = st.session_state.feedback

                    st.markdown("### 📝 Chat Summary")
                    st.markdown(feedback['issue_summary'])

                    st.markdown("### 😊 What Went Well")
                    for item in feedback['what_went_well']:
                        st.markdown(f"- {item}")

                    st.markdown("### 😐 What Can Be Improved")
                    for item in feedback['what_can_be_improved']:
                        for key, value in item.items():
                            st.write(f"{key}: {value}")

                    st.markdown("### 🚀 Quick Tip")
                    st.markdown(feedback['tip'])

                else:
                    st.warning("Chat couldn't be parsed correctly.")
            except Exception:
                st.error("⚠️ Oops, something went wrong. Please upload the chat again.")

# Tab 4: Detailed Report
with tab4:
    if not st.session_state.raw_data or not st.session_state.feedback:
        st.info("Upload chat data for analysis.")
    else:
        feedback = st.session_state.feedback
        st.subheader("📜 Summary")
        st.markdown(feedback["final_rating"]["summary"])

        st.subheader("📑 Category Scores")
        for category, details in feedback["categories"].items():
            st.markdown(f"**👉 {category}**")
            st.markdown(details["comment"])
