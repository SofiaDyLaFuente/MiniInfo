FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
