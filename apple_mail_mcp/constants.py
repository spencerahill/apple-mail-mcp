"""Shared constants for Apple Mail MCP tools."""

# Newsletter detection patterns (sender-based)
NEWSLETTER_PLATFORM_PATTERNS = [
    "substack.com", "beehiiv.com", "mailchimp", "sendgrid",
    "convertkit", "buttondown", "ghost.io", "revue.co", "mailgun",
]

NEWSLETTER_KEYWORD_PATTERNS = [
    "newsletter", "digest", "weekly", "daily",
    "bulletin", "briefing", "news@", "updates@",
]

# Folders to skip during broad searches
SKIP_FOLDERS = [
    "Trash", "Junk", "Junk Email", "Deleted Items",
    "Sent", "Sent Items", "Sent Messages", "Sent Mail",
    "Drafts", "Spam", "Deleted Messages", "All Mail", "Bin",
]

# Flag color mapping (zero-indexed, empirically confirmed on macOS Sequoia)
FLAG_COLOR_MAP = {
    "red": 0, "orange": 1, "yellow": 2, "green": 3,
    "blue": 4, "purple": 5, "gray": 6,
}
FLAG_INDEX_TO_COLOR = {v: k for k, v in FLAG_COLOR_MAP.items()}

# Thread subject prefixes to strip when matching threads
THREAD_PREFIXES = ["Re:", "Fwd:", "FW:", "RE:", "Fw:"]

# Human-friendly time range mappings (name -> days)
TIME_RANGES = {
    "today": 1,
    "yesterday": 2,
    "week": 7,
    "month": 30,
    "all": 0,
}
