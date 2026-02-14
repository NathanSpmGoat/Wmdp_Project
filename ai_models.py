# ai_models.py
import os
import openai
import requests
import json

# --------------------
# ChatGPT via OpenAI
# --------------------
def query_chatgpt(question):
    """
    Interroge ChatGPT via l'API OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY non défini dans l'environnement")

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # rapide et suffisant pour tests
        messages=[{"role": "user", "content": question}],
        temperature=0
    )

    return response['choices'][0]['message']['content']


# --------------------
# Claude via Anthropic
# --------------------
def query_claude(question):
    """
    Interroge Claude via l'API Anthropic.
    """
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise ValueError("CLAUDE_API_KEY non défini dans l'environnement")

    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-v1",  # ou "claude-v1.3" selon ton compte
        "prompt": question,
        "max_tokens_to_sample": 1000,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("completion", "[Claude] Pas de réponse reçue")


# --------------------
# Gemini via Google
# --------------------
def query_gemini(question):
    """
    Interroge Google Gemini via HTTP API.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY non défini dans l'environnement")

    url = "https://gemini.api.google.com/v1/generate"  # exemple, à adapter selon docs Google
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": question,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("output_text", "[Gemini] Pas de réponse reçue")
