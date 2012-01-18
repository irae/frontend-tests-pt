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
	@if [ ! -e "$(JENKINS)" ] ; then curl -L -o $(JENKINS) http://mirrors.jenkins-ci.org/war/1.420/jenkins.war; else echo "OK" ;fi
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
.PHONY: help
help:
	@echo "==== ${RED}Hi! U new here?${NC}"
	@echo "   * ${GREEN}downloads${NC} : will get the binaries I don't like on git from the internet"
	@echo "   * ${GREEN}clean-downloads${NC} : will delete files downloaded by 'make downloads'"
	@echo "   * ${GREEN}start_jenkins${NC} : will start jenkins on port 8081 with configdir in this project folder"
	@echo "   * ${GREEN}stop_jenkins${NC} : will send a command to jenkins to stop (curl error if not running)"
	@echo "   * ${GREEN}clean${NC} : will delete log files and stuff"
#
