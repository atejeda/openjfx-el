# https://github.com/atejeda/openjfx-rpm

RPMBUILD_ROOT=/root/rpmbuild

all: info
	chown root.root -R $(RPMBUILD_ROOT)
	mkdir -p $(RPMBUILD_ROOT)/SOURCES/
	rpmbuild -ba SPECS/openjfx.spec

deps:
	spectool -g -R SPECS/openjfx.spec
	
info:
	# os
	@cat /etc/redhat-release
	@uname -a && echo
	# cmake
	@which cmake
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