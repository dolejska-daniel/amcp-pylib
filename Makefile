
all: build

build:
	python3 setup.py sdist bdist_wheel

deploy: clean build
	twine upload dist/*

clean:
	rm -Rf *.egg-info build dist
