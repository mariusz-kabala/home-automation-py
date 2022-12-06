FROM python:3.11

RUN mkdir /app 
COPY lgsoundbar /app/lgsoundbar
COPY pyproject.toml /app 
COPY poetry.lock /app
COPY README.md /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ARG MQTT_HOST
ARG DEVICE_IP

ENV MQTT_HOST ${MQTT_HOST}
ENV DEVICE_IP ${DEVICE_IP}

CMD [ "poetry", "run", "start" ]
