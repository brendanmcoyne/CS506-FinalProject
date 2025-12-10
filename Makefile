# Makefile for MLB Payroll Project

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default target
all: setup run test

# Create virtual environment and install dependencies
setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run the analysis notebook (convert to .py then run)
run:
	jupyter nbconvert --to python Graphs.ipynb --execute --output Graphs.py

# Run test suite
test:
	$(PYTHON) test_model.py

# Clean generated files
clean:
	rm -rf $(VENV)
	rm -f Graphs.py
	rm -f *.pyc __pycache__
