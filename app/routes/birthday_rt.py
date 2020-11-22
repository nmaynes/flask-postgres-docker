from helpers import read_sql
from flask import Flask, Blueprint, render_template, request
import psycopg2
import pandas as pd
import appconfig as cfg

city_rt = Blueprint('birthday', __name__, template_folder='templates')
# Following code snippet queries the table for city
@city_rt.route('/birthday', methods = ['GET'])
def city():
    return render_template('birthdays.html')

@city_rt.route('/birthdayList', methods=['GET'])
def cityList():

    conn = None
    birthdayResult = None
    try:
        conn = psycopg2.connect(host=cfg.postgres['host'], database=cfg.postgres['db'], user=cfg.postgres['user'], password=cfg.postgres['password'])

        sqlCity = read_sql('birthday_list.sql', './sql/')
        state_df = pd.read_sql(sqlCity, conn)

        birthdayResult = '{ "records":' + state_df.to_json(orient='records') + ', "total":8}'

        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return birthdayResult


@city_rt.route('/birthdaySave', methods = ['POST'])
def citySave():

    conn = None
    try:
        result = request.form
        submissions = result.values()
        birthdayid = result['record[birthdayid]']
        age = result['record[age]']

        sqlCityUpdate = read_sql('birthday_save.sql', './sql/')

        conn = psycopg2.connect(host=cfg.postgres['host'], database=cfg.postgres['db'], user=cfg.postgres['user'], password=cfg.postgres['password'])

        cur = conn.cursor()
        cur.execute(sqlCityUpdate, (age, birthdayid))
        conn.commit()

        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return ""

