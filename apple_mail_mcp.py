#!/usr/bin/env python3
"""Apple Mail MCP Server - Entry point.

Supports two safety modes (mutually exclusive):
  --read-only   Truly read-only: compose/reply/forward tools removed, draft
                creation blocked.  Only search/read/move/flag/delete available.
  --draft-only  Compose/reply/forward available but forced to save as draft —
                never send.  manage_drafts "send" action is also blocked.
"""

import argparse
import apple_mail_mcp.server as server

parser = argparse.ArgumentParser(description="Apple Mail MCP Server")
mode_group = parser.add_mutually_exclusive_group()
mode_group.add_argument(
    "--read-only",
    action="store_true",
    help="Truly read-only: remove compose/reply/forward tools, block draft creation.",
)
mode_group.add_argument(
    "--draft-only",
    action="store_true",
    help="Draft-only: compose/reply/forward create drafts instead of sending.",
)
args = parser.parse_args()

# Set flags before tools are imported (decorator registration happens on import).
# DRAFT_ONLY defaults to True in server.py (safest mode). CLI/env can override.
import os
env_mode = os.environ.get("APPLE_MAIL_MODE", "")
if args.read_only or env_mode == "read-only":
    server.READ_ONLY = True
    server.DRAFT_ONLY = False  # read-only is stricter; override draft-only default
elif args.draft_only or env_mode == "draft-only":
    server.DRAFT_ONLY = True  # explicit, but also the default

from apple_mail_mcp import mcp  # noqa: E402

# In read-only mode, remove send-capable tools that were registered by decorators.
if server.READ_ONLY:
    for name in ["compose_email", "reply_to_email", "forward_email"]:
        try:
            mcp.remove_tool(name)
        except (KeyError, ValueError):
            pass  # Tool may not exist — fine to skip.

if __name__ == "__main__":
    mcp.run()
