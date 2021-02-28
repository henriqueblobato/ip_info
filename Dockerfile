FROM python:3.8

WORKDIR /tmp

COPY . /tmp
RUN ls -lah /tmp
RUN apt update

RUN apt install -y tor net-tools
RUN echo "ControlPort 9051" >> /etc/tor/torrc
RUN echo HashedControlPassword $(tor --hash-password henrique | cut -d "." -f 2 | tail -n 1) >> /etc/tor/torrc
RUN echo "CookieAuthentication 1" >> /etc/tor/torrc
RUN service tor stop && service tor start
RUN tail /etc/tor/torrc
RUN ifconfig | grep inet

RUN pip install -r "/tmp/requirements.txt"

EXPOSE 80
EXPOSE 8080
EXPOSE 9050
EXPOSE 9051

ENV FLASK_APP = /tmp/app.py
ENV SERVER_NAME = '0.0.0.0'

CMD ["python3", "main2.py"]
# CMD ["gunicorn", "--config", "/tmp/gunicorn_config.py", "main:app"]
