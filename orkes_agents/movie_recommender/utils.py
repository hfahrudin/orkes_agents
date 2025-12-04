import json
import re

from duckduckgo_search import DDGS


def extract_json(raw_text: str):
    cleaned = re.sub(r"```json\s*|```", "", raw_text, flags=re.IGNORECASE).strip()
    return json.loads(cleaned)


def search(query, max_results=10):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r)
    return results
