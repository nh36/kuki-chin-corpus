# Kuki-Chin Corpus Build System
# ==============================

PYTHON := python3
TSV_DIR := data/ctd_analysis
DB_PATH := data/ctd_backend.db

# Expected counts for sanity check
EXPECTED_SOURCES := 30000
EXPECTED_TOKENS := 830000
EXPECTED_LEMMAS := 7000

.PHONY: help backend backend-check clean-backend grammar-reports dictionary link-examples metrics metrics-check editorial-dashboard dictionary-draft

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
	@echo "  make metrics-check     - Verify README/PROGRESS metrics match canonical"
	@echo "  make editorial-dashboard - Generate editorial priorities report"
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
	@echo "Grammar reports generated in output/grammar/"

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

# Verify README/PROGRESS metrics match canonical
metrics-check: metrics
	@echo "Checking for metric drift..."
	@$(PYTHON) scripts/check_metrics.py --db $(DB_PATH)

# Generate editorial dashboard showing priorities for dictionary/grammar work
editorial-dashboard: backend-check
	@echo "Generating editorial dashboard..."
	$(PYTHON) scripts/generate_editorial_dashboard.py --db $(DB_PATH)
	@echo "Dashboard written to output/editorial_dashboard.md"

# Generate complete draft dictionary
dictionary-draft: backend-check
	@echo "Generating draft dictionary..."
	$(PYTHON) scripts/generate_dictionary_draft.py --db $(DB_PATH)
	@echo "Draft written to output/dictionary/draft_dictionary.md"

# Generate chaptered grammar draft
grammar-draft: backend-check
	@echo "Generating draft grammar..."
	$(PYTHON) scripts/generate_grammar_draft.py --db $(DB_PATH)
	@echo "Draft written to output/grammar/draft_grammar.md"

# Generate publication dashboard (metrics + readiness + blockers)
publication-dashboard: metrics editorial-dashboard dictionary-draft grammar-draft
	@echo "Generating publication dashboard..."
	$(PYTHON) scripts/generate_publication_dashboard.py --db $(DB_PATH)
	@echo "Dashboard written to output/publication_dashboard.md"
