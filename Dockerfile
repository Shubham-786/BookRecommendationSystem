FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV DATABASE_URL=postgresql+asyncpg://myusername:mypassword@mydbinstance.abcdefg123456.us-west-2.rds.amazonaws.com:5432/mydatabase

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

