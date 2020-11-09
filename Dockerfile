FROM ubuntu:focal
MAINTAINER Sophia Hadash <s.hadash@tue.nl>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qqy && \
	apt-get install software-properties-common git python3.6 python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget twine -qqy && \
	pip3 install pipenv

# install docker
RUN if test $(uname -m) = "x86_64"; then \
		a="amd64"; \
	elif test $(uname -m) = "armhf"; then \
		a="armhf"; \
	elif test $(uname -m) = "aarch64"; then \
		a="arm64"; \
	fi && \
    apt-get update -qq && \
	apt-get install -qqy --no-install-recommends apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
	curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
	add-apt-repository \
   		"deb [arch=${a}] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   		$(lsb_release -cs) \
   		stable" && \
	apt-get update -qq && \
	apt-get install -qqy --no-install-recommends docker-ce docker-ce-cli containerd.io && \
	apt-get clean

ENV PROJECT_DIR /argueview
WORKDIR ${PROJECT_DIR}
COPY Pipfile Pipfile.lock build.sh CHANGELOG.md LICENSE MANIFEST.in README.md settings.py setup.py ${PROJECT_DIR}/
COPY argueview ${PROJECT_DIR}/
RUN pipenv install --system --deploy --dev
