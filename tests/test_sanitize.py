"""Tests for _sanitize_for_json Unicode preservation."""

from apple_mail_mcp.core import _sanitize_for_json


def test_preserves_unicode():
    s = "2026 Summer Salary — naïve sender AM"
    assert _sanitize_for_json(s) == s


def test_normalizes_line_endings_and_strips_controls():
    assert _sanitize_for_json("a\r\nb\rc\x00d\x7fe\tf") == "a\nb\ncd" + "e\tf"
