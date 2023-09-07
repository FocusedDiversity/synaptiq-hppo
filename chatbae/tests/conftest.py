import pytest
from mlc_chat import ChatConfig, ConvConfig

from chatbae.llm import JPHOWARD_PROMPT, MLCArgs, init_mlc_chat


def pytest_collection_modifyitems(config, items):
    keywordexpr = config.option.keyword
    markexpr = config.option.markexpr
    if keywordexpr or markexpr:
        return  # let pytest handle this

    skip_internet = pytest.mark.skip(reason="needs internet")
    for item in items:
        if "internet" in item.keywords:
            item.add_marker(skip_internet)


@pytest.fixture(scope="session")
def chat_mod():
    chat_mod = init_mlc_chat(
        MLCArgs(
            model="mlc-chat-Llama-2-7b-chat-hf",
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
