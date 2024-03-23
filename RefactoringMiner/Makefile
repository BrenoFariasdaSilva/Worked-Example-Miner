# Variables
VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Scripts:
repositories_refactors_script: $(VENV)
	clear; time $(PYTHON) repositories_refactors.py

metrics_evolution_refactors_script: $(VENV)
	clear; time $(PYTHON) metrics_evolution_refactors.py

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

.PHONY: clean repositories_refactors_script metrics_evolution_refactors_script dependencies generate_requirements
