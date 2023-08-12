FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y software-properties-common curl && \
    apt-get update && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.11 python-is-python3

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /app
COPY . /app

WORKDIR /app
RUN poetry install
