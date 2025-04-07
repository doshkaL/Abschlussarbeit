# Directories
SRC_DIR := src
TEST_DIR := test
FEEDBACK_DIR := feedback

# Python executable (can be overridden by an environment variable)
PYTHON ?= python3

# Files
PYTHON_FILES := $(wildcard $(SRC_DIR)/*.py)
GRADE_FILE := test/autograde.py

# Define PYTHONPATH
PYTHONPATH := "$(PWD):$(PWD)/$(SRC_DIR)"

# Phony targets
.PHONY: all test autograde check-style clean

# Default target
all: test autograde check-style

# Target to run unit tests
test:
	@echo "========== Running Unit Tests =========="
	@mkdir -p $(FEEDBACK_DIR)
	@if [ -d "$(TEST_DIR)" ]; then \
		export PYTHONPATH=$(PYTHONPATH) && $(PYTHON) -m pytest -s $(TEST_DIR)/*.py 2>&1 | tee -a $(FEEDBACK_DIR)/test-results.txt || { \
		echo "Tests failed. Check $(FEEDBACK_DIR)/test-results.txt for details."; \
		exit 1; }; \
	else \
		echo "Error: Test directory $(TEST_DIR) not found!"; \
		exit 1; \
	fi
	@echo "Tests completed successfully."

# Target to run autograde.py
autograde:
	@echo "========== Running Autograde =========="
	@mkdir -p $(FEEDBACK_DIR)
	@if [ -f "$(GRADE_FILE)" ]; then \
		export PYTHONPATH=$(PYTHONPATH) && $(PYTHON) $(GRADE_FILE) 2>&1 | tee -a $(FEEDBACK_DIR)/autograde-results.txt || { \
		echo "Autograde execution failed. Check $(FEEDBACK_DIR)/autograde-results.txt for details."; \
		exit 1; }; \
	else \
		echo "Error: Grading file $(GRADE_FILE) not found!"; \
		exit 1; \
	fi
	@echo "Autograde completed successfully."

# Check Python style with pylint
check-style:
	@echo "========== Running Style Checks =========="
	@mkdir -p $(FEEDBACK_DIR)
	@if [ -n "$(PYTHON_FILES)" ]; then \
		$(PYTHON) -m pylint $(PYTHON_FILES) 2>&1 | tee -a $(FEEDBACK_DIR)/lint-results.txt || { \
		echo "Style checks failed. Check $(FEEDBACK_DIR)/lint-results.txt for details."; \
		exit 1; }; \
	else \
		echo "No Python files found in $(SRC_DIR)."; \
		exit 1; \
	fi
	@echo "Style checks completed successfully."

# Clean up the project: remove feedback directory
clean:
	@echo "========== Cleaning Up =========="
	@rm -rf $(FEEDBACK_DIR)
	@echo "Cleanup complete."
