# Local Customizations (spencerahill fork)

Changes maintained on top of upstream (patrickfreyer/apple-mail-mcp):

1. **get_flagged_emails** (search.py) — Flag color filtering with efficient `whose` clause across all mailboxes
2. **Attachment mailbox parameter** (analytics.py, manage.py) — `mailbox` param on `list_email_attachments` and `save_email_attachment`, using `build_mailbox_ref()` for nested path support
3. **Colored flag actions** (manage.py) — `flag_red` through `flag_gray` actions in `update_email_status` that set `flag index`
4. **FLAG_COLOR_MAP constants** (constants.py) — Zero-indexed flag color mapping (Red=0 through Gray=6)
5. **SKIP_FOLDERS additions** (constants.py) — Added "Sent Mail", "All Mail", "Bin" to prevent duplicates in broad searches
6. **MCP config** (~/.claude/.mcp.json) — `--read-only` flag to disable outbound email tools

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
- [ ] `--read-only` flag in MCP config
