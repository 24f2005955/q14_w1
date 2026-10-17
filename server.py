import hashlib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

EMAIL = "24f2005955@ds.study.iitm.ac.in"

mcp = FastMCP(name="exam-mcp-server")

@mcp.tool
def solve_challenge() -> str:
    """Returns the required hash for the challenge sent in HTTP headers."""
    headers = get_http_headers()

    challenge = headers.get("x-exam-challenge", "")
    timestamp = headers.get("x-exam-timestamp", "")
    signature = headers.get("x-exam-signature", "")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    digest = hashlib.sha256(f"{challenge}:{EMAIL}".encode("utf-8")).hexdigest()
    return digest[:16]

import os

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        path="/mcp"
    )
