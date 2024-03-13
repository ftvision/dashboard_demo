# Create a Python virtual environment
.venv:
	python3 -m venv .venv

# Activate the virtual environment
activate:
	. .venv/bin/activate


# Clean up the virtual environment
clean:
	rm -rf .venv*

set_py_path:
	export PYTHONPATH=$PWD

# Install dependencies from requirements.txt
install-gradio: clean .venv set_py_path
	$(MAKE) activate
	pip install -r gradio-requirements.txt

# Install dependencies from requirements.txt
install-streamlit: clean .venv set_py_path
	$(MAKE) activate
	pip install -r streamlit-requirements.txt

# Install dependencies from requirements.txt
install-reflex: clean .venv set_py_path
	$(MAKE) activate
	pip install -r reflex-requirements.txt

install-taipy: clean .venv set_py_path
	$(MAKE) activate
	pip install -r taipy-requirements.txt


