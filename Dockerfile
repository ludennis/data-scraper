FROM ubuntu:20.04

ARG SSH_KEY

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

# install web app requirements
RUN apt-get install -y libpq-dev
RUN apt-get install -y python3-pip
RUN pip3 install flask psycopg2 --quiet

# get the simpel web app
RUN DEBIAN_FRONTEND=noninteractive TZ=Asia apt-get -y install tzdata
RUN apt-get install -y ssh
RUN mkdir -p /root/.ssh
RUN echo "$SSH_KEY" > /root/.ssh/id_rsa
RUN chmod -R 600 /root/.ssh
RUN ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

# show ip address and run web app
ARG rebuild
RUN apt-get install -y git
RUN apt-get install net-tools
RUN git clone --branch web-app git@github.com:ludennis/data-scraper.git

EXPOSE 8888

CMD python3 ./data-scraper/server.py
