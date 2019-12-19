all: install

install:
	@if [[ -d "python-json-benchmark" ]]; then \
		cd python-json-benchmark; \
		git pull; \
	else \
		git clone https://github.com/akrylysov/python-json-benchmark; \
	fi
	pipenv install

uninstall:
	rm -rf python-json-benchmark
	pipenv --rm

run:
	@echo ------------------------------------
	@echo "Running benchmark 1"
	@echo ------------------------------------
	@cd python-json-benchmark && pipenv run python benchmark.py
	@echo ------------------------------------
	@echo "Running benchmark 2"
	@echo ------------------------------------
	@pipenv run python benchmark2.py
