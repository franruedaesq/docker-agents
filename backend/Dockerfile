FROM python:latest

# host.docker.internal insted of localhost
RUN apt-get update && apt-get install -y curl
# Create python virtual enviornment
# isolate our python app and install from system-level python
RUN python -m venv /opt/venv/
ENV PATH=/opt/venv/bin:$PATH

WORKDIR /app

# copy localfolder container_destination
COPY requirements.txt /tmp/requirements.txt

# RUN within_container_while_building
RUN pip install -r /tmp/requirements.txt
COPY ./src .

CMD ["python", "-m", "http.server", "8000"]


