FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./alembic /code/alembic
COPY alembic.ini /code/alembic.ini
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000

CMD ["/code/entrypoint.sh"]
