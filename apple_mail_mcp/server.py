"""FastMCP server instance and user preferences."""

import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Apple Mail MCP")

# Load user preferences from environment
USER_PREFERENCES = os.environ.get("USER_EMAIL_PREFERENCES", "")

# Read-only mode flag — set via --read-only CLI argument.
# When enabled, compose/reply/forward tools are removed entirely and
# manage_drafts create/send actions are blocked. Truly read-only.
READ_ONLY = False

# Draft-only mode flag — set via --draft-only CLI argument or as default.
# When enabled, compose/reply/forward tools are available but forced to save
# as draft instead of sending. manage_drafts send action is also blocked.
# Default True: safest operational mode. Use --read-only to override to full lockdown.
DRAFT_ONLY = True
