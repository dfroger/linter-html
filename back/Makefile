serve: venv/bin/linter-html-server
	./$<

venv/bin/linter-html-server: venv
	./venv/bin/pip install -e .

venv:
	python -m venv venv

clean:
	rm -rf venv/ linter_html_server.egg-info/ __pycache__/

test:
	./venv/bin/python ./venv/bin/linter-html-server
