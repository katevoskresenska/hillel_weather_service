FROM python:3.6.11-slim-stretch

WORKDIR /root/weather_web

ADD weather /root/weather_web/weather
ADD weather_api /root/weather_web/weather_api
ADD utils /root/weather_web/utils
ADD manage.py requirements.txt ./

RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000