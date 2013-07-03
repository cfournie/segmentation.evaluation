test:
	cd segeval
	nosetests
coverage:
	cd segeval
	nosetests --with-coverage --cover-package=segeval
coverage_html: coverage
	coverage html 
coveralls: coverage
	coveralls
build:
	python setup.py sdist --formats=gztar,zip
install:
	python setup.py install
upload:
	python setup.py sdist register upload
clean:
	find . -name '*.pyc' -delete
	rm -r dist build segeval.egg-info
