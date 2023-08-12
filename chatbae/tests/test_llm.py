from collections import namedtuple

import pytest
from mlc_chat import ChatConfig, ConvConfig

from chatbae.llm import init_mlc_chat, MLCArgs


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
                system="""[INST] <<SYS>>
                
                You are a helpful, respectful and honest assistant. 
                
                Always answer as helpfully as possible, while being safe.
                
                Please ensure that your responses are positive in nature. 
                
                If a question does not make any sense, or is not factually coherent, 
                explain why instead of answering something not correct. 
                
                If you don't know the answer to a question, please don't share false information.
                <</SYS>>
                """,
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
