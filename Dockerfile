FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV DISCORD_TOKEN=""
ENV ADMIN_ID=""
ENV OLLAMA_URL=""
ENV MODEL=""
ENV SD_URL=""

CMD ["python", "main.py"]