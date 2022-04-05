mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: build run test

update:
	go mod tidy

build:
	go build

run: build
	./backend

test:
	XWAY_BACKEND_CONFIG_FILE=$(mkfile_path)/test/config/config.yaml \
	cd $(mkfile_path)/test && go test -v
