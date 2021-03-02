FROM python:3.8

WORKDIR /tmp

COPY . /tmp
RUN ls -lah /tmp
RUN apt update

RUN apt install -y tor net-tools

RUN pip install -r "/tmp/requirements.txt"

EXPOSE 5000
EXPOSE 80

ENV FLASK_APP = /tmp/app.py
ENV SERVER_NAME = '0.0.0.0'

# CMD ["python3", "main2.py"]
# CMD ["gunicorn", "--config", "/tmp/gunicorn_config.py", "main:app"]
CMD ["gunicorn", "main2:app"]
