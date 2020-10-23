FROM python:3.7-slim

RUN apt update
RUN apt install -y libcairo2-dev

RUN mkdir /golem \
  && mkdir /golem/work

COPY data/country_codes.csv /golem/country_codes.csv
COPY data/owid-covid-data.csv /golem/owid-covid-data.csv
COPY requirements.txt /golem/requirements.txt

RUN pip3 install -r /golem/requirements.txt

COPY plot.py /golem/plot.py

VOLUME /golem/work
