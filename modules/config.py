import os
import logging

class Config:
    database_host = 'localhost'
    database_user = 'root'
    database_password = 'password'
    namespace = 'default'
    label = 'kubesdb'

    def __init__(self):
        if "NAMESPACE" in os.environ and os.environ['NAMESPACE']:
            self.namespace = os.environ['NAMESPACE']
        if "LABEL" in os.environ and os.environ['LABEL']:
            self.label = os.environ['LABEL']
        if "DATABASE_HOSTNAME" in os.environ and os.environ['DATABASE_HOSTNAME']:
            self.database_host = os.environ["DATABASE_HOSTNAME"]
        if "DATABASE_MASTER_USERNAME" in os.environ and os.environ['DATABASE_MASTER_USERNAME']:
            self.database_user = os.environ["DATABASE_MASTER_USERNAME"]
        if "DATABASE_MASTER_PASSWORD" in os.environ and os.environ['DATABASE_MASTER_PASSWORD']:
            self.database_password = os.environ["DATABASE_MASTER_PASSWORD"]

        logging.info("Config done")
