# Variables
VENV := $(CURDIR)/venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Activate the virtual environment: source venv/bin/activate

# Main Scripts:
gemini_script: $(VENV)
	clear; time $(PYTHON) ./gemini.py

# Setup Virtual Environment and Install Dependencies
$(VENV): dependencies

# Install the project dependencies in a virtual environment
dependencies:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Generate requirements.txt from the current venv
generate_requirements:
	$(PIP) freeze > requirements.txt

# Utility rule for cleaning the project
clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: gemini_script clean dependencies generate_requirements
