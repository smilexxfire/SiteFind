FROM python:3.9.19
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && chmod +x thirdparty/*
CMD ["python", "sitefind_worker.py", "|| exit 1"]