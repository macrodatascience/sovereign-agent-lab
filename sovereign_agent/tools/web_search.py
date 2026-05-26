from langchain_core.tools import tool
import json
import requests

@tool
def search_web(query: str) -> str:
    """
    Simple web search tool (mock-safe version using DuckDuckGo API style endpoint).
    Returns top results as JSON string.
    """
    
    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1,
            },
            timeout=8,
        )

        data = resp.json()

        answer = data.get("AbstractText", "")
        source = data.get("AbstractURL", "")

        # fallback: use related topics if no abstract
        related = data.get("RelatedTopics", [])

        flattened = []
        for item in related:
            if isinstance(item, dict) and "Text" in item:
                flattened.append(item["Text"])

        if not answer and flattened:
            answer = " | ".join(flattened[:5])

        results = {
            "query": query,
            "answer": answer if answer else None,
            "source": source if source else None,
            "related": flattened[:5] if flattened else None,
        }
        return json.dumps(results)
    
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

    # try:
    #     resp = requests.get(
    #         "https://api.duckduckgo.com/",
    #         params={
    #             "q": query,
    #             "format": "json",
    #             "no_html": 1,
    #             "skip_disambig": 1,
    #         },
    #         timeout=8,
    #     )

    #     data = resp.json()

    #     results = {
    #         "answer": data.get("AbstractText", ""),
    #         "source": data.get("AbstractURL", ""),
    #     }

    #     return json.dumps(results)

    # except Exception as e:
    #     return json.dumps({
    #         "success": False,
    #         "error": str(e)
    #     })
        
    # Mock response for testing without real API calls.
    
    # return json.dumps({
    #     "query": query,
    #     "results": [
    #         {
    #             "title": f"Search result for {query}",
    #             "url": "https://example.com",
    #             "snippet": "Simulated web result for agent reasoning."
    #         },
    #         {
    #             "title": "Venue listing page",
    #             "url": "https://example.com/venues",
    #             "snippet": "Large venues in Edinburgh for events."
    #         }
    #     ]
    # })