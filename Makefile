setup: requirements.txt
	pip install virtualenv
ifeq ($(OS), Windows_NT)
	py -m venv venv
	./venv/scripts/pip install -r requirements.txt
else
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
endif

run:
ifeq ($(OS), Windows_NT)
	venv\Scripts\activate
	./venv/scripts/python.exe run.py
else
	venv/bin/activate
	./venv/bin/python run.py
endif

clean:
ifeq ($(OS), Windows_NT)
	if exist __pycache__ rmdir /s /q __pycache__
	if exist venv rmdir /s /q venv
else
	rm -rf __pycache__
	rm -rf venv
endif

.PHONY: run clean setup