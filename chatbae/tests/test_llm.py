from collections import namedtuple

import pytest
from mlc_chat import ChatConfig, ConvConfig

from chatbae.llm import JPHOWARD_PROMPT, MLCArgs, init_mlc_chat


@pytest.fixture(scope="session")
def chat_mod():
    chat_mod = init_mlc_chat(
        MLCArgs(
            model="Llama-2-7b-chat-hf",
            quantization="q4f16_1",
            device_name="metal",
            device_id=0,
        ),
        ChatConfig(
            temperature=1.0,
            max_gen_len=4096,
            conv_config=ConvConfig(
                system=JPHOWARD_PROMPT,
            ),
        ),
    )
    return chat_mod


def test_init(chat_mod):
    assert chat_mod


def test_llm_decodes(chat_mod):
    response = chat_mod.generate(prompt="Hello")
    assert "Hello" in response


def test_llm_tells_stories(chat_mod):
    response = chat_mod.generate(prompt="Tell me a story.")
    assert "Hello" in response
