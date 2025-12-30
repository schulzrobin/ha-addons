# Nutze offizielles Python-3.11 slim Image
FROM python:3.11-slim

WORKDIR /app

# venv erstellen (in slim Images ist venv meist schon vorhanden)
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Dependencies installieren
COPY app/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# App kopieren
COPY app ./app
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]