FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ../Цифрвой%20прорыв%20Пермь/requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app/
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]