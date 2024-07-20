FROM node:20 as node_build

#ARG VITE_API_BASE_URL

ENV VITE_API_BASE_URL=http://localhost:8080
ENV VITE_API_PREFIX=/api

WORKDIR /app

COPY ui/package*.json ./ui/
RUN npm install --prefix ui

COPY ui ./ui
RUN npm run build --prefix ui

FROM python:3.12-slim as python

WORKDIR /app

RUN apt-get update && apt-get install -y nginx && apt-get clean

RUN apt-get install -y python3-venv

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY core/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install fastapi uvicorn

COPY core /app/core

COPY --from=node_build /app/ui/dist /usr/share/nginx/html

COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 8080

CMD ["sh", "-c", "fastapi run /app/core/src/api/api.py --host 0.0.0.0 --port 8080 & nginx -g 'daemon off;'"]
