install-metal:
	pip uninstall llama-cpp-python -y
	CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install -U llama-cpp-python --no-cache-dir
