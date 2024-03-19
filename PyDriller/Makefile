# Variables
VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Main Scripts:
code_metrics_script: $(VENV)
	clear; time $(PYTHON) code_metrics.py

metrics_changes_script: $(VENV)
	clear; time $(PYTHON) metrics_changes.py

# Auxiliar Scripts:
empty_folders_script: $(VENV)
	clear; time $(PYTHON) Scripts/empty_folders.py

extractZipFiles: $(VENV)
	chmod +x Scripts/extractZipFiles.sh; clear; time ./Scripts/extractZipFiles.sh

generateZipFiles: $(VENV)
	chmod +x Scripts/generateZipFiles.sh; clear; time ./Scripts/generateZipFiles.sh

moveExtractedFiles: $(VENV)
	chmod +x Scripts/moveExtractedFiles.sh; clear; time ./Scripts/moveExtractedFiles.sh

track_files_script: $(VENV)
	clear; time $(PYTHON) Scripts/track_files.py

# Setup Virtual Environment and Install Dependencies
$(VENV): dependencies

dependencies:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Generate requirements.txt from the current venv
generate-requirements:
	$(PIP) freeze > requirements.txt

# Utility rule for cleaning the project
clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: clean code_metrics_script metrics_changes_script empty_folders_script extractZipFiles generateZipFiles moveExtractedFiles track_files_script dependencies generate-requirements
