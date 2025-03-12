FROM python:3.9-slim
WORKDIR /app
COPY python.py /app/python.py

RUN pip install flask
EXPOSE 5000
CMD ["python", "python.py"]