FROM tiangolo/uwsgi-nginx-flask:python3.5
ENV FQDN *.example.com
RUN python -m pip install pip==9.0.3
RUN apt-get update
RUN apt-get install -y gcc libevent-dev python-dev
COPY ./requirements.txt /
COPY ./ /app
COPY ./gen_cert.sh /gen_cert.sh
RUN pip install -r /requirements.txt
CMD sh /gen_cert.sh && cp /server.crt /etc/nginx/certs:/etc/nginx/certs && /start.sh




