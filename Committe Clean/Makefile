ENV_NAME := $(shell cat environment.yml | grep '^name:' | awk '{print $$2}')
SHELL := /bin/bash


.PHONY: data-pull env env-rm env-rmk

data-pull:
	rm -rf "s3-data" && wget -i csv-data-files.txt -P s3-data

env:
	conda env create -f environment.yml || conda env update -f environment.yml

env-rm:
	conda remove --name $(ENV_NAME) --all -y

env-rmk: env-rm env
