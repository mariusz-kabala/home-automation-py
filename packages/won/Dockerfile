FROM python:3.11

RUN mkdir /app 
COPY won /app/won
COPY pyproject.toml /app 
COPY poetry.lock /app
COPY README.md /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD [ "poetry", "run", "start" ]
