test:
	python -m unittest discover -s . -p '*est.py'
coverage:
	coverage run -m unittest discover -s . -p '*est.py'
coverage_report:coverage
	coverage report -m
coverage_html: coverage
	coverage html 
coveralls: coverage_report
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
