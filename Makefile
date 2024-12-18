# Define variables
PYTHON = python
CODE_PATH = src/honeycomb/rag_search
TEST_PATH = tests/honeycomb/rag_search

# Run code formatting and cleaning
autoformat:
	@echo "Formatting code with autopep8..."
	@autopep8 --in-place --aggressive --recursive --max-line-length 88 $(CODE_PATH)
	@echo "Formatting code with docformatter..."
	@docformatter --in-place --recursive $(CODE_PATH)
	@echo "Removing unused imports with autoflake..."
	@autoflake --in-place --remove-all-unused-imports --recursive $(CODE_PATH)
	@echo "Formatting code with black..."
	@black --line-length 88 $(CODE_PATH)

	@echo "Autoformatting completed."

# Check code formatting and style
checkformat:
	@echo "Checking code with flake8..."
	@flake8 --max-complexity 10 --max-line-length 88 --extend-ignore=E501 $(CODE_PATH)
	@echo "Check Completed"

# Run unit tests
unittests:
	@echo "Running unit tests..."
	@tox -e unittests

# Define phony targets to avoid conflicts with file names
.PHONY: autoformat checkformat unittests
