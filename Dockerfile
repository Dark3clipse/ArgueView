FROM ubuntu:focal
MAINTAINER Sophia Hadash <s.hadash@tue.nl>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qqy && \
	apt-get install software-properties-common git python3.6 python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget -qqy && \
	pip3 install pipenv

ENV PROJECT_DIR /argueview
WORKDIR ${PROJECT_DIR}
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy --dev
