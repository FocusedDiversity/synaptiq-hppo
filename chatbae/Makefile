start:
	poetry run python -m chatbae.main

docker:
	docker build -t chatbae . && docker run -ti --rm --runtime=nvidia --gpus all -v $(pwd):/app chatbae:latest poetry run pytest
