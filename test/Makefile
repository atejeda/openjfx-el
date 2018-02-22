SOURCES = $(shell ls *.java)
CLASSES = $(SOURCES:%.java=%.class)

all: info $(CLASSES)
	
%.class: %.java
	javac $<

clean:
	@rm -rf *.class

info:
	# java
	@readlink -f `which java`
	@java -version && echo