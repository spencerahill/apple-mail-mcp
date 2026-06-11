"""Tests for _parse_pipe_output field positions (message_id at 6, content at 7)."""

from apple_mail_mcp.tools.search import _parse_pipe_output


def test_full_record_with_message_id_and_content():
    raw = (
        "Subj|||sender@x.edu|||Tuesday, June 10, 2026 at 9:00:00 AM|||false"
        "|||CCNY|||INBOX|||ABC123@mail.example.com|||Body preview here"
    )
    [email] = _parse_pipe_output(raw)
    assert email["subject"] == "Subj"
    assert email["is_read"] is False
    assert email["mailbox"] == "INBOX"
    assert email["message_id"] == "ABC123@mail.example.com"
    assert email["content"] == "Body preview here"


def test_record_with_message_id_no_content():
    raw = (
        "Subj|||sender@x.edu|||Tuesday, June 10, 2026 at 9:00:00 AM|||true"
        "|||CCNY|||Archive|||ABC123@mail.example.com"
    )
    [email] = _parse_pipe_output(raw)
    assert email["message_id"] == "ABC123@mail.example.com"
    assert email["content"] == ""


def test_legacy_six_field_record():
    raw = "Subj|||sender@x.edu|||Tuesday, June 10, 2026 at 9:00:00 AM|||true|||CCNY|||Archive"
    [email] = _parse_pipe_output(raw)
    assert email["message_id"] == ""
    assert email["content"] == ""
