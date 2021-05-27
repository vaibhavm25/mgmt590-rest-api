from transformers.pipelines import pipeline
from flask import Flask
from flask import request
from flask import jsonify
from flask import json
import mysql.connector
import sqlite3
import os

# Create my app
app = Flask(__name__)

cnx = sqlite3.connect('database.db')


listOfTables = cnx.execute(
    """SELECT name FROM sqlite_master WHERE type='table'
    AND name='models'; """).fetchall()

if listOfTables==[]:
    cur = cnx.cursor()
    cnx.execute('create table models (name varchar(100),model varchar(100),tokenizer varchar(100))')
    sql_insert_query1 = "insert into models values(" + "'" + "distilled-bert" + "'" + "," \
                        + "'" + "distilbert-base-uncased-distilled-squad" + "'" + "," + "'" + \
                        "distilbert-base-uncased-distilled-squad" + "'" + ")"
    sql_insert_query2 = "insert into models values(" + "'" + "deepset-roberta" + "'" + "," \
                        + "'" + "deepset/roberta-base-squad2" + "'" + "," + "'" + \
                        "deepset/roberta-base-squad2" + "'" + ")"
    sql_insert_query3 = "insert into models values(" + "'" + "bert-tiny" + "'" + "," \
                        + "'" + "mrm8488/bert-tiny-5-finetuned-squadv2" + "'" + "," + "'" + \
                        "mrm8488/bert-tiny-5-finetuned-squadv2" + "'" + ")"
    cur.execute(sql_insert_query1)
    cur.execute(sql_insert_query2)
    cur.execute(sql_insert_query3)
    cnx.commit()
    cnx.close()

else:
    print("table exists")
    cnx.close()


@app.route("/models", methods=['GET', "PUT", "DELETE"])
def models():
    if request.method == 'GET':
        cnx1 = sqlite3.connect('database.db')
        sql_select_query = "select Distinct * from models"
        cursor = cnx1.cursor()
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        list1 = []

        for record in records:
            out = {
                "name": record[0],
                "tokenizer": record[2],
                "model": record[1]
            }
            list1.append(out)
        return json.jsonify(list1)
        cnx1.close()

    if request.method=="PUT":
        data = request.json
        cnx1 = sqlite3.connect('database.db')

        sql_insert_query = "insert into models values(" + "'" + data['name']+"'" + "," \
                           +"'"+ data['model'] + "'" + "," + "'" + data["tokenizer"]+"'" + ")"
        cursor = cnx1.cursor()
        cursor.execute(sql_insert_query)
        cnx1.commit()

        sql_select_query = "select Distinct * from models"
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        list1 = []

        for record in records:
            out = {
                "name": record[0],
                "tokenizer": record[2],
                "model": record[1]
            }
            list1.append(out)
        return json.jsonify(list1)
        cnx1.close()

    if request.method == "DELETE":
        cnx1 = sqlite3.connect('database.db')
        model = request.args.get('model')
        sql_delete_query = "delete from models where" + "`" + "name" + "`" + "=" + "'" + str(model) + "'"
        cursor = cnx1.cursor()
        cursor.execute(sql_delete_query)
        cnx1.commit()

        sql_select_query = "select Distinct * from models"
        cursor = cnx1.cursor()
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        list1 = []

        for record in records:
            out = {
                "name": record[0],
                "tokenizer": record[2],
                "model": record[1]
            }
            list1.append(out)
        return json.jsonify(list1)
        cnx1.close()




# Run if running "python answer.py"
if __name__ == '__main__':
    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)), threaded=True)
© 2021 GitHub, Inc.
