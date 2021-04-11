
COMMENT=$(m)
VALUE := $(if $(n),$(n),head)


.PHONY: prepare
prepare: prepare-ubuntu

prepare-ubuntu:
	sudo apt-get update
	sudo apt-get install python3-dev
	pip3 install sanic

prepare-centos:
	sudo yum install python3-devel

freeze:
	pip3 freeze > requirements.txt

pip-install:
	pip3 install -r requirement.txt

start:
	# cd src; sanic xway.app
	# cd src; uvicorn xway:app --reload
	cd src; python3.7 xway.py

run: start

stop:

restart:
	$(MAKE) start
	$(MAKE) stop

test:
	echo "TODO"


# make revision m="comment"
revision:
	cd src; alembic revision -m "$(COMMENT)"

# make upgrade n=1
upgrade:
	cd src; alembic upgrade $(VALUE)

# make downgrade n=2
downgrade:
	cd src; alembic downgrade -$(VALUE)

history:
	cd src; alembic history --verbose

base:
	cd src; alembic downgrade base
