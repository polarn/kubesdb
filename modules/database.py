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

    def create_database(self, database, username, password):
        logging.info("Creating database: %s" % (database))

        try:
            with self.connection.cursor() as cursor:
                sql_db = "CREATE DATABASE IF NOT EXISTS `%s`" % (database)
                cursor.execute(sql_db)

                sql_user = "CREATE USER IF NOT EXISTS '%s'@'%%' IDENTIFIED BY '%s'" % (username, password)
                cursor.execute(sql_user)

                sql_grant = "GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'%%'" % (database, username)
                cursor.execute(sql_grant)

            self.connection.commit()
        except:
            raise

    def close(self):
        self.connection.close()
