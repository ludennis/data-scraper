FROM ubuntu:20.04

ARG SSH_KEY

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

# get the simpel web app
RUN apt-get install -y ssh
RUN mkdir -p /root/.ssh
RUN echo "$SSH_KEY" > /root/.ssh/id_rsa
RUN chmod -R 600 /root/.ssh
RUN ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

RUN apt-get install -y git
RUN git clone --branch devel git@github.com:ludennis/data-scraper.git

# install web app requirements
RUN apt-get install -y libpq-dev
RUN apt-get install -y python3-pip
RUN pip3 install flask psycopg2 --quiet

# show ip address and run web app
RUN apt-get install net-tools
RUN ifconfig
CMD python3 ./data-scraper/server.py
