setup: requirements.txt
ifeq ($(OS), Windows_NT)
	py -m venv venv
	./venv/scripts/pip install -r requirements.txt
else
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
endif
run:
ifeq ($(OS), Windows_NT)
	venv/scripts/activate
	./venv/scripts/python.exe run.py
else
	venv/bin/activate
	./venv/bin/python run.py
endif
clean:
	rm -rf __pycache__
	rm -rf venv
.PHONY: run clean setup