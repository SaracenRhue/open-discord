FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV DISCORD_TOKEN=""
ENV ADMIN_ID=""
ENV OLLAMA_URL=""
ENV MODEL=""

CMD ["python", "main.py"]