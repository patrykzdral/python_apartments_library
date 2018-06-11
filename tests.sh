
#!/usr/bin/env bash
set -e
virtualenv venv --distribute -p python3
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. venv/bin/python3 testing/test_simple.py
PYTHONPATH=. venv/bin/coverage run testing/test_simple.py
