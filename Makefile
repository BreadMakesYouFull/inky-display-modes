.PHONY: install
install: # install to local virtual environment
	./scripts/install.sh

run: ./venv
run: # Run inkymapfunc
	./scripts/run.sh

.PHONY: uninstall
uninstall: # install to local virtual environment
	rm -rf venv *.egg-info build
	find . -path '*/__pycache__/*' -delete
	find . -type d -name '__pycache__' -empty -delete
clean: uninstall

help: # Show available targets
	@echo "inkyfuncmap makefile\n"
	@echo "Usage: make [target]\n"
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9_-]+: #' < Makefile
	@echo ""
usage: help
.PHONY: help

