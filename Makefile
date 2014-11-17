PYTHON=`which python3`

all:
	@echo "make source - Create source package"
	@echo "make clean - Get rid of scratch and byte files"
	@echo "make test - Run tests"

source:
	$(PYTHON) setup.py sdist $(COMPILE)

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST
	find . -type f -name '*.py[cod]' -delete
	find . -type d -name '__pycache__' -delete

test:
	tox
	coverage html
