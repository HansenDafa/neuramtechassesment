import httpx
import json
import re
from typing import Dict


def extract_structured_info(text: str, api_key: str, model: str = "gpt-4o-mini") -> Dict[str, str]:
    """Call OpenRouter to extract structured fields from CV text.

    Returns a dict with keys: name, location, work_experience_summary.
    Raises ValueError for missing API key and RuntimeError for request failures.
    """
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not configured")

    prompt = (
        "Extract the following fields from the provided CV text and return a compact JSON object with keys: "
        "\"name\", \"location\", \"work_experience_summary\". If a field is missing, use null or empty string.\n\n"
        "CV_TEXT:\n"
        f"{text}\n\n"
        "Return ONLY valid JSON."
    )

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 800,
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        r = httpx.post("https://api.openrouter.ai/v1/chat/completions", json=payload, headers=headers, timeout=30.0)
        r.raise_for_status()
        data = r.json()

        # Extract assistant content from a few possible response shapes
        content = None
        if isinstance(data, dict):
            choices = data.get("choices") or []
            if choices:
                first = choices[0]
                if isinstance(first, dict):
                    msg = first.get("message") or first.get("delta") or {}
                    if isinstance(msg, dict):
                        content = msg.get("content") or msg.get("text")
        if not content:
            # fallback to top-level text
            if isinstance(data, dict) and data.get("choices") and data["choices"][0].get("text"):
                content = data["choices"][0]["text"]

        if not content:
            raise RuntimeError("No assistant content in OpenRouter response")

        # Try to locate JSON within the assistant message
        m = re.search(r"(\{.*\})", content, re.S)
        json_text = m.group(1) if m else content
        result = json.loads(json_text)

        return {
            "name": result.get("name"),
            "location": result.get("location"),
            "work_experience_summary": result.get("work_experience_summary"),
        }

    except httpx.HTTPStatusError as he:
        raise RuntimeError(f"OpenRouter API error: {he.response.status_code} {he.response.text}")
    except Exception as e:
        raise RuntimeError(f"LLM request failed: {e}")
