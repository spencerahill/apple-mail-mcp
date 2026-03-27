# Local Customizations (spencerahill fork)

Changes maintained on top of upstream (patrickfreyer/apple-mail-mcp):

1. **get_flagged_emails** (search.py) — Flag color filtering with efficient `whose` clause across all mailboxes
2. **Attachment mailbox parameter** (analytics.py, manage.py) — `mailbox` param on `list_email_attachments` and `save_email_attachment`, using `build_mailbox_ref()` for nested path support
3. **Colored flag actions** (manage.py) — `flag_red` through `flag_gray` actions in `update_email_status` that set `flag index`
4. **FLAG_COLOR_MAP constants** (constants.py) — Zero-indexed flag color mapping (Red=0 through Gray=6)
5. **SKIP_FOLDERS additions** (constants.py) — Added "Sent Mail", "All Mail", "Bin" to prevent duplicates in broad searches
6. **Cross-account move support** (manage.py, bulk.py) — `to_account` parameter on `move_email` and `bulk_move_emails` for moving emails between accounts (e.g., Columbia inbox → CCNY filing mailbox)
7. **MCP config** (~/.claude/.mcp.json) — `--draft-only` flag to force compose/reply/forward into draft mode
8. **Draft-only mode** (apple_mail_mcp.py, server.py, compose.py) — New `--draft-only` CLI flag: compose/reply/forward tools stay available but are forced to save as draft, never send. `--read-only` is now truly read-only (also blocks draft creation). The two flags are mutually exclusive.
9. **reply_to_email mailbox parameter** (compose.py) — `mailbox` param (default "INBOX") so replies can target emails in any mailbox (e.g., Sent Items, advising/haochang-luo). Uses `build_mailbox_ref()` for nested path support. NOTE: draft mode has known threading limitations for non-inbox messages (AppleScript `set content` breaks Mail's HTML threading layer). Works correctly in "open" and "send" modes.

## Rebase workflow

```bash
git fetch upstream
git tag pre-rebase-$(date +%Y-%m-%d)
git rebase upstream/main
# resolve conflicts
git diff pre-rebase-$(date +%Y-%m-%d) HEAD --stat  # verify no regressions
```

## Rebase checklist

After rebasing onto upstream, verify each item above is present:

- [ ] `get_flagged_emails` tool exists in search.py
- [ ] `list_email_attachments` has `mailbox` parameter (analytics.py)
- [ ] `save_email_attachment` has `mailbox` parameter (manage.py)
- [ ] `update_email_status` supports `flag_red` through `flag_gray` (manage.py)
- [ ] `FLAG_COLOR_MAP` and `FLAG_INDEX_TO_COLOR` exist in constants.py
- [ ] `SKIP_FOLDERS` includes "Sent Mail", "All Mail", "Bin" (constants.py)
- [ ] `move_email` has `to_account` parameter (manage.py)
- [ ] `bulk_move_emails` has `to_account` parameter (bulk.py)
- [ ] `--draft-only` flag in MCP config (~/.claude/.mcp.json)
- [ ] `DRAFT_ONLY` flag in server.py
- [ ] compose_email forces `mode="draft"` when DRAFT_ONLY (compose.py)
- [ ] reply_to_email forces `effective_mode="draft"` when DRAFT_ONLY (compose.py)
- [ ] forward_email saves as draft instead of sending when DRAFT_ONLY (compose.py)
- [ ] manage_drafts blocks "create" when READ_ONLY, blocks "send" when READ_ONLY or DRAFT_ONLY (compose.py)
- [ ] `reply_to_email` has `mailbox` parameter using `build_mailbox_ref()` (compose.py)
