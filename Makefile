# colors, 'cause bitches loves colors
RED=\033[01;31m
GREEN=\033[01;32m
NC=\033[01;00m

# env
SRCDIR = $(shell pwd)
JENKINS="$(SRCDIR)/bin/jenkins.war"

# local
os=$(shell uname)

#
.PHONY: default
default: help
#
.PHONY: downloads
downloads:
	@echo "Downloading binary (unversioned) files"
	@echo "${GREEN}Jenkins${NC}"
	@mkdir -p $(SRCDIR)/bin
	@if [ ! -e "$(JENKINS)" ] ; then curl -L -o $(JENKINS) http://mirrors.jenkins-ci.org/war/1.420/jenkins.war;fi
	@echo "OK"
	@echo "${GREEN}git submodules${NC}"
	@git submodule init
	@git submodule update
	@echo "OK"
	@echo "${GREEN}pip dependencies${NC}"
	@pip install -r requirements.txt && echo "OK"
#
.PHONY: clean
clean:
	@echo "Deleting logs and stuff"
	@rm -rf $(SRCDIR)/logs/*
	@# restore .gitkeep
	@touch $(SRCDIR)/logs/.gitkeep
#
.PHONY: clean-downloads
clean-downloads:
	@echo "Deleting dowloaded files"
	@rm $(JENKINS)
#
.PHONY: start_jenkins
start_jenkins:
	@JENKINS_HOME=$(SRCDIR)/jenkins/ nohup java -jar $(JENKINS) --httpPort=8081 > $(SRCDIR)/logs/jenkins.log 2>&1 &
	@echo "Jenkins started on http://0.0.0.0:8081/"
#
.PHONY: stop_jenkins
stop_jenkins:
	@curl http://0.0.0.0:8081/exit
#
#
.PHONY: slide_gen
slide_gen:
	@landslide slides.md -i -l table
#
.PHONY: slides
slides:
	@make slide_gen
	@open presentation.html
#
.PHONY: help
help:
	@echo "==== ${RED}Hi! U new here?${NC}"
	@echo "   * ${GREEN}downloads${NC} : get the binaries I don't like on git from the internet"
	@echo "   * ${GREEN}clean-downloads${NC} : delete files downloaded by 'make downloads'"
	@echo "   * ${GREEN}clean${NC} : delete log files and stuff"
	@echo "==== ${RED}Slides${NC}"
	@echo "   * ${GREEN}slide_gen${NC} : generate presentation.html from slides.md"
	@echo "   * ${GREEN}slides${NC} : generate and open slideshow on browser"
	@echo "==== ${RED}Continuous Integration${NC}"
	@echo "   * ${GREEN}start_jenkins${NC} : start jenkins on port 8081 with configdir in this project folder"
	@echo "   * ${GREEN}stop_jenkins${NC} : send a command to jenkins to stop (curl error if not running)"
#
