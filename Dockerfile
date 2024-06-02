FROM ubuntu/postgres:14-22.04_beta
RUN apt-get update

RUN apt-get install build-essential -y --no-install-recommends
RUN apt-get install cmake -y
RUN apt-get install sudo -y
RUN apt-get install wget -y
RUN apt-get install sudo -y

RUN apt-get install net-tools -y

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install postgresql-client -y

RUN apt-get install python3-pip -y
RUN apt-get install python3 -y

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /
RUN dpkg -i /google-chrome-stable_current_amd64.deb 2>&1 > /dockerfile_build.log || echo "Allowing dpkg error"

RUN apt-get install -f -y
RUN dpkg -i /google-chrome-stable_current_amd64.deb

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /home/ubuntu
WORKDIR /home/ubuntu
