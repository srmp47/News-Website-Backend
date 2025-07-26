# استفاده از یک ایمج پایه پایتون
FROM python:3.12-slim-bookworm

# جلوگیری از ایجاد فایل‌های کش پایتون
ENV PYTHONDONTWRITEBYTECODE 1

# نمایش لاگ‌ها در زمان اجرا
ENV PYTHONUNBUFFERED 1

# نصب وابستگی‌های سیستمی
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# تنظیم مسیر کاری در کانتینر
WORKDIR /app

# کپی فایل نیازمندی‌ها
COPY requirements.txt .

# نصب پکیج‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# کپی تمام فایل‌های پروژه
COPY . .

# ایجاد پوشه برای Celery
RUN mkdir -p /var/lib/celery/ \
    && touch /var/lib/celery/celerybeat-schedule \
    && chmod 777 /var/lib/celery/celerybeat-schedule \
    && mkdir -p /app/staticfiles