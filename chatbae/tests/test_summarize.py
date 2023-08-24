import pytest
import requests
from bs4 import BeautifulSoup
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
            temperature=0.2,
            # max_gen_len=4096,
            conv_config=ConvConfig(
                system=JPHOWARD_PROMPT,
            ),
        ),
    )
    return chat_mod


def test_summarize(chat_mod):
    text = requests.get("http://shakespeare.mit.edu/lear/full.html").text
    soup = BeautifulSoup(text, "html.parser")
    print(len(soup.text))
    win = 1024
    print(soup.text[:win])
    response = chat_mod.generate(
        prompt=f"""
            Please summarize the content of this text: {soup.text[:win]}
        """
    )
    print(response)

    assert True
