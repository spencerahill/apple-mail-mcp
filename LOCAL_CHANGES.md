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
10. **fetch_new_mail tool** (inbox.py) — Triggers Mail.app's "Get All New Mail" via AppleScript `check for new mail`, then sleeps `wait_seconds` (default 15) for the async sync to settle. Optional `account` parameter scopes to one account. Used by `/inbox-triage` (and intended for `/daily-review`, `/stale-check`) so queries see today's mail instead of running between Mail's poll cycles. Uses `launch` not `activate` to avoid stealing focus.
11. **Cross-account Gmail-source move fix** (core.py, manage.py, bulk.py) — `move_email` and `bulk_move_emails` cross-account moves (`to_account` set) now use `duplicate` to the destination followed by `move` of the original to the *source* account's Trash, instead of a single `move`. ROOT CAUSE: a plain AppleScript `move` from a Gmail/IMAP source to another account copies the message to the destination but does **not** strip the server-side `\Inbox` label from the source (Gmail has labels, not folders, and no real "Archive" mailbox; "Archive" resolves to All Mail where the message already lives). The local INBOX view drops it optimistically, but the next server sync restores it, so consolidation moves silently bounced back. Trash is the one operation that strips all Gmail labels server-side, so duplicate-to-dest + move-source-to-Trash clears the source inbox durably while preserving the copy on the destination account. Same-account moves are unchanged (plain `move`; Exchange folders and real Gmail labels both honor it). Helpers: `build_cross_account_move()` and `source_trash_setup()` in core.py (unit-tested in tests/test_bulk_helpers.py). Diagnosed 2026-06-04; the regression surfaced after the Phase-3 routing switch to built-in `Archive` + cross-account-to-CCNY targets.
12. **Message-ID in search/flagged output** (search.py): `search_emails` and `get_flagged_emails` now fetch `message id of aMessage` (the RFC822 Message-ID, per-message try with empty-string fallback) and include it in all output formats. Text output gains a `Message-ID:` line; the JSON pipe format carries it at fixed position 6 (before the optional content field), parsed into a `message_id` key by `_parse_pipe_output`. Added 2026-06-10 for the exec-asst Phase 3c flagged-mail/org-cache dedup, so real ids replace the synthetic `<backfill-stub:…@local>` ingestion stubs going forward.
13. **get_flagged_emails JSON output** (search.py): `output_format="json"` pipe mode mirroring `search_emails`, parsed by `_parse_flagged_pipe_output`. Record fields: subject, sender, date, is_read, mailbox, message_id, flag_color (lowercased label), content (optional, last position); `account` is injected Python-side from the tool parameter. Text mode is unchanged. Added 2026-06-10 so the exec-asst flag-snapshot pipeline (`plans/flag-cache-unification.md`) consumes structured data instead of parsing prose.

14. **Unicode-preserving output sanitization** (core.py): `_sanitize_for_json` no longer forces ASCII (upstream's `encode('ascii', 'replace')` turned every non-ASCII char into `?`: accented sender names, curly quotes, and the U+00A0/U+202F spaces Mail puts in subjects and formatted dates). It now only normalizes line endings and strips control characters; JSON-RPC escapes non-ASCII at serialization time, so the wire stays safe. Fixed 2026-06-11 because the `?`-mangled subjects broke the exec-asst flag-snapshot subject matching.

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
- [ ] `fetch_new_mail` tool exists in inbox.py (with `account` and `wait_seconds` parameters)
- [ ] `build_cross_account_move` and `source_trash_setup` exist in core.py; `move_email` and `bulk_move_emails` cross-account paths use duplicate + source-Trash (manage.py, bulk.py)
- [ ] `search_emails` and `get_flagged_emails` fetch `message id` and emit it in text (`Message-ID:` line) and pipe/JSON (`message_id` key, position 6) output; `_parse_pipe_output` parses it (search.py)
- [ ] `get_flagged_emails` has `output_format="json"` with `flag_color` + `message_id` keys; `_parse_flagged_pipe_output` exists (search.py)
- [ ] `_sanitize_for_json` preserves Unicode (no ascii-replace pass) (core.py)
