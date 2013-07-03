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
install_requirements:
	pip install -r requirements.txt --use-mirrors
install:
	python setup.py install
upload:
	python setup.py sdist register upload
clean:
	find . -name '*.pyc' -delete
	rm -r dist build segeval.egg-info
style:
	flake8 --config=setup.cfg segeval
