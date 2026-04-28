# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from google import genai
from google.genai import types
import traceback
from .config import API_KEY
import requests

def generate(text, system_instruction=""):
    result_text = ""
    try:
        client = genai.Client(
            api_key=API_KEY,
        )

        model = "gemma-4-26b-a4b-it"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=text),
                ],
            ),
        ]
        tools = [
            types.Tool(googleSearch=types.GoogleSearch(
            )),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level="HIGH",
            ),
            tools=tools,
            system_instruction=[
            types.Part.from_text(text=system_instruction),
        ],

        )

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                result_text += chunk.text
    except Exception as e:
        result_text = f"Lỗi Gemini: {str(e)}\n{traceback.format_exc()}"
    
    return result_text

def send_facebook_message(psid, text, access_token):
    url = f"https://graph.facebook.com/v19.0/me/messages"

    params = {
        "access_token": access_token
    }

    payload = {
        "recipient": {"id": psid},
        "message": {"text": text}
    }

    try:
        res = requests.post(url, params=params, json=payload, timeout=10)
        return res.text
    except Exception as e:
        return str(e)
