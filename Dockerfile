FROM python:3.13-slim

WORKDIR /app

# System dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libmariadb-dev \
    build-essential \
    pkg-config \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-mysql.sh /app/wait-for-mysql.sh
RUN chmod +x /app/wait-for-mysql.sh

EXPOSE 8000

CMD ["./wait-for-mysql.sh", "db:3306", "--", "python", "news_app/manage.py", "runserver", "0.0.0.0:8000"]
