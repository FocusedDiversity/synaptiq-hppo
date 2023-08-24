start:
	poetry run python -m chatbae.main

docker-image:
	docker build -t chatbae . 

docker-pytest: docker-image
	docker run -ti --rm --runtime=nvidia --gpus all -v ${PWD}/dist:/app/dist chatbae:latest poetry run pytest

docker-shell: docker-image
	docker run -ti --rm --runtime=nvidia --gpus all -v ${PWD}/dist:/app/dist chatbae:latest /bin/bash 

docker-run: docker-image
	docker run -ti --rm --runtime=nvidia --gpus all -v ${PWD}/dist:/app/dist chatbae:latest poetry run python -m chatbae.main --device-name=cuda
