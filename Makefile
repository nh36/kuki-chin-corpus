# Kuki-Chin Corpus Build System
# ==============================

PYTHON := python3
TSV_DIR := data/ctd_analysis
DB_PATH := data/ctd_backend.db

# Expected counts for sanity check
EXPECTED_SOURCES := 30000
EXPECTED_TOKENS := 830000
EXPECTED_LEMMAS := 7000

.PHONY: help backend backend-check clean-backend grammar-reports dictionary

help:
	@echo "Kuki-Chin Corpus Build Targets"
	@echo "=============================="
	@echo ""
	@echo "  make backend        - Rebuild Tedim SQLite backend from TSV exports"
	@echo "  make backend-check  - Verify backend counts are sane"
	@echo "  make clean-backend  - Remove generated database"
	@echo "  make grammar-reports - Generate all grammar reports from backend"
	@echo "  make dictionary     - Generate dictionary outputs from backend"
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

# Remove generated database
clean-backend:
	rm -f $(DB_PATH)

# Generate grammar reports from backend
grammar-reports: backend-check
	@echo "Generating grammar reports..."
	$(PYTHON) scripts/generate_tam_report_backend.py
	$(PYTHON) scripts/generate_case_report_backend.py
	@echo "Grammar reports generated in output/"

# Generate dictionary outputs from backend  
dictionary: backend-check
	@echo "Dictionary generation not yet implemented"
	@echo "TODO: generate_sample_entries.py from backend"
