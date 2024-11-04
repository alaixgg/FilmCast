import os
import pymysql.cursors
import time

import logging
logging.basicConfig(level=logging.INFO)

host_env = os.getenv('DB_HOST')
user_env = os.getenv('DB_USER')
pass_env = os.getenv('DB_PASSWORD')
db_env = os.getenv('DB_NAME')

# Helper to connect to the DB
def get_db_connection(host=None, user=None, password=None, database=None):
    while True:
        try:
            connection = pymysql.connect(
                host=host_env,
                user=user_env,
                password=pass_env,
                database=db_env
            )
            return connection
        except pymysql.err.OperationalError as e:
            logging.warning(f"Error!!!!! -> {e}")
            logging.warning("Database connection failed, retrying in 5 seconds...")
            time.sleep(5)

