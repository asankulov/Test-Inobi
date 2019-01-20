FROM python:3.7-slim-stretch

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install build-essential gcc python-dev -y

COPY requirements.txt .
RUN pip install pip --upgrade
RUN pip3 install --no-cache -r requirements.txt
RUN pip3 install uwsgi

COPY . .

CMD [ "uwsgi", "--ini", "app.ini" ]