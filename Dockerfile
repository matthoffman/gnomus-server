FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# For Flask
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# For some other command
# CMD ["python", "app.py"]
