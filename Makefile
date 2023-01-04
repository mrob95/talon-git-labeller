clean:
	rm -rf dist build

dist: clean
	python setup.py sdist bdist_wheel

package: dist
	twine upload dist/*
