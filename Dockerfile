FROM python:3.7

WORKDIR /opt/project

ADD poetry.lock pyproject.toml /opt/project/

RUN pip install poetry && \
    poetry config settings.virtualenvs.create false && \
    poetry install

EXPOSE 80

ADD . /opt/project/

CMD ["uvicorn", "api.endpoint:app", "--host", "0.0.0.0", "--port", "$PORT"]