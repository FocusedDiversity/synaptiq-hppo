import pytest

from chatbae.digest import digest, harvest_url


def test_harvest_url_https():
    assert harvest_url("plugin:digest https://synaptiq.ai") == "https://synaptiq.ai"


def test_harvest_url_http():
    assert harvest_url("plugin:digest http://synaptiq.ai") == "http://synaptiq.ai"


def test_harvest_url_foobar():
    assert harvest_url("foobar https://synaptiq.ai foobar") == "https://synaptiq.ai"


def test_harvest_url_first():
    assert (
        harvest_url(
            "The best https website is this https://synaptiq.ai not this https://wwww.wikipedia.com"
        )
        == "https://synaptiq.ai"
    )


@pytest.mark.internet
def test_digest(chat_mod):
    prompt = "plugin:digest https://synaptiq.ai"
    summary = digest(chat_mod, prompt)
    assert "YouTube" in summary
