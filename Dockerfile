FROM python:3

RUN groupadd -r kubesdb && useradd --no-log-init -r -g kubesdb kubesdb

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER kubesdb

CMD [ "python", "./kubesdb.py" ]
