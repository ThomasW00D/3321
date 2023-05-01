ifeq ($(OS), Windows_NT)
run:
	python Package/Main_Login.py

install: requirements.txt
	pip install -r requirements.txt

build: setup.py
	python setup.py build bdist_wheel

clean:
	if exist "./build" rd /s /q build
	if exist "./dist" rd /s /q dist
	if exist "./EMail_Client.egg-info" rd /s /q EMail_Client.egg-info
else
run:
	python3 Package/Main_Login.py

install: requirements.txt
	pip3 install -r requirements.txt

build: setup.py
	python3 setup.py build bdist_wheel

.PHONY: test
test: requirements.txt
	pytest GMail/gmailtests.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf EMail_Client.egg-info
endif