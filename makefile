test:
	python -m unittest discover -s . -p '*est.py'
coverage:
	cd segeval
	nosetests --with-coverage --cover-package=segeval
coverage_html: coverage
	coverage html 
coveralls: coverage
	coveralls --verbose
build:
	python setup.py sdist --formats=gztar,zip
install:
	python setup.py install
upload:
	python setup.py sdist register upload
clean:
	find . -name '*.pyc' -delete
	rm -r dist build segeval.egg-info
