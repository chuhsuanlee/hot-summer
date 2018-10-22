FROM python:2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

## python dependency (requirements.txt)
COPY src/requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

## copy file to /usr/src/app
COPY ./src /usr/src/app

ENTRYPOINT ["python", "main.py"]
