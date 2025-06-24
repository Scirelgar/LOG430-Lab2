FROM python:3.12-slim
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN useradd app
USER app

# Support pour les caisses multiples
# Utiliser une variable d'environnement pour spécifier l'ID de caisse
ENV CASHIER_ID=""
CMD if [ -n "$CASHIER_ID" ]; then python src/main.py --cashier-id $CASHIER_ID; else python src/main.py; fi