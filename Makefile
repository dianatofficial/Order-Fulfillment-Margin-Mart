.PHONY: help install generate-data build-mart test run-ui pipeline clean

help:
	@echo "Available commands:"
	@echo "  make install        Install Python dependencies"
	@echo "  make generate-data  Generate synthetic raw operational dataset"
	@echo "  make build-mart     Execute DuckDB Kimball ELT transformations"
	@echo "  make test           Execute automated test suite"
	@echo "  make run-ui         Launch Streamlit interactive analytics app"
	@echo "  make pipeline       Run full pipeline (generate -> transform -> test)"
	@echo "  make clean          Clean temporary files and caches"

install:
	pip install -r requirements.txt

generate-data:
	python run_pipeline.py --generate-data

build-mart:
	python run_pipeline.py --build-mart

test:
	python run_pipeline.py --run-tests

run-ui:
	streamlit run app.py

pipeline:
	python run_pipeline.py --full-pipeline

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache
