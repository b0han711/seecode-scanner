DOC_DIR = docs
SRC_DIR = seecode_scanner
MAKE = make
PY_VERSION=`python -c "import sys; v = sys.version_info; sys.stdout.write('py%d%d' % (v[0], v[1]))"`
.PHONY: clean html test unit func lint lintall

all:
	make test
	make html
	make clean

install:
	@pip install -r requirements/dev.txt

lint:
	prospector $(SRC_DIR) --strictness veryhigh

test:
	make unit
	make func

unit:
	export PYTHONPATH=$(SRC_DIR) && nosetests -x -v --nocapture \
	--with-coverage --cover-erase --cover-package=$(SRC_DIR) \
	tests/unit/core/* \
	tests/unit/engines/entity/* \
	tests/unit/engines/* \
	tests/unit/utils/*

func:
	export PYTHONPATH=$(SRC_DIR) && nosetests -x -v --nocapture \
	--logging-config tests/functional/log.conf \
	tests/functional/controller/*


clean:
	rm -rf *.egg-info dist
	find $(SRC_DIR) tests -type f -name '*.pyc' -delete
