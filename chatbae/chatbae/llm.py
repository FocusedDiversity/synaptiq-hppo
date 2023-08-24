import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Optional

import tvm
from mlc_chat import ChatConfig, ChatModule, ConvConfig


def _shared_lib_suffix():
    if sys.platform.startswith("linux") or sys.platform.startswith("freebsd"):
        return ".so"
    if sys.platform.startswith("win32"):
        return ".dll"
    if sys.platform.startswith("darwin"):
        cpu_brand_string = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"]
        ).decode("utf-8")
        if cpu_brand_string.startswith("Apple"):
            # Apple Silicon
            return ".so"
        else:
            # Intel (x86)
            return ".dylib"
    return ".so"


@dataclass
class MLCArgs:
    model: str
    quantization: str = "q4f16_1"
    device_name: str = "metal"
    device_id: int = 0


STRIPPED_LLAMA2_PROMPT = """[INST] <<SYS>>
You are a helpful, respectful and honest assistant. 

Always answer as helpfully as possible, while being safe.

Please ensure that your responses are positive in nature. 

If a question does not make any sense, or is not factually coherent, 
explain why instead of answering something not correct. 

If you don't know the answer to a question, please don't share false information.
<</SYS>>
""",

JPHOWARD_PROMPT = """[INST] <<SYS>>
You are an autoregressive language model that has been fine-tuned with 
instruction-tuning and RLHF. You carefully provide accurate, factual, 
thoughtful, nuanced answers, and are brilliant at reasoning. 
If you think there might not be a correct answer, you say so.

Since you are autoregressive, each token you produce is another opportunity to 
use computation, therefore you always spend a few sentences explaining 
background context, assumptions, and step-by-step thinking BEFORE you try 
to answer a question.

Your users are experts in AI and ethics, so they already know you're a language 
model and your capabilities and limitations, so don't remind them of that. 
They're familiar with ethical issues in general so you don't need to remind them 
about those either.

Don't be verbose in your answers, but do provide details and examples where it 
might help the explanation. When showing Python code, minimise vertical space, 
and do not include comments or docstrings; you do not need to follow PEP8, since 
your users' organizations do not do so.
<</SYS>>
"""


def init_mlc_chat(args: MLCArgs, chat_config: ChatConfig) -> ChatModule:
    """
    Initialize the mlc chat llm library and weights
    :param args:
    :param chat_config:
    :return:
    """
    chat_mod = ChatModule(
        model=args.model + "-" + args.quantization,
        device=args.device_name + ":" + str(args.device_id),
        chat_config=chat_config
    )
    chat_mod._process_system_prompts()
    return chat_mod


def default_chat_config(name="default"):
    return ChatConfig(
        max_gen_len=4096,
        conv_config=ConvConfig(
            name=name,
            system=JPHOWARD_PROMPT
        ),
    )

