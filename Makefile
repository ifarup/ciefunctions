sdist:
	python3 setup.py sdist

pypi: sdist
	twine upload dist/*
