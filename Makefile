# https://github.com/atejeda/openjfx-el

RPMBUILD_ROOT=$(shell pwd)/rpmbuild

all: setup info
	rpmbuild --define "_topdir $(RPMBUILD_ROOT)" -ba SPECS/openjfx.spec

setup:
	mkdir -p $(RPMBUILD_ROOT)
	chown root.root -R $(RPMBUILD_ROOT)
	chown root.root -R $(shell pwd)/SPECS
	mkdir -p $(RPMBUILD_ROOT)/SOURCES

deps: setup
	spectool -C $(RPMBUILD_ROOT)/SOURCES -g SPECS/openjfx.spec
	
info:
	# os
	@cat /etc/redhat-release
	@uname -a && echo
	# qmake
	@readlink -f `which qmake`
	@qmake --version && echo
	# cmake
	@readlink -f `which cmake`
	@cmake --version && echo
	# java
	@readlink -f `which java`
	@java -version && echo
	# gcc
	@readlink -f `which gcc`
	@gcc --version
	# g++
	@readlink -f `which g++`
	@g++ --version
	@#alternatives --display java