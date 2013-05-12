test:
	python -m unittest discover -s . -p '*est.py'
coverage:
	coverage run -m unittest discover -s . -p '*est.py'
	coverage report -m
coverage_html: coverage
	coverage html 
build:
	python setup.py sdist --formats=gztar,zip
install:
	python setup.py install
upload:
	python setup.py sdist upload --formats=gztar,zip
clean:
	find . -name '*.pyc' -delete
	rm -r dist build segeval.egg-info
