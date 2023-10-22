FROM python:3.10

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

ENV DATABASE_URL "postgresql+asyncpg://user:password@postgres:5432/db_name"


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
