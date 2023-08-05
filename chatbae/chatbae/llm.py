import os
import subprocess
import sys
from collections import namedtuple

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


LLM_ARGS = namedtuple(
    "ARGS", ["artifact_path", "model", "quantization", "device_name", "device_id"]
)


def init_mlc_chat(args: LLM_ARGS):
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
        chat_mod.reload(lib=lib, model_path=local_model_path)
    elif os.path.exists(prebuilt_model_path):
        chat_mod.reload(lib=lib, model_path=prebuilt_model_path)
    else:
        raise ValueError(
            f"Unable to find model params at {local_model_path} or {prebuilt_model_path}."
        )

    chat_mod.process_system_prompts()
    return chat_mod
