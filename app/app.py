# imports
from flask import Flask
import logging
import appconfig as cfg


from routes.mainmenu_rt import mainmenu_rt


app = Flask(__name__)

app.register_blueprint(mainmenu_rt)


# this is a very useful setting for automatically reloading html changes
# https://stackoverflow.com/questions/9508667/reload-flask-app-when-template-file-changes

app.config['TEMPLATES_AUTO_RELOAD'] = True
logging.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':
    app.run(host=cfg.appcfg['host'], debug=cfg.appcfg['debug'])
