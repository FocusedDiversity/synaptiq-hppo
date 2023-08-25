def test_init(chat_mod):
    assert chat_mod


def test_llm_decodes(chat_mod):
    response = chat_mod.generate(prompt="Hello")
    assert "Hello" in response


def test_llm_tells_stories(chat_mod):
    response = chat_mod.generate(prompt="Tell me a story.")
    assert "Hello" in response
