FROM python:3.5

RUN python -m pip install pip==9.0.3
RUN pip install flask-ask
RUN pip install cryptography==2.1.4
RUN apt-get update
RUN apt-get install -y gcc libevent-dev python-dev

RUN pip install --upgrade pip
COPY ./requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ /app
RUN python /app/nltkDown.py
WORKDIR /app
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app"]