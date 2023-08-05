import argparse
import asyncio
import logging

from dotenv_vault import load_dotenv
from mlc_chat.chat_module import quantization_keys

from chatbae.bot import start_async_handler
from chatbae.llm import init_mlc_chat

load_dotenv()
logger = logging.getLogger(__name__)


def _parse_args():
    args = argparse.ArgumentParser("MLC Chat Slack API")
    args.add_argument("--model", type=str, default="Llama-2-70b-chat-hf")
    args.add_argument("--artifact-path", type=str, default="dist")
    args.add_argument(
        "--quantization",
        type=str,
        choices=quantization_keys(),
        default=quantization_keys()[2],
    )
    args.add_argument("--device-name", type=str, default="metal")
    args.add_argument("--device-id", type=int, default=0)

    parsed = args.parse_args()
    return parsed


async def main():
    args = _parse_args()
    init_mlc_chat(args)
    await start_async_handler()


# Start your app
if __name__ == "__main__":
    asyncio.run(main())
