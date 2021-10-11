FROM python:3.9.4-alpine3.13

RUN mkdir -p /app/crawler

WORKDIR /app

COPY requirements.txt ./crawler
RUN pip install --upgrade pip
RUN pip install -r ./crawler/requirements.txt

COPY crawler/ ./crawler

CMD ["python", "-m", "crawler"]