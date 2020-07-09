FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements ./requirements
RUN pip install -r requirements/local.txt
