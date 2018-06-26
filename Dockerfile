FROM python:3.6-alpine as builder
RUN apk update
RUN apk add --no-cache gcc python3-dev musl-dev postgresql-dev
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

FROM python:3.6-alpine
RUN apk update
RUN apk add --no-cache libpq
COPY --from=builder /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
RUN mkdir /app
COPY *.py /app/
WORKDIR /app
ENTRYPOINT ["python", "/app/fetch.py"]
