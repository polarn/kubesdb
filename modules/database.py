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

        self.check_if_database_exists(database)

        try:
            with self.connection.cursor() as cursor:
                sql_db = "CREATE DATABASE IF NOT EXISTS `%s`" % (database)
                cursor.execute(sql_db)
                logging.info(sql_db)

                sql_user = "CREATE USER IF NOT EXISTS '%s'@'%%' IDENTIFIED BY '%s'" % (username, password)
                cursor.execute(sql_user)
                logging.info(sql_user)

                sql_grant = "GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'%%'" % (database, username)
                cursor.execute(sql_grant)
                logging.info(sql_grant)

            self.connection.commit()
            logging.info("committed")
        except:
            raise

    def check_if_database_exists(self,database):
        try:
            with self.connection.cursor() as cursor:
                sql = "SHOW DATABASES LIKE '%s'" % (database)
                rows_returned = cursor.execute(sql)
                cursor.fetchall()
                if (rows_returned > 0):
                    return True
        except:
            raise
        return False

    def close(self):
        self.connection.close()
