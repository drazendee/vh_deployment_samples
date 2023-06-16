FROM ubuntu:3.10

RUN apt-get install libssl-dev -y

ADD requirements-deployment.txt .
RUN pip install -r requirements-deployment.txt
