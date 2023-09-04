# Databricks notebook source
from huggingface_hub import notebook_login

# COMMAND ----------

notebook_login()

# COMMAND ----------

!echo ~

# COMMAND ----------

!cat /root/.cache/huggingface/token

# COMMAND ----------

from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

# COMMAND ----------

model = "meta-llama/Llama-2-7b-chat-hf"
revision = "0ede8dd71e923db6258295621d817ca8714516d4"

# COMMAND ----------

tokenizer = AutoTokenizer.from_pretrained(model, padding_side="left")

# COMMAND ----------

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    revision=revision,
    return_full_text=False
)

# COMMAND ----------

pipeline.tokenizer.pad_token_id = tokenizer.eos_token_id

# COMMAND ----------

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

INTRO_BLURB = "Below is an instruction that describes a task. Write a response that appropriately completes the request."
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

# COMMAND ----------

pipeline('hello')

# COMMAND ----------


