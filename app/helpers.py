import os
from datetime import datetime

def read_sql(report, sql_path='../app/sql/'):
    with open(os.path.join(sql_path, report), 'r') as f:
            sql = f.read()
    return sql