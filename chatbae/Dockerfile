FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y software-properties-common curl && \
    apt-get update &&  \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.11  

RUN curl -sSL https://install.python-poetry.org | python3.11 -

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /app

WORKDIR /app
COPY pyproject.toml poetry.lock README.md /app/
RUN mkdir /app/chatbae && touch /app/chatbae/__init__.py
RUN poetry install
COPY . /app/
COPY .env /app/.env
