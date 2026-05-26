from langchain_core.tools import tool
import json

@tool
def read_file(path: str) -> str:
    """Read a file from disk."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.dumps({"success": True, "content": f.read()})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return json.dumps({"success": True, "path": path})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})