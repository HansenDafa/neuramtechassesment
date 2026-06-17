import httpx
from typing import List, Dict


def search_news(query: str, api_key: str, base_url: str = "https://api.tavily.com/search") -> List[Dict]:
    """Search news via Tavily API. Returns list of normalized articles.

    The Tavily API shape may vary; this function tries common response keys.
    """
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not configured")

    params = {"query": query, "limit": 10}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        # Tavily may expect a POST with JSON body for search; try POST first.
        r = httpx.post(base_url, json=params, headers=headers, timeout=20.0)
        if r.status_code == 405:
            # fallback to GET if POST not allowed
            r = httpx.get(base_url, params=params, headers={"Authorization": f"Bearer {api_key}"}, timeout=20.0)
        r.raise_for_status()
        data = r.json()

        items = []
        if isinstance(data, dict):
            items = data.get("results") or data.get("articles") or []
        elif isinstance(data, list):
            items = data

        results = []
        for it in items:
            if not isinstance(it, dict):
                continue
            title = it.get("title") or it.get("headline")
            summary = it.get("summary") or it.get("content") or it.get("description")
            url = it.get("url") or it.get("link")
            date = it.get("published_at") or it.get("date")
            if title and url:
                results.append({"title": title, "summary": summary, "url": url, "date": date})

        return results

    except httpx.HTTPStatusError as he:
        raise RuntimeError(f"Tavily API error: {he.response.status_code} {he.response.text}")
    except Exception as e:
        raise RuntimeError(f"Tavily request failed: {e}")
