import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@%s/%s' % (
        # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
        os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['DBNAME']
    )