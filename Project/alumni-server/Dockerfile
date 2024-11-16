FROM python:3.12

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY src/ /src
WORKDIR /src

# exec form to receive signals for graceful shutdown
CMD exec gunicorn \
    -b :5000 \
    --workers 3 \
    --worker-class gevent \
    --worker-tmp-dir /dev/shm \
    --timeout 30 \
    app:app
