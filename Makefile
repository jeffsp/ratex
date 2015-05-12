# @file Makefile
# @brief run across texas
# @author Jeff Perry <jeffsp@gmail.com>
# @version 1.0
# @date 2014-05-31

default:
	python run.py

run: default

check: pep8 automatic_tests interactive_tests

automatic_tests:
	python ./test_application.py
	python ./test_forms.py
	python ./test_models.py
	python ./test_stormpath.py

interactive_tests:
	-python ./test_runkeeper.py
	-python ./test_login.py

pep8:
	pep8 *.py
	pep8 application/*.py
	pep8 application/runkeeper/*.py
