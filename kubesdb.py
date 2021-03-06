#!/usr/bin/env python
# 
# Create database based on kube secrets
#

import os
import yaml
import signal
import sys
import logging
import time

from base64 import b64decode
import kubernetes
from urllib3.exceptions import ReadTimeoutError
import pymysql.cursors

from modules.config import Config
from modules.database import Database
from modules.VERSION import Version

logging.basicConfig(
    level=logging.INFO, # if appDebug else logging.INFO,
    format="%%(asctime)s kubesdb %s %%(levelname)s: %%(message)s" % Version,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("kubesdb")
logger.setLevel(logging.INFO)

c = Config()

logger.info("Starting up...")

def watch_loop(db):
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        kubernetes.config.load_incluster_config()
    else:
        kubernetes.config.load_kube_config()

    v1 = kubernetes.client.CoreV1Api()
    w = kubernetes.watch.Watch()

    logger.info("Watching for secrets in namespace %s with label %s" % (c.namespace, c.label))

    for event in w.stream(v1.list_namespaced_secret, c.namespace, label_selector=c.label):

        event_type = event['type']
        secret = event['object']
        if event_type == "ADDED":
            data = secret.data
            if "database" and "password" and "username" in secret.data:
                database = b64decode(data['database']).decode("utf-8")
                username = b64decode(data['username']).decode("utf-8")
                password = b64decode(data['password']).decode("utf-8")
                db.create(database, username, password)
            else:
                logging.info("Secret: %s %s - secret malformed" % (event_type, secret.metadata.name))
        else:
            logging.info("Secret: %s %s - event not supported" % (event_type, secret.metadata.name))

db = Database(c)

while True:
    try:
        watch_loop(db)

    except KeyboardInterrupt:
        logging.info("Keyboard interrupt")
        db.close()
        sys.exit()

    except:
        logging.exception("could not watch for Kubernetes service changes")

    time.sleep(5)

print("End of script")
