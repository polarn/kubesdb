FROM python:3

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd -r kubesdb && useradd --no-log-init -r -g kubesdb kubesdb

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY kubesdb-connect /usr/local/bin/kubesdb-connect

USER kubesdb

CMD [ "python", "./kubesdb.py" ]
