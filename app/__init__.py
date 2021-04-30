"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask
from yaml import load, Loader
import random



def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST'),
            query={
                "unix_socket": "{}/{}".format(
                    os.environ.get("DB_SOCKET_DIR"),  # e.g. "/cloudsql"
                    os.environ.get("CLOUD_SQL_CONNECTION_NAME"))  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        )
    )

    return pool
#INSTANCE_CONNECTION_NAME
#mercury-scheduler:us-central1:musketeers
#<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>
#instance name - musketeers
#db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

def randstr():
    result = ""
    for i in range(64):
        base = 'a'
        lower = random.randint(0, 1)
        if lower == 0:
            base = chr(ord('a') + random.randint(0, 25))
        else:
            base = chr(ord('A') + random.randint(0, 25))
        result += base
    return result


app = Flask(__name__)
app.secret_key = randstr()
db = init_connection_engine()

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes
