FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY app /app/app

EXPOSE 8080

CMD [ "fastapi", "run", "app/api/api.py", "--port", "8080" ]