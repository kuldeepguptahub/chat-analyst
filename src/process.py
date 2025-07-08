import re
from typing import List, Dict

def parse_chat(chat_text:str) -> List[Dict[str, str]]:
    agent = None
    customer = None
    speakers = []
    structured_chat = []

    # Step 1: Convert chat_text into a list of strings

    chat_lines = chat_text.strip().split('\n')

    # Step 2: Clean up chat lines removing system messages, timestamps
    patterns = [
    r'\d{2}:\d{2}', # datestamp
    r'Copilot', #copilot
    r'canned', #canned
    r'Internal note', #internal notes
    r'Archived - customer left' # Archived message
    ]

    chat_lines = [line for line in chat_lines if not any(re.search(p, line) for p in patterns)]

    # Step 3: Remove any empty lines

    chat_lines = [line.strip() for line in chat_lines if line != '']

    # Step 4: Identify the agent by looking for canned response
    for i, line in enumerate(chat_lines):
        if "thank you for contacting" in line.lower():
            if i > 0:
                agent = chat_lines[i - 1].strip()
                break

    if not agent:
        raise ValueError("Agent could not be identified from canned message.")

    # Step 5: Identify customer as first different speaker
    for line in chat_lines:
        if re.match(r'^[A-Za-z0-9.@_\-\s]{1,30}$', line.strip()):  # likely a name/email/ID line
            name = line.strip()
            if name != agent:
                customer = name
                break

    if not customer:
        raise ValueError("Customer could not be identified.")

    # Step 6: Replace names and build role-labeled structure
    role_map = {agent: "agent", customer: "customer"}

    current_speaker = None
    message_buffer = []

    for line in chat_lines:
        line = line.strip()
        
        # Check if it's a speaker line
        if line in role_map:
            # Flush any buffered message
            if current_speaker and message_buffer:
                structured_chat.append({
                    current_speaker: " ".join(message_buffer).strip()
                })
                message_buffer = []
            current_speaker = role_map[line]
        else:
            message_buffer.append(line)

    # Add final message
    if current_speaker and message_buffer:
        structured_chat.append({
            current_speaker: " ".join(message_buffer).strip()
        })

    return structured_chat
