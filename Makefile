# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
STREAMLIT = $(VENV)/bin/streamlit

# Detect OS for cross-platform compatibility
ifeq ($(OS),Windows_NT)
    PYTHON = $(VENV)\Scripts\python.exe
    PIP = $(VENV)\Scripts\pip.exe
    STREAMLIT = $(VENV)\Scripts\streamlit.exe
endif

.PHONY: all setup run clean

# Default target
all: setup run

# Create virtual environment and install requirements
setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate

# Run the Streamlit application
run:
	$(STREAMLIT) run main.py

# Clean up the environment
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
