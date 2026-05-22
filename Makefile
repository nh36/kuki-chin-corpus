# Kuki-Chin Corpus Build System
# ==============================

PYTHON := python3
TSV_DIR := data/ctd_analysis
DB_PATH := data/ctd_backend.db

# Expected counts for sanity check
EXPECTED_SOURCES := 30000
EXPECTED_TOKENS := 830000
EXPECTED_LEMMAS := 7000

.PHONY: help backend backend-check clean-backend grammar-reports grammar-integration-report grammar-example-audit dictionary link-examples metrics test test-analyzer test-backend

help:
	@echo "Kuki-Chin Corpus Build Targets"
	@echo "=============================="
	@echo ""
	@echo "  make backend           - Rebuild Tedim SQLite backend from TSV exports"
	@echo "  make backend-check     - Verify backend counts are sane"
	@echo "  make link-examples     - Link examples to senses and generate corpus examples"
	@echo "  make clean-backend     - Remove generated database"
	@echo "  make grammar-reports   - Generate all grammar reports from backend"
	@echo "  make dictionary        - Generate dictionary outputs from backend"
	@echo "  make metrics           - Generate canonical Tedim metrics (JSON + Markdown)"
	@echo "  make test-analyzer     - Run the legacy analyzer test runner"
	@echo "  make test-backend      - Rebuild backend and run backend-native pytest tests"
	@echo "  make test              - Run analyzer runner, rebuild backend, then run full pytest suite"
	@echo "  make grammar-integration-report - Generate Tedim grammar source integration dashboard"
	@echo "  make grammar-example-audit - Generate Tedim backend example-selection audit"
	@echo ""

# Rebuild the SQLite backend from TSV exports
backend: clean-backend
	@echo "Rebuilding Tedim backend from $(TSV_DIR)..."
	$(PYTHON) scripts/backend.py migrate --tsv-dir $(TSV_DIR) --db $(DB_PATH)
	@echo ""
	@echo "Backend rebuilt. Run 'make backend-check' to verify."

# Verify backend counts look reasonable
backend-check:
	@echo "Checking backend integrity..."
	@$(PYTHON) scripts/check_backend.py --db $(DB_PATH)

# Link examples to senses and generate corpus examples
link-examples: backend-check
	@echo "Linking examples to senses..."
	$(PYTHON) scripts/link_examples_to_senses.py --generate --max-senses 10000

# Remove generated database
clean-backend:
	rm -f $(DB_PATH)

# Generate grammar reports from backend
grammar-reports: backend-check
	@echo "Generating grammar reports..."
	$(PYTHON) scripts/generate_tam_report_backend.py --output output/grammar/tam_report.md
	$(PYTHON) scripts/generate_case_report_backend.py --output output/grammar/case_marking_report.md
	$(PYTHON) scripts/generate_grammar_from_backend.py --output output/grammar/grammar_constructions.md
	$(PYTHON) scripts/generate_grammar_from_backend.py --full --output output/grammar/grammar_full.md
	$(PYTHON) scripts/generate_grammar_integration_report.py --db $(DB_PATH) --output output/grammar_integration_report.md
	$(PYTHON) scripts/generate_example_selection_audit.py --db $(DB_PATH) --output output/grammar/example_selection_audit.md
	@echo "Grammar reports generated in output/grammar/"

# Generate grammar integration report from Tedim source map
grammar-integration-report: backend-check
	@echo "Generating Tedim grammar integration report..."
	$(PYTHON) scripts/generate_grammar_integration_report.py --db $(DB_PATH) --output output/grammar_integration_report.md
	@echo "Integration report written to output/grammar_integration_report.md"

# Generate backend example-selection audit
grammar-example-audit: backend-check
	@echo "Generating Tedim backend example-selection audit..."
	$(PYTHON) scripts/generate_example_selection_audit.py --db $(DB_PATH) --output output/grammar/example_selection_audit.md
	@echo "Example-selection audit written to output/grammar/example_selection_audit.md"

# Generate dictionary outputs from backend  
dictionary: backend-check
	@echo "Generating sample dictionary entries..."
	$(PYTHON) scripts/generate_sample_entries_backend.py --pos V --limit 50 --output output/dictionary/sample_entries_verbs.md
	$(PYTHON) scripts/generate_sample_entries_backend.py --pos N --limit 50 --output output/dictionary/sample_entries_nouns.md
	$(PYTHON) scripts/generate_sample_entries_backend.py --type grammatical --limit 30 --output output/dictionary/sample_entries_grammatical.md
	@echo "Dictionary outputs generated in output/dictionary/"

# Generate canonical Tedim metrics
metrics: backend-check
	@echo "Generating canonical Tedim metrics..."
	$(PYTHON) scripts/generate_metrics.py --db $(DB_PATH)
	@echo "Metrics written to output/metrics/"

# Run the legacy analyzer runner
test-analyzer:
	@echo "Running legacy analyzer test runner..."
	$(PYTHON) tests/run_all_tests.py -v

# Rebuild backend, then run backend-native pytest tests
test-backend:
	@$(MAKE) backend
	@echo "Running backend-native pytest suite..."
	$(PYTHON) -m pytest tests/test_backend.py -v --tb=short

# Standard repository test workflow
test:
	@$(MAKE) test-analyzer
	@$(MAKE) backend
	@echo "Running full pytest suite..."
	$(PYTHON) -m pytest tests/ -v --tb=short
