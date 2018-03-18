class DB_CREDENTIALS :
    DATABASE_ENGINE     = 'django.db.backends.postgresql_psycopg2'
    DATABASE_NAME       = 'sms'
    DATABASE_USER       = 'sms'
    DATABASE_PASSWORD   = 'helloworld'
    DATABASE_HOST       = '127.0.0.1'
    DATABASE_PORT       = '5432'

class MONGO_CREDENTIALS:
    DATABASE_NAME       = 'sms'
    # DATABASE_USER       = 'stamp'
    # DATABASE_PASSWORD   = 'p@ssw0rd'


ServerMail = 'noname.ssp1@gmail.com'

DATE_INPUT_FORMATS = ['%d-%m-%Y']