DOCKER := docker

IMAGE_NAME := hot_summer
IMAGE_NAMESPACE := chuhsuanlee
IMAGE_VERSION := 0.1.0
IMAGE_REPO := $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)

USERNAME := $(shell id -u -n)
WORKDIR := $(shell pwd)
REPORT_PATH := $(WORKDIR)/src/reports
FLAG := \
	-v /etc/localtime:/etc/localtime \
	-v $(REPORT_PATH):/usr/src/app/reports

# Followings are the Make commands that can be used.

.PHONY: help
help:
	@echo "Usage:"
	@echo "    make <target>"
	@echo
	@echo "Targets:"
	@echo "    build"
	@echo "        Build docker image."
	@echo
	@echo "    clean"
	@echo "        Remove docker image."
	@echo
	@echo "    exec (CMD=<cmd>)"
	@echo "        Create container and execute specified command (default: bash)."
	@echo
	@echo "    run"
	@echo "        Create container and perform task."
	@echo

.PHONY: build
build:
	$(DOCKER) build \
		--build-arg USERNAME=$(USERNAME) \
		-t $(IMAGE_REPO) \
		.

.PHONY: clean
clean:
	$(DOCKER) rmi $(IMAGE_REPO) || true

.PHONY: exec
exec: build
	$(eval CMD ?= bash)
	$(DOCKER) run \
		--rm -it ${FLAG} \
		--network="host" \
		--entrypoint $(CMD) \
		$(IMAGE_REPO)

.PHONY: run
run: build
	$(DOCKER) run \
		--rm ${FLAG} \
		--network="host" \
		$(IMAGE_REPO)
