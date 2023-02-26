.ONESHELL:
	SHELL:=/bin/bash

VENV := ./.venv
POETRY := $(VENV)/Scripts/poetry

default:
	@echo "Call a specific subcommand: create-env, install-poetry, install, update"

clean:
	rm -r -f $(VENV)

all:
	$(MAKE) -s install

$(POETRY): 
	$(MAKE) -s $(VENV)
	. $(VENV)/Scripts/activate
	pip install poetry
	deactivate

$(VENV):
	python -m venv $(VENV)

.PHONY : create-env
create-env: 
	@$(MAKE) -s $(VENV)

.PHONY : install-poetry
install-poetry:
	@$(MAKE) -s $(POETRY)

.PHONY : install
install : poetry.lock
	$(MAKE) -s $(VENV)
	$(MAKE) -s $(POETRY)
	. $(VENV)/Scripts/activate
	$(POETRY) install
	deactivate

.PHONY : update
update: 
	$(MAKE) -s install
	. $(VENV)/Scripts/activate
	$(POETRY) update
	deactivate
