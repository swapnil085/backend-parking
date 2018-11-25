FROM tiangolo/uwsgi-nginx-flask:python3.6.6

RUN apt-get update && apt-get install -y libmysqlclient-dev python-bs4

COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN apt-get update -y 
RUN apt-get install -y python-pip python-dev build-essential

RUN mkdir /src

ADD . /src
WORKDIR /src
RUN pip install -r ./src/requirements.txt
EXPOSE 5000
