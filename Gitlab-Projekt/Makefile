# Root directory for exercises
EXERCISES_DIR = Courses
EXERCISES = $(shell find $(EXERCISES_DIR) -name 'Makefile')
EXERCISES_DIRS = $(dir $(EXERCISES))

# Default targets
all: test check-style autograde

# Create global feedback directory
feedback-dir:
	@echo "Creating feedback directory..."
	@mkdir -p feedback
	@echo "Feedback directory created."

# Run tests for all exercises
test: feedback-dir
	@echo "========== Running Tests for All Exercises =========="
	@for dir in $(EXERCISES_DIRS); do \
		EXERCISE_NAME=$$(basename $$dir); \
		echo "Processing directory: $$dir"; \
		if [ -f $$dir/Makefile ]; then \
			echo "Makefile found in $$dir. Running tests..."; \
			$(MAKE) -C $$dir test 2>&1 | tee -a feedback/errors.log >> feedback/$$EXERCISE_NAME-test-result.txt || { \
				echo "Error running tests in $$dir" >> feedback/errors.log; true; }; \
		else \
			echo "Skipping $$dir: No Makefile found." | tee -a feedback/errors.log; \
		fi; \
	done
	@echo "========== Tests Completed =========="

# Perform style checks for all exercises
check-style: feedback-dir
	@echo "========== Checking Style for All Exercises =========="
	@for dir in $(EXERCISES_DIRS); do \
		EXERCISE_NAME=$$(basename $$dir); \
		echo "Processing directory: $$dir"; \
		if [ -f $$dir/Makefile ]; then \
			if $(MAKE) -q -C $$dir check-style > /dev/null 2>&1; then \
				echo "Check-style target found in $$dir. Running style checks..."; \
				$(MAKE) -C $$dir check-style 2>> feedback/errors.log >> feedback/$$EXERCISE_NAME-lint-result.txt || { \
					echo "Error running style checks in $$dir" >> feedback/errors.log; true; }; \
			else \
				echo "No check-style target in $$dir. Running default style check..."; \
				PYTHON_FILES=$$(find $$dir/scr -name '*.py'); \
				if [ -n "$$PYTHON_FILES" ]; then \
					mkdir -p feedback; \
					python3 -m pylint $$PYTHON_FILES 2>> feedback/errors.log >> feedback/$$EXERCISE_NAME-lint-result.txt || { \
						echo "Error running style checks in $$dir" >> feedback/errors.log; true; }; \
				else \
					echo "No Python files found in $$dir/scr"; \
				fi; \
			fi; \
		else \
			echo "Skipping $$dir: No Makefile found." | tee -a feedback/errors.log; \
		fi; \
	done
	@echo "========== Style Checks Completed =========="

# Run autograde for all exercises
autograde: feedback-dir
	@echo "========== Running Autograde for All Exercises =========="
	@for dir in $(EXERCISES_DIRS); do \
		EXERCISE_NAME=$$(basename $$dir); \
		echo "Processing directory: $$dir"; \
		if [ -f $$dir/Makefile ]; then \
			echo "Makefile found in $$dir. Running autograde..."; \
			$(MAKE) -C $$dir autograde 2>&1 | tee -a feedback/errors.log >> feedback/$$EXERCISE_NAME-autograde-result.txt || { \
				echo "Error running autograde in $$dir" >> feedback/errors.log; true; }; \
		else \
			echo "Skipping $$dir: No Makefile found." | tee -a feedback/errors.log; \
		fi; \
	done
	@echo "========== Autograde Completed =========="

# Clean feedback directories for all exercises
clean:
	@echo "========== Cleaning All Exercises =========="
	@for dir in $(EXERCISES_DIRS); do \
		EXERCISE_NAME=$$(basename $$dir); \
		echo "Processing directory: $$dir"; \
		if [ -f $$dir/Makefile ]; then \
			$(MAKE) -C $$dir clean || { echo "Error cleaning $$dir" | tee -a feedback/errors.log; true; }; \
		else \
			echo "Skipping $$dir: No Makefile found." | tee -a feedback/errors.log; \
		fi; \
	done
	@rm -rf feedback
	@echo "========== Cleaning Completed =========="
