# Variables
VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Scripts:
repositories_refactors_script: $(VENV)
	clear; time $(PYTHON) repository_refactors.py

metrics_evolution_refactors_script: $(VENV)
	clear; time $(PYTHON) metrics_evolution_refactors.py

# Setup Virtual Environment and Install Dependencies
$(VENV): dependencies

dependencies:
	python3 -m venv $(VENV)
	$(PIP) install colorama pandas pydriller scikit-learn tqdm

# Utility rule for cleaning the project
clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: clean repositories_refactors_script metrics_evolution_refactors_script dependencies
