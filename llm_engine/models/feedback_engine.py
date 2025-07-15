import os
from pathlib import Path
import json

from dotenv import load_dotenv

from llm_engine.models.together_wrapper import call_together_api

load_dotenv()

# Constants
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "system_prompts.txt"

def get_feedback_from_chat(chat: list[dict]) -> dict:
    """
    Accepts a cleaned chat transcript (list of dicts).
    Loads system prompt, formats chat as string, sends to Together.ai.
    Returns parsed feedback JSON.
    """
    if not isinstance(chat, list) or not all(isinstance(msg, dict) for msg in chat):
        raise ValueError("Invalid input format. Expected list of dictionaries.")

    # Load system prompt
    try:
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        raise RuntimeError("System prompt template not found.")

    # Format parsed_data string (optional: you can use json.dumps or custom formatter)
    parsed_data = json.dumps(chat, indent=2)

    # Call Together API with prompt + chat data
    feedback = call_together_api(system_prompt, parsed_data)

    return feedback