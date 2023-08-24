import pytest

from chatbae.digest import digest


@pytest.mark.internet
def test_digest(chat_mod):
    prompt = "plugin:digest https://synaptiq.ai"
    summary = digest(chat_mod, prompt)
    assert "YouTube" in summary
