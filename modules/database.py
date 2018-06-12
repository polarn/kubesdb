import logging
import pymysql.cursors
from modules.config import Config

class Database:

    def __init__(self, c):
        self.connection = pymysql.connect(host=c.database_host,
                                    user=c.database_user,
                                    password=c.database_password,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def create(self, database, username, password):
        logging.info("Create: database=%s, username=%s" % (database, username))

        try:
            self.create_database(database)
            self.create_user(username, password)
            self.create_grant(database, username)

            self.connection.commit()
            logging.info("committed")
        except:
            raise

    def create_database(self, database):
        logging.info("Creating database: %s" % (database))
        cursor = self.connection.cursor()
        rows_returned = cursor.execute("SHOW DATABASES LIKE '%s'" % (database))
        cursor.fetchall()
        if (rows_returned > 0):
            logging.debug("Database %s already exists" % database)
        else:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `%s`" % (database))
            logging.info("Database %s created" % database)

    def create_user(self, username, password):
        logging.info("Creating user: %s" % (username))
        cursor = self.connection.cursor()
        rows_returned = cursor.execute("SELECT * FROM mysql.user WHERE user = '%s'" % (username))
        cursor.fetchall()
        if (rows_returned > 0):
            logging.debug("User %s already exists" % username)
        else:
            cursor.execute("CREATE USER IF NOT EXISTS '%s'@'%%' IDENTIFIED BY '%s'" % (username, password))
            logging.info("User %s created" % username)

    def create_grant(self, database, username):
        logging.info("Creating grant for user %s on database %s" % (username, database))
        cursor = self.connection.cursor()
        cursor.execute("GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'%%'" % (database, username))

    def close(self):
        self.connection.close()
