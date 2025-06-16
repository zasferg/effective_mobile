FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
COPY ./src/.env /app/src/.env

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install uvicorn

COPY ./src /app/src

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn src.app:app --host 0.0.0.0"]





