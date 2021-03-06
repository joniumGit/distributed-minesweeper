FROM python:3.8-alpine AS builder
RUN python -m venv /opt/venv && python -m pip install --upgrade pip
ENV PATH "/opt/venv/bin:$PATH"
COPY ./game ./game
COPY ./game-server ./game-server
RUN pip install uvicorn ./game ./game-server

FROM python:3.8-alpine
RUN apk add curl
COPY --from=builder /opt/venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"
CMD python -m uvicorn --port 8080 --host 0.0.0.0 --workers 1 --no-access-log server.app:app