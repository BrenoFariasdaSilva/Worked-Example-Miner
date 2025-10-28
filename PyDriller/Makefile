# Variables
VENV := $(CURDIR)/venv
OS := $(shell uname 2>/dev/null || echo Windows)

# Detect correct Python and Pip commands for venv
ifeq ($(OS), Windows)
	PYTHON := $(VENV)/Scripts/python.exe
	PIP := $(VENV)/Scripts/pip.exe
	CLEAR_CMD := cls
	TIME_CMD :=
else
	PYTHON := $(VENV)/bin/python3
	PIP := $(VENV)/bin/pip
	CLEAR_CMD := clear
	TIME_CMD := time
endif

# Main Scripts
code_metrics_script: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./code_metrics.py

metrics_changes_script: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./metrics_changes.py

repositories_picker_script: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./repositories_picker.py

repositories_attributes_analyzer_script: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./repositories_attributes_analyzer.py

# Compound targets
repositories_picker_to_code_metrics: $(VENV)
	$(MAKE) repositories_picker_script
	$(MAKE) code_metrics_script

repositories_picker_to_metrics_changes: $(VENV)
	$(MAKE) repositories_picker_script
	$(MAKE) code_metrics_script
	$(MAKE) metrics_changes_script

code_metrics_to_metrics_changes: $(VENV)
	$(MAKE) code_metrics_script
	$(MAKE) metrics_changes_script

code_metrics_to_repositories_attributes_analyzer: $(VENV)
	$(MAKE) code_metrics_script
	$(MAKE) metrics_changes_script
	$(MAKE) repositories_attributes_analyzer_script

metrics_changes_to_repositories_attributes_analyzer: $(VENV)
	$(MAKE) metrics_changes_script
	$(MAKE) repositories_attributes_analyzer_script

# Main target
all: repositories_picker_script code_metrics_script metrics_changes_script repositories_attributes_analyzer_script

# Auxiliary Scripts
empty_folders_script: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./Scripts/empty_folders.py

extract_zip_files_script: $(VENV)
	chmod +x ./Scripts/extract_zip_files.sh; $(CLEAR_CMD); $(TIME_CMD) ./Scripts/extract_zip_files.sh

generate_short_zip_files_script: $(VENV)
	chmod +x ./Scripts/generate_short_zip_files.sh; $(CLEAR_CMD); $(TIME_CMD) ./Scripts/generate_short_zip_files.sh

generate_zip_files_script: $(VENV)
	chmod +x ./Scripts/generate_zip_files.sh; $(CLEAR_CMD); $(TIME_CMD) ./Scripts/generate_zip_files.sh

move_extracted_files_script: $(VENV)
	chmod +x ./Scripts/move_extracted_files.sh; $(CLEAR_CMD); $(TIME_CMD) ./Scripts/move_extracted_files.sh

track_files_script: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./Scripts/track_files.py

batch_processing: $(VENV)
	# Recommended for low-performance machines
	while true; do \
		echo "Running $$i repo"; \
		$(MAKE) code_metrics_script < /dev/null; \
		$(MAKE) metrics_changes_script < /dev/null; \
	done

# Setup Virtual Environment and Install Dependencies
$(VENV): dependencies

dependencies:
	cd .. && git submodule update --init --recursive
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Generate requirements.txt from the current venv
generate_requirements:
	$(PIP) freeze > requirements.txt

# Utility rule for cleaning the project
clean:
	rm -rf $(VENV) || rmdir /S /Q $(VENV) 2>nul
	find . -type f -name '*.pyc' -delete || del /S /Q *.pyc 2>nul
	find . -type d -name '__pycache__' -delete || rmdir /S /Q __pycache__ 2>nul

.PHONY: clean code_metrics_script metrics_changes_script empty_folders_script extract_zip_files_script generate_short_zip_files_script generate_zip_files_script move_extracted_files_script repositories_picker_script track_files_script dependencies generate_requirements repositories_picker_to_code_metrics code_metrics_to_repositories_attributes_analyzer metrics_changes_to_repositories_attributes_analyzer
