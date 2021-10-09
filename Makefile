PYTEST 	    = pytest
PYTEST_ARGS = -v -s


init:
	@echo "Run one of the below goals"
	@echo "unit       - Run all unit test cases under tests/"
	@echo "cov        - Get the test case coverage percentage"
	@echo "cov-report - Get html coverage report"

unit:
	$(PYTEST) $(PYTEST_ARGS) tests/

cov:
	$(PYTEST) --cov=crawler

cov-report:
	$(PYTEST) --cov=crawler --cov-report=html

