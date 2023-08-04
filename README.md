# synaptiq-melvil
The truth-aware document manager

## Dependencies:

docker: https://www.docker.com/products/docker-desktop/
kind: https://kind.sigs.k8s.io
ctlptl: https://github.com/tilt-dev/ctlptl
tilt: https://tilt.dev

## Getting started

Install docker, kind, ctlptl and tilt (see above)

```sh
make clean-tilt

```

# What's here:

## ui

Next.js user interface for all the things

## cp

Postgres + hasura control plane database and api


## index

TBD embedding index

## archive

FoundationDB kv/store for metadata + object storage interface.

## crawler

TBD agent-powered content finder

## llm

TBD online fine-tuned language model (powering chatbae + index)

## sojourner

TBD browser extension

## chatbae

Slack interface
