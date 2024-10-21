FROM python:3.11.10-slim-bookworm

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ../../Model/Lud/app /app
#COPY app/requirements.txt /app/requirements.txt

RUN python3 -m venv venv

#ENV GITHUB_TOKEN=aaa

RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 1234

CMD ["gunicorn", "-b", "0.0.0.0:1234", "app:app"]
