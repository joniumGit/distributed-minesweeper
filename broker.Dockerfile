FROM python:3.8-alpine AS builder
RUN python -m venv /opt/venv && python -m pip install --upgrade pip
ENV PATH "/opt/venv/bin:$PATH"
COPY ./broker ./broker
RUN pip install uvicorn ./broker

FROM python:3.8-alpine
COPY --from=builder /opt/venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"
ENV DS_IN_CONTAINER 1
CMD python -m uvicorn --port 8080 --host 0.0.0.0 --workers 2 broker.app:app