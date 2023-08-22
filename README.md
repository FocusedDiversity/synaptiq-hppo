# synaptiq-melvil
The truth-aware document manager

## Dependencies:
* docker: https://www.docker.com/products/docker-desktop/
* kind: https://kind.sigs.k8s.io
* ctlptl: https://github.com/tilt-dev/ctlptl
* tilt: https://tilt.dev

## Getting started
Install docker, kind, ctlptl and tilt (see above)
```sh
make clean-tilt
```

# What's here:
## axiom
Fact checking browser extension

## archive
FoundationDB kv/store for metadata + object storage interface.

## chatbae
Slack interface

## cp
Postgres + hasura control plane database and api

## crawler
TBD agent-powered content finder

## infrastructure
Shared infrastructure services (databases, storage, queues, etc)

## index
TBD embedding index

## llm
TBD online fine-tuned language model (powering chatbae + index)

## ui
Next.js user interface for all the things