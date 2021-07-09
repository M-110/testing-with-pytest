.PHONY: install, test, rate, clean

install:
	venv/scripts/pip.exe install -e . --use-feature=in-tree-build

test:
	venv/scripts/python.exe -m pytest tests -v ${args}

rate:
	-flake8 src/tasks
	-pylint src/tasks

clean:
	@echo hello $(name)