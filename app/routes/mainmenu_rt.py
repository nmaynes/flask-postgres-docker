from flask import Flask,Blueprint, render_template
import psycopg2
import pandas as pd
from helpers import read_sql
import appconfig as cfg
from flask import Flask,Blueprint, render_template
import psycopg2
import pandas as pd
import appconfig as cfg

mainmenu_rt = Blueprint('mainmenu', __name__, template_folder='templates')
# Following code snippet queries the table for mainmenu
@mainmenu_rt.route('/', methods = ['GET'])
def mainmenu():
    conn = None
    birthdays = None
    results_list = []
    print("Main Menu")
    try:
        conn = psycopg2.connect(host=cfg.postgres['host'], database=cfg.postgres['db'], user=cfg.postgres['user'],
                                password=cfg.postgres['password'])

        sql_birthdays = '''SELECT f.name, b.birthdate FROM birthdays b, friends f where f.id = b.fid'''
        birthdays = pd.read_sql(sql_birthdays, conn)

        for row in birthdays.itertuples():
            display_dict = {"name": row.name, "birthdate": row.birthdate}
            results_list.append(display_dict)
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return render_template("main_menu.html", data=results_list)
