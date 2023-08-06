import json
import os
import subprocess
import sys
from dataclasses import dataclass, fields, asdict, is_dataclass
from typing import Optional

import tvm
from mlc_chat import ChatModule


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
    artifact_path: str
    model: str
    quantization: str = "q4f16_1"
    device_name: str = "metal"
    device_id: int = 0


@dataclass
class MLCChatConvConfig:
    system: str


@dataclass
class MLCChatConfig:
    """
    https://mlc.ai/mlc-llm/docs/get_started/mlc_chat_config.html
    """

    temperature: Optional[float] = None
    repetition_penalty: Optional[float] = None
    top_p: Optional[float] = None
    mean_gen_len: Optional[int] = None
    max_gen_len: Optional[int] = None
    shift_fill_factor: Optional[float] = None
    conv_config: Optional[MLCChatConvConfig] = None

    @staticmethod
    def uncensored():
        return MLCChatConfig(
            temperature=1.0,
            max_gen_len=4096,
            conv_config=MLCChatConvConfig(
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
        )


def configure_model(chat_config: MLCChatConfig, model_path: str) -> None:
    mlc_chat_config_path = os.path.join(model_path, "mlc-chat-config.json")
    config_file = open(mlc_chat_config_path, "r")
    config = json.load(config_file)
    config_file.close()

    for field in fields(chat_config):
        value = getattr(chat_config, field.name)
        if value:
            if is_dataclass(value):
                value = asdict(value)
            config[field.name] = value

    config_file = open(mlc_chat_config_path + ".tmp", "w")
    json.dump(config, config_file, indent=2, sort_keys=True)
    config_file.close()
    os.replace(mlc_chat_config_path + ".tmp", mlc_chat_config_path)


def init_mlc_chat(args: MLCArgs, chat_config: MLCChatConfig) -> ChatModule:
    """
    Initialize the mlc chat llm library and weights
    :param args:
    :return:
    """
    chat_mod = ChatModule(args.device_name, args.device_id)
    model_path = os.path.join(args.artifact_path, args.model + "-" + args.quantization)
    model_dir = args.model + "-" + args.quantization
    model_lib = model_dir + "-" + args.device_name + _shared_lib_suffix()
    lib_dir = os.path.join(model_path, model_lib)
    prebuilt_lib_dir = os.path.join(args.artifact_path, "prebuilt", "lib", model_lib)
    if os.path.exists(lib_dir):
        lib = tvm.runtime.load_module(lib_dir)
    elif os.path.exists(prebuilt_lib_dir):
        lib = tvm.runtime.load_module(prebuilt_lib_dir)
    else:
        raise ValueError(
            f"Unable to find {model_lib} at {lib_dir} or {prebuilt_lib_dir}."
        )

    local_model_path = os.path.join(model_path, "params")
    prebuilt_model_path = os.path.join(
        args.artifact_path, "prebuilt", f"mlc-chat-{model_dir}"
    )
    if os.path.exists(local_model_path):
        configure_model(chat_config, prebuilt_model_path)
        chat_mod.reload(lib=lib, model_path=local_model_path)
    elif os.path.exists(prebuilt_model_path):
        configure_model(chat_config, prebuilt_model_path)
        chat_mod.reload(lib=lib, model_path=prebuilt_model_path)
    else:
        raise ValueError(
            f"Unable to find model params at {local_model_path} or {prebuilt_model_path}."
        )

    chat_mod.process_system_prompts()
    return chat_mod
