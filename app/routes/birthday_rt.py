from helpers import read_sql
from flask import Flask, Blueprint, render_template, request
import psycopg2
import pandas as pd
import appconfig as cfg

birthday_route = Blueprint('birthdays', __name__, template_folder='templates')
# Following code snippet queries the table for city
@birthday_route.route('/birthdays', methods = ['GET'])
def city():
    return render_template('birthdays.html')

@birthday_route.route('/birthdayList', methods=['GET'])
def birthday_list():

    conn = None
    birthday_result = None
    try:
        conn = psycopg2.connect(host=cfg.postgres['host'], database=cfg.postgres['db'], user=cfg.postgres['user'], password=cfg.postgres['password'])

        sql_birthday = read_sql('birthday_list.sql', './sql/')
        state_df = pd.read_sql(sql_birthday, conn)

        birthday_result = '{ "records":' + state_df.to_json(orient='records') + ', "total":8}'

        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return birthday_result


@birthday_route.route('/birthdaySave', methods = ['POST'])
def birthday_save():

    conn = None
    try:
        result = request.form
        submissions = result.values()
        birthdayid = result['record[birthdayid]']
        age = result['record[age]']

        sql_birthday_update = read_sql('birthday_save.sql', './sql/')

        conn = psycopg2.connect(host=cfg.postgres['host'], database=cfg.postgres['db'], user=cfg.postgres['user'],
                                password=cfg.postgres['password'])

        cur = conn.cursor()
        cur.execute(sql_birthday_update, (age, birthdayid))
        conn.commit()

        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return ""

