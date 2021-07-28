
COMMENT = $(m)
VALUE := $(if $(n),$(n),head)
FROMREV := 0
TOREV := 0001

PYTHON ?= python3
PIP ?= pip3
test ?= tests

.PHONY: prepare
prepare: prepare-ubuntu prepare-postgresql

.PHONY: prepare-ubuntu
prepare-ubuntu:
	sudo apt-get update
	apt install postgresql

.PHONY: prepare-postgresql
prepare-postgresql:
	pg_ctlcluster 12 main start
	cd /tmp; sudo -u postgres psql -c "alter user postgres with password 'postgres'"

.PHONY: prepare-centos
prepare-centos:
	sudo yum install python3-devel

freeze:
	$(PIP) freeze > requirements.txt

.PHONY: pip-install
pip-install:
	$(PIP) install -r requirements.txt

.PHONY: start
start: local
	# pg_ctlcluster 12 main start
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
	cd src; $(PYTHON) -m pytest -s $(test)

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

gen-upgrade-sql:
	cd src; alembic upgrade $(FROMREV):$(TOREV) --sql

gen-downgrade-sql:
	cd src; alembic downgrade $(FROMREV):$(TOREV) --sql

gen-init-sql:
	cd src; alembic upgrade base:head --sql

gen-uninit-sql:
	cd src; alembic head:base downgrade --sql

.PHONY: history
history:
	cd src; alembic history --verbose

.PHONY: base
base:
	cd src; alembic downgrade base

.PHONY: psql
psql:
	cd /tmp; sudo -u postgres psql -U postgres -d xway
	# psql -h 127.0.0.1 -p 5432 -U postgres -d xway

local:
	@for lang in `ls src/locales`; do \
		if [ ! -f src/locales/$$lang/LC_MESSAGES/base.mo ]; then \
			sed s/charset=CHARSET/charset=UTF-8/ -i src/locales/$$lang/LC_MESSAGES/base.po; \
			msgfmt -o src/locales/$$lang/LC_MESSAGES/base.mo src/locales/$$lang/LC_MESSAGES/base.po; \
		fi; \
		find src/ -iname "*.py" | xargs xgettext --from-code utf-8 -o src/locales/$$lang/LC_MESSAGES/new_base.pot; \
		sed s/charset=CHARSET/charset=UTF-8/ -i src/locales/$$lang/LC_MESSAGES/new_base.pot; \
		msgmerge -U src/locales/$$lang/LC_MESSAGES/base.po src/locales/$$lang/LC_MESSAGES/new_base.pot; \
		msgfmt -o src/locales/$$lang/LC_MESSAGES/base.mo src/locales/$$lang/LC_MESSAGES/base.po; \
		rm -f src/locales/$$lang/LC_MESSAGES/new_base.pot; \
	done
