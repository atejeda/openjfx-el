# https://github.com/atejeda/openjfx-rpm

RPMBUILD_ROOT=~/rpmbuild

all:

	
.PHONY: info
info:
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
	# os
	@cat /etc/redhat-release
	@uname -a
