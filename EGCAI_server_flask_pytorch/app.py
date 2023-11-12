import os
import json
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify
import image_process
from flask_cors import CORS
from utils.json_to_sql import json_to_sql


app = Flask(__name__)
CORS(app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='endo',
                            user='endo',
                            password='123456')
    return conn


@app.route('/api/login', methods=('GET', 'POST'))
def login():
    pass


@app.route('/api/survey_response', methods=['POST'])
def survey_response():
    response_json = request.get_json()
    response_sql = json_to_sql(response_json)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(response_sql)
    conn.commit()
    survey_id = response_json['Responses'][0]['Survey_id']
    cur.execute('SELECT row_to_json(t) FROM(SELECT * FROM surveys WHERE '
                'Survey_id=%s) t',
                (survey_id,))
    survey = cur.fetchall()
    cur.close()
    conn.close()
    survey_dict = {
        'msg': 'success',
        'data': survey
    }
    return jsonify(survey_dict)


@ app.route('/api/survey', methods=['GET'])
def survey(survey_id):
    pass


@ app.route('/api/Answer_question', methods=('GET', 'POST'))
def Answer_question():
    pass


@ app.route('/api/<question_id>/parent', methods=['GET'])
def getParentQuestionId(question_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT row_to_json(t) FROM('
                'SELECT Parent_question_id '
                'FROM Question_logic AS ql '
                'WHERE ql.Child_question_id=%s'
                ') t',
                (question_id,)
                )
    parentQuestionid = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'msg': 'success', 'data': parentQuestionid})


@ app.route('/api/<question_id>/<option_id>/child', methods=['GET'])
def getChildQuestionId(question_id, option_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT row_to_json(t) FROM('
                'SELECT Child_question_id '
                'FROM Question_logic AS ql '
                'WHERE ql.Parent_question_id=%s AND ql.Parent_option_id=%s'
                ') t',
                (question_id, option_id)
                )
    parentQuestionid = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'msg': 'success', 'data': parentQuestionid})


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=9999)
