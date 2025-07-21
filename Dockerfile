# 1. Imagem base
# Use uma imagem oficial do Python como base.
# A versão 3.12 é compatível com as dependências do seu requirements.txt.
FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app
COPY ./alembic /code/alembic
COPY alembic.ini .
COPY ./front_end /code/front_end
COPY ./start.sh /code/start.sh
RUN chmod +x /code/start.sh


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]