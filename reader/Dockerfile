FROM tiangolo/uwsgi-nginx-flask:python3.5

RUN python -m pip install pip==9.0.3
RUN apt-get update
RUN apt-get install -y gcc libevent-dev python-dev

COPY ./requirements.txt /
COPY ./ /app

COPY ./nginx.conf /etc/nginx/nginx.conf
#COPY /app/certificate.pem /etc/nginx/certs
RUN pip install -r /requirements.txt

