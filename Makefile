setup:
	python3 -m venv ~/.tldr-venv

install:
	pip3 install --upgrade pip &&\
		pip3 install -r requirements.txt

lint:
	black *.py

all: setup install lint