# Databricks notebook source
# MAGIC %pip install slack-bolt
# MAGIC %pip install xformers

# COMMAND ----------

import asyncio

import nest_asyncio
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

# COMMAND ----------

from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

# COMMAND ----------

from huggingface_hub import notebook_login
notebook_login()

# COMMAND ----------

SLACK_APP_TOKEN = dbutils.secrets.get("hippo", "SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = dbutils.secrets.get("hippo", "SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = dbutils.secrets.get("hippo", "SLACK_SIGNING_SECRET")

# COMMAND ----------

model = "meta-llama/Llama-2-7b-chat-hf"
revision = "0ede8dd71e923db6258295621d817ca8714516d4"

# COMMAND ----------

tokenizer = AutoTokenizer.from_pretrained(model, padding_side="left")
pipe = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    revision=revision,
    return_full_text=False
)

pipe.tokenizer.pad_token_id = tokenizer.eos_token_id

# COMMAND ----------

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

PROMPT_FOR_GENERATION_FORMAT = """
<s>[INST]<<SYS>>
{system_prompt}
<</SYS>>

{instruction}
[/INST]
""".format(
    system_prompt=DEFAULT_SYSTEM_PROMPT,
    instruction="{instruction}"
)

def gen_text(prompt: str, use_template=False, **kwargs):
    if use_template:
        full_prompt = PROMPT_FOR_GENERATION_FORMAT.format(instruction=prompt)
    else:
        full_prompt = prompt

    if "batch_size" not in kwargs:
        kwargs["batch_size"] = 1
    
    # the default max length is pretty small (20), which would cut the generated output in the middle, so it's necessary to increase the threshold to the complete response
    if "max_new_tokens" not in kwargs:
        kwargs["max_new_tokens"] = 512

    # configure other text generation arguments, see common configurable args here: https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
    kwargs.update(
        {
            # Hugging Face sets pad_token_id to eos_token_id by default
            # setting here to not see redundant message
            "pad_token_id": tokenizer.eos_token_id,
            "eos_token_id": tokenizer.eos_token_id,
        }
    )

    outputs = pipe([full_prompt], **kwargs)
    outputs = [out[0]["generated_text"] for out in outputs]

    return outputs[0]

# COMMAND ----------


async def init_slack_bot(bot_token: str, signing_secret: str, app_token: str):
    app = AsyncApp(token=bot_token, signing_secret=signing_secret)

    @app.command("/echo")
    async def repeat_text(ack, respond, command):
        # Acknowledge command request
        await ack()
        await respond(f"{command['text']}")

    @app.event("message")
    async def event_im_message(event, say):
        prompt = ' '.join(event['text'].split())
        print(f'New Prompt: {prompt}')
        response = gen_text(prompt, max_new_tokens=512)
        await say(response)

    handler = AsyncSocketModeHandler(app=app, app_token=app_token)
    await handler.start_async()

# COMMAND ----------

nest_asyncio.apply()

# COMMAND ----------

asyncio.run(init_slack_bot(SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, SLACK_APP_TOKEN))

# COMMAND ----------


