FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
      build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps

# Copy project files
COPY . /backend

# Set working directory
WORKDIR /backend

# Copy the entrypoint script separately to ensure it exists
COPY ./entrypoint.sh /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["sh", "/entrypoint.sh"]
