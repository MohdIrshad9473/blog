# ckass property in small or all in capital; dont mix
class config:
    database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser="postgres",
        dbpass="irshad9473",
        dbhost="127.0.0.1",
        dbname="irshad"

    )
    secret_key = "SeCrate willl be string"
    Mail_SERVER = "smtp.googlemail.com" 
    MAIL_PORT = 587
    BASE_URL = "http://127.0.0.1:5000" 

#  postgresql+psycopg2://postgres:irshad9473@127.0.0.1/postgres