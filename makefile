.PHONY: build
build:
	@rm -rf src/dist src/*.egg-info
	@python3 src/setup.py sdist

.PHONY: publish
publish:
	@python3 -m twine upload --verbose src/dist/*