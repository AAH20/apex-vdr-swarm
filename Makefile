.PHONY: test bench clean build install run

test:
	python3 -m unittest discover -s tests -v

bench:
	python3 benchmarks/bench_solvers_latency.py

clean:
	rm -rf build dist *.egg-info .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

build: clean
	python3 -m pip install --upgrade build
	python3 -m build

install:
	python3 -m pip install -e .

run:
	python3 -m apex_vdr_swarm.cli
