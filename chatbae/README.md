# ChatBae

On an apple silicon mac with osx 13:

## Install python stuff

```sh
pyenv install 3.11.2
poetry env use python
poetry install
```

Note that currently mlc is published as nightlies and
they are deleting the old ones pretty rapidly, so it may be
necessary to manually update the revision in pyproject.toml.

In some cases, "poetry lock" will be enough to figure it out.

Good luck if they change the API!

## Download model and weights

Refer to https://mlc.ai/mlc-llm/docs/get_started/try_out.html.
Always download the libs and the 7b (smallest) model so tests run. You
will need a 64gb+ machine to run the 70b model.

```shell
git submodule update --init -- dist/prebuilt/lib
git submodule update --init -- dist/prebuilt/mlc-chat-Llama-2-7b-chat-hf-q4f16_1
# or 
git submodule update --init -- dist/prebuilt/mlc-chat-Llama-2-13b-chat-hf-q4f16_1
#of 
git submodule update --init -- dist/prebuilt/mlc-chat-Llama-2-70b-chat-hf-q4f16_1
```

## Set up your app tokens
```shell
cat > .env <<-EOF
SLACK_APP_TOKEN="<APP TOKEN from Slack App>"
SLACK_BOT_TOKEN="<BOT TOKEN from Slack App>"
SLACK_SIGNING_SECRET="<SIGNING SECRET from Slack App>"
EOF
```

## Start the server

```sh
poetry run python -m chatbae.main
```
