# Variables
VENV := $(CURDIR)/venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Activate the virtual environment: source venv/bin/activate

# Main Scripts:
code_metrics_script: $(VENV)
	clear; time $(PYTHON) ./code_metrics.py

metrics_changes_script: $(VENV)
	clear; time $(PYTHON) ./metrics_changes.py

repositories_picker_script: $(VENV)
	clear; time $(PYTHON) ./repositories_picker.py

repositories_attributes_analyzer_script: $(VENV)
	clear; time $(PYTHON) ./repositories_attributes_analyzer.py

repositories_picker_to_code_metrics: $(VENV)
	$(MAKE) repositories_picker_script
	$(MAKE) code_metrics_script

code_metrics_to_repositories_attributes_analyzer: $(VENV)
	$(MAKE) code_metrics_script
	$(MAKE) metrics_changes_script
	$(MAKE) repositories_attributes_analyzer_script

metrics_changes_to_repositories_attributes_analyzer: $(VENV)
	$(MAKE) metrics_changes_script
	$(MAKE) repositories_attributes_analyzer_script

# Define the main target that runs the scripts in the specified order and waits for the previous one to finish before starting the next one
all: repositories_picker_script code_metrics_script metrics_changes_script repositories_attributes_analyzer_script

# Auxiliary Scripts:
empty_folders_script: $(VENV)
	clear; time $(PYTHON) ./Scripts/empty_folders.py

extract_zip_files_script: $(VENV)
	chmod +x ./Scripts/extract_zip_files.sh; clear; time ./Scripts/extract_zip_files.sh

generate_short_zip_files_script: $(VENV)
	chmod +x ./Scripts/generate_short_zip_files.sh; clear; time ./Scripts/generate_short_zip_files.sh

generate_zip_files_script: $(VENV)
	chmod +x ./Scripts/generate_zip_files.sh; clear; time ./Scripts/generate_zip_files.sh

move_extracted_files_script: $(VENV)
	chmod +x ./Scripts/move_extracted_files.sh; clear; time ./Scripts/move_extracted_files.sh

track_files_script: $(VENV)
	clear; time $(PYTHON) ./Scripts/track_files.py

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

.PHONY: clean code_metrics_script metrics_changes_script empty_folders_script extract_zip_files_script generate_short_zip_files_script generate_zip_files_script move_extracted_files_script repositories_picker_script track_files_script dependencies generate_requirements repositories_picker_to_code_metrics code_metrics_to_repositories_attributes_analyzer metrics_changes_to_repositories_attributes_analyzer
