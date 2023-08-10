import argparse
import asyncio
import logging

from dotenv_vault import load_dotenv
from mlc_chat.chat_module import quantization_keys

from chatbae.bot import init_slack_bot
from chatbae.llm import init_mlc_chat, MLCArgs, MLCChatConfig

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

def get_chat_mod(args):
    def get_bot():
        mlc_args = MLCArgs(**vars(args))
        chat_config = MLCChatConfig.uncensored()
        return init_mlc_chat(mlc_args, chat_config)
    return get_bot

async def main():
    args = _parse_args()
    await init_slack_bot(get_chat_mod(args))


# Start your app
if __name__ == "__main__":
    asyncio.run(main())
