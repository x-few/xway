
COMMENT = $(m)
VALUE := $(if $(n),$(n),head)

PYTHON ?= python3
PIP ?= pip3

.PHONY: prepare
prepare: prepare-ubuntu

.PHONY: prepare-ubuntu
prepare-ubuntu:
	sudo apt-get update
	apt install postgresql
	# sudo apt-get install python3-dev
	# pip3 install sanic

.PHONY: prepare-centos
prepare-centos:
	sudo yum install python3-devel

freeze:
	$(PIP) freeze > requirements.txt

.PHONY: pip-install
pip-install:
	$(PIP) install -r requirements.txt

.PHONY: start
start:
	pg_ctlcluster 12 main start
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
	$(eval NEXT_ID = $(shell ls src/db/alembic/versions/ | grep -P '^\d{4}-.*\.py$$' | wc -l))
	$(eval NEXT_ID = $(shell expr $(NEXT_ID) + 1))
	cd src; alembic revision -m "$(COMMENT)" --rev-id=`printf "%04d" $(NEXT_ID)`

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

local:
	# find src/ -iname "*.py" | xargs xgettext -o src/locales/zh_CN/LC_MESSAGES/base.po
	# find src/ -iname "*.py" | xargs xgettext -o src/locales/en_US/LC_MESSAGES/base.po
	sed s/charset=CHARSET/charset=UTF-8/ -i src/locales/zh_CN/LC_MESSAGES/base.po
	sed s/charset=CHARSET/charset=UTF-8/ -i src/locales/en_US/LC_MESSAGES/base.po
	msgfmt -o src/locales/zh_CN/LC_MESSAGES/base.mo src/locales/zh_CN/LC_MESSAGES/base.po
	msgfmt -o src/locales/en_US/LC_MESSAGES/base.mo src/locales/en_US/LC_MESSAGES/base.po

tr-merge:
	for lang in `ls src/locales`; do \
		find src/ -iname "*.py" | xargs xgettext --from-code utf-8 -o src/locales/$$lang/LC_MESSAGES/new_base.pot; \
		sed s/charset=CHARSET/charset=UTF-8/ -i src/locales/$$lang/LC_MESSAGES/new_base.pot; \
		msgmerge -U src/locales/$$lang/LC_MESSAGES/base.po src/locales/$$lang/LC_MESSAGES/new_base.pot; \
		msgfmt -o src/locales/$$lang/LC_MESSAGES/base.mo src/locales/$$lang/LC_MESSAGES/base.po; \
		rm -f src/locales/$$lang/LC_MESSAGES/new_base.pot; \
	done
