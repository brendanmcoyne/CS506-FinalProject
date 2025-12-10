# Makefile for MLB Payroll Project

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
JUPYTER = $(VENV)/bin/jupyter

all: setup run test

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(JUPYTER) nbconvert --to python Graphs.ipynb --execute --output Graphs.py

test:
	$(PYTHON) test_model.py

clean:
	rm -rf $(VENV)
	rm -f Graphs.py
	rm -rf __pycache__
	rm -f *.pyc
