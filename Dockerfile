FROM ubuntu:latest
RUN apt-get update && apt-get install -y libmysqlclient-dev python-bs4
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["python","./src/app.py"]
