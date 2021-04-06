
# all:

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

stop:

restart:
	$(MAKE) start
	$(MAKE) stop

test:
	echo "TODO"
