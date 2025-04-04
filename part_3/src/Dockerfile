FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

COPY . /src/

EXPOSE 8000

CMD ["python", "/src/ed_project/manage.py", "runserver", "0.0.0.0:8000"]
