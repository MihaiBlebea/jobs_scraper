FROM python:3.9

WORKDIR /app

COPY ./src /app/src

RUN python3 -m venv virtualenv

COPY requirements.txt .

RUN /app/virtualenv/bin/pip3 install -r requirements.txt

VOLUME [ "/app/store.db" ]

EXPOSE 5000

CMD ["/app/virtualenv/bin/python3", "/app/src/api.py"]