# Makefile for stackdio-server
#

.PHONY: all clean yarn_install build_ui pep8 pylint test tar wheel

all: build_ui pep8 pylint test tar wheel

clean:
	rm -rf dist/ build/ *.egg-info/ htmlcov/ tests.xml node_modules/ stackdio/ui/static/lib/ stackdio/ui/static/stackdio/build/

yarn_install:
	yarn install

build_ui: yarn_install
	python manage.py build_ui

pep8:
	pep8 stackdio

pylint:
	pylint stackdio

test:
	py.test --cov=stackdio --cov-report=html --junit-xml=tests.xml stackdio

tar: build_ui
	python setup.py sdist

wheel: build_ui
	python setup.py bdist_wheel
