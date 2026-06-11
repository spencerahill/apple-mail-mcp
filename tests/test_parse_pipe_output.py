"""Tests for the pipe-output parsers (field positions and key mapping)."""

from apple_mail_mcp.tools.search import _parse_flagged_pipe_output, _parse_pipe_output


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


def test_flagged_record_without_content():
    raw = (
        "Re: Faculty Stipend|||Judith Disla <jd@ccny.cuny.edu>"
        "|||Friday, June 5, 2026 at 11:28:25 AM|||false"
        "|||ADM_26-summer-salary|||ABC123@outlook.com|||Orange"
    )
    [email] = _parse_flagged_pipe_output(raw, "CCNY")
    assert email["subject"] == "Re: Faculty Stipend"
    assert email["is_read"] is False
    assert email["account"] == "CCNY"
    assert email["mailbox"] == "ADM_26-summer-salary"
    assert email["message_id"] == "ABC123@outlook.com"
    assert email["flag_color"] == "orange"
    assert email["content"] == ""


def test_flagged_record_with_content():
    raw = (
        "Subj|||s@x.edu|||Monday, May 18, 2026 at 1:30:54 PM|||true"
        "|||GR_doe-wrl|||DEF456@x.edu|||Blue|||Preview text"
    )
    [email] = _parse_flagged_pipe_output(raw, "CCNY")
    assert email["flag_color"] == "blue"
    assert email["content"] == "Preview text"


def test_flagged_skips_non_record_lines():
    raw = "some header noise\nA|||b|||c|||true|||M|||id|||Red\n"
    emails = _parse_flagged_pipe_output(raw, "LDEO")
    assert len(emails) == 1
    assert emails[0]["account"] == "LDEO"
    assert emails[0]["flag_color"] == "red"
