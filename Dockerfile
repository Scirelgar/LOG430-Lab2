FROM python:3.12-slim
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
EXPOSE 8000

RUN useradd app
USER app

CMD fastapi dev src/main.py --host 0.0.0.0 --port 8000