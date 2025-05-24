import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.utils.retry import retry_on_failure


def test_retry_decorator_retries_twice_before_success(monkeypatch):
    calls = {"count": 0}

    @retry_on_failure(max_attempts=3, delay=0)
    def flaky():
        calls["count"] += 1
        if calls["count"] < 3:
            raise ValueError("fail")
        return "success"

    assert flaky() == "success"
    assert calls["count"] == 3
