.PHONY: venv test-run outputs
venv:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
test-run:
	python -m scraper.main --once
outputs:
	@echo "See ./_exports/`date +%F` for results"
