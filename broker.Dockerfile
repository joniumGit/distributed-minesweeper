FROM python:3.8-alpine
WORKDIR /root
RUN python -m venv /opt/venv && python -m pip install --upgrade pip
ENV PATH "/opt/venv/bin:$PATH"
COPY ./broker/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ENV DS_IN_CONTAINER 1
CMD python -m uvicorn --port 8080 --host 0.0.0.0 --workers 1 --reload broker.app:app