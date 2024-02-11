setup: requirements.txt
	py -m venv venv
	venv/scripts/python.exe -m pip install --upgrade pip
	./venv/scripts/pip install -r requirements.txt
run:
	venv/scripts/activate
	./venv/scripts/python.exe run.py
clean:
	rm -rf __pycache__
	rm -rf venv
.PHONY: run clean