
COMMENT = $(m)
VALUE := $(if $(n),$(n),head)

PYTHON ?= python3.7
PIP ?= pip3

.PHONY: prepare
prepare: prepare-ubuntu

.PHONY: prepare-ubuntu
prepare-ubuntu:
	sudo apt-get update
	sudo apt-get install python3-dev
	pip3 install sanic

.PHONY: prepare-centos
prepare-centos:
	sudo yum install python3-devel

freeze:
	$(PIP) freeze > requirements.txt

.PHONY: pip-install
pip-install:
	$(PIP) install -r requirement.txt

.PHONY: start
start:
	# cd src; sanic xway.app
	# cd src; uvicorn xway:app --reload
	cd src; $(PYTHON) xway.py

.PHONY: run
run: start

.PHONY: stop
stop:

.PHONY: restart
restart:
	$(MAKE) start
	$(MAKE) stop

.PHONY: test
test:
	cd src; $(PYTHON) -m pytest tests -s

.PHONY: revision
# make revision m="comment"
revision:
	cd src; alembic revision -m "$(COMMENT)"

.PHONY: upgrade
# make upgrade n=1
upgrade:
	cd src; alembic upgrade $(VALUE)

.PHONY: downgrade
# make downgrade n=2
downgrade:
	cd src; alembic downgrade -$(VALUE)

.PHONY: history
history:
	cd src; alembic history --verbose

.PHONY: base
base:
	cd src; alembic downgrade base

.PHONY: psql
psql:
	psql -h 127.0.0.1 -p 5432 -U postgres -d xway
