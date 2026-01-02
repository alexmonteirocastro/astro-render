.PHONY: help install test demo example

PYTHON ?= python
PIP ?= pip
PYTEST ?= pytest
STREAMLIT ?= streamlit

help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make demo       Run Streamlit demo app"
	@echo "  make clean      Remove __pycache__ and pytest cache"

install:
	$(PIP) install -r requirements.txt

demo:
	PYTHONPATH=. $(STREAMLIT) run demo.py

clean:
	@echo "Cleaning __pycache__ and pytest cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache

