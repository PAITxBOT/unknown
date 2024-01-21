FROM python:3.10.8-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip install -U pip && pip install -U -r requirements.txt
#RUN pip install python-telegram-bot --upgrade && python -m pip show python-telegram-bot
WORKDIR /app

COPY . .
CMD ["python", "bot.py"]
