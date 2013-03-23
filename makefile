test:
	python -m unittest segeval
build:
	python setup.py sdist --formats=gztar,zip
install:
	python setup.py install
upload:
	python setup.py sdist upload --formats=gztar,zip
clean:
	rm -r dist build segeval.egg-info