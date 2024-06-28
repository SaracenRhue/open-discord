FROM python:3.11-slim

WORKDIR /home/app

COPY . .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

CMD python main.py