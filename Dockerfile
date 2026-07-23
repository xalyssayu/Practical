FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]