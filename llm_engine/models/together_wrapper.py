import os
import together
import json

from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    raise EnvironmentError("TOGETHER_API_KEY not set in .env file.")

together_client = together.Together(api_key=TOGETHER_API_KEY)

def call_together_api(prompt: str, 
                      parsed_data: str, 
                      model: str = "meta-llama/Llama-Vision-Free") -> dict:
    """
    Calls Together.ai with the given prompt and returns parsed JSON response.
    Raises error if model output is invalid or unparseable.
    """

    feedback = []

    try:
        response = together_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": str(parsed_data)
                }
            ],
            max_tokens=3000,
            stream=True
        )

        for token in response:
            if hasattr(token, 'choices') and token.choices:
                delta = token.choices[0].delta
                if delta and hasattr(delta, 'content') and delta.content:
                    feedback.append(delta.content)
            
        feedback = ''.join(feedback)

        # Try parsing as JSON
        try:
            return json.loads(feedback)
        except json.JSONDecodeError:
            raise ValueError("Model output is not valid JSON.")

    except Exception as e:
        raise RuntimeError(f"Together.ai request failed: {str(e)}")
