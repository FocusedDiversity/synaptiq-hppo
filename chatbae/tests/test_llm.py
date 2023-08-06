from collections import namedtuple

import pytest

from chatbae.llm import init_mlc_chat, MLCArgs, MLCChatConfig


@pytest.fixture(scope="session")
def chat_mod():
    chat_mod = init_mlc_chat(
        MLCArgs(
            **dict(
                artifact_path="dist",
                model="Llama-2-7b-chat-hf",
                quantization="q4f16_1",
                device_name="metal",
                device_id=0,
            )
        ),
        MLCChatConfig(**dict(temperature=1.0, max_gen_len=8192)),
    )
    return chat_mod


def test_init(chat_mod):
    assert chat_mod


def test_llm_decodes(chat_mod):
    chat_mod.prefill(input="Hello")
    response = ""
    while not chat_mod.stopped():
        chat_mod.decode()
        response = chat_mod.get_message()
    assert "Hello" in response


def test_llm_tells_stories(chat_mod):
    chat_mod.prefill(input="Tell me a story.")
    response = ""
    while not chat_mod.stopped():
        chat_mod.decode()
        response = chat_mod.get_message()
    assert "Hello" in response
