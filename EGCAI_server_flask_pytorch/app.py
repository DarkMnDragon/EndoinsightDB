import os
import json
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify
import image_process
from flask_cors import CORS
from utils.json_to_sql import json_to_sql
import hashlib

app = Flask(__name__)
CORS(app)


def check(cur, table, id_name, table_id):
    cur.execute('select row_to_json(t) from('
                'select %s from %s where %s.%s=%s'
                ') t', (id_name, table, table, id_name, table_id,))
    res = cur.fetchall()
    if(len(res) == 0):
        return 0
    else:
        return 1


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='endo',
                            user='endo',
                            password='123456')
    return conn


@ app.route('/api/surveys/<survey_id>/end_survey', methods=['POST'])
def end_survey(survey_id):
    response = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    if(check(cur, 'surveys', 'survey_id', survey_id) == 0 or
       check(cur, 'users', 'user_id', user_id) == 0 or
       check(cur, 'responses', 'response_id', response_id) == 0
       ):
        cur.close()
        conn.close()
        error_info = {'type': 'InvalidData', 'description': '提供数据不正确'}
        return jsonify({'message': 'fail', 'error': error_info})
    # todo
    return jsonify({'message': 'success'})


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/previous_question',
            methods=['POST'])
def getPreviousQuestion(survey_id, question_id):
    response = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and response.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})
    cur.execute('select question_response_id from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, current_question_id)
                )
    question_response_id = cur.fetchall()[0]
    cur.execute('SELECT list_id, parent_question_id '
                'FROM lists '
                'WHERE lists.child_question_id=%s AND'
                ' lists.response_id=%s',
                (question_id, response_id)
                )
    list_id, previous_question_id = cur.fetchall()

    cur.execute('select question_id, type_id from questions '
                'where questions.question_id=%s',
                (previous_question_id, )
                )
    question_text, type_id = cur.fetchall()
    cur.execute('select * from options '
                'where options.question_id=%s',
                (previous_question_id,)
                )
    previous_question_options = cur.fetchall()
    option_num = len(previous_question_options)
    options_text = []
    for previous_question_option in previous_question_options:
        options_text.append(previous_question_option[1])
    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, previous_question_id)
                )
    question_response_before = cur.fetchall()
    hist_text = question_response_before[1]
    cur.execute('select * from selected_option '
                'where question_response_id=%s',
                (question_response_before[0], )
                )
    hist_options = []
    options_before = cur.fetchall()
    for option_before in options_before:
        hist_options.append(option_before[2])
    cur.execute('select first_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    first_question_id = cur.fetchall()[0]
    if first_question_id == previous_question_id:
        is_first_question = True
    else:
        is_first_question = False

    data = {
        'question_id': previous_question_id,
        'question_text': question_text,
        'type_id': type_id,
        'option_num': option_num,
        'options_text': options_text,
        'hist_text': hist_text,
        'hist_options': hist_options,
        'is_first_question': is_first_question
    }
    cur.execute('delete table lists where list_id=%s',
                (list_id,)
                )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'msg': 'success', 'data': data})


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/next_question',
            methods=['POST'])
def getNextQuestion(survey_id, question_id):
    response = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})
    cur.execute('select type_id from questions '
                'where questions.question_id=%s',
                (current_question_id, )
                )
    type_id = cur.fetchall()[0]
    cur.execute('select question_response_id from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, current_question_id)
                )
    question_response_id = cur.fetchall()[0]
    cur.execute('select option_id from selected_option '
                'where question_response_id=%s',
                (question_response_id, )
                )
    option_id = cur.fetchall()
    cur.execute('SELECT Child_question_id '
                'FROM Question_logic AS ql '
                'WHERE ql.Parent_question_id=%s AND'
                ' ql.Parent_option_id=%s',
                (question_id, option_id)
                )
    next_question_id = cur.fetchall()
    cur.execute('select question_id, type_id from questions '
                'where questions.question_id=%s',
                (next_question_id, )
                )
    question_text, type_id = cur.fetchall()
    cur.execute('select * from options '
                'where options.question_id=%s',
                (next_question_id,)
                )
    next_question_options = cur.fetchall()
    option_num = len(next_question_options)
    options_text = []
    for next_question_option in next_question_options:
        options_text.append(next_question_option[1])
    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, next_question_id)
                )
    question_response_before = cur.fetchall()
    if len(question_response_before) == 0:
        submit_before = False
        hist_text = ''
        hist_options = []
    else:
        submit_before = True
        hist_text = question_response_before[1]
        cur.execute('select * from selected_option '
                    'where question_response_id=%s',
                    (question_response_before[0], )
                    )
        hist_options = []
        options_before = cur.fetchall()
        for option_before in options_before:
            hist_options.append(option_before[2])
    cur.execute('select last_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    last_question_id = cur.fetchall()[0]
    if last_question_id == next_question_id:
        is_last_question = True
    else:
        is_last_question = False

    data = {
        'question_id': next_question_id,
        'question_text': question_text,
        'type_id': type_id,
        'option_num': option_num,
        'options_text': options_text,
        'submit_before': submit_before,
        'hist_text': hist_text,
        'hist_options': hist_options,
        'is_last_question': is_last_question
    }
    m = hashlib.sha256()
    question_id_encode = current_question_id.encode('utf-8')
    next_question_id_encode = next_question_id.encode('utf-8')
    response_id_encode = response_id.encode('utf-8')
    m.update(question_id_encode)
    m.update(next_question_id_encode)
    m.update(response_id_encode)
    list_id = m.hexdigest()
    cur.execute('insert table lists value (%s, %s, %s, %s)',
                list_id, current_question_id, next_question_id, response_id
                )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'msg': 'success', 'data': data})


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/submit',
            methods=['POST'])
def submit(survey_id, question_id):
    response = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    if(check(cur, 'surveys', 'survey_id', survey_id) == 0 or
       check(cur, 'questions', 'question_id', question_id) == 0 or
       check(cur, 'users', 'user_id', response.get('user_id')) == 0 or
       check(cur, 'responses', 'response_id', response.get('response_id')) == 0 or
       check(cur, 'input_type', 'type_id', response.get('type_id')) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'InvalidData', 'description': '提供数据不正确'}
        return jsonify({'message': 'fail', 'error': error_info})
    if not response.get('text'):
        error_info = {'type': 'EmptyData', 'description': '没有填写答案'}
        return jsonify({'message': 'fail', 'error': error_info})
    m = hashlib.sha256()
    response_id_encode = response.get('response_id').encode('utf-8')
    question_id_encode = response.get('question_id').encode('utf-8')
    m.update(response_id_encode)
    m.update(question_id_encode)
    question_response_id = m.hexdigest()
    cur.execute('select question_response_id from question_responses '
                'where question_response_id=%s',
                (question_response_id,)
                )
    submit_before = cur.fetchall()
    if len(submit_before) != 0:
        cur.execute('begin transaction')
        conn.commit()
        cur.execute('delete from question_responses where '
                    'question_response_id=%s',
                    (question_response_id,)
                    )
        conn.commit()
        question_response = {
            'question_response_id': question_response_id,
            'answer': response.get('text'),
            'response_id': response.get('response_id'),
            'question_id': question_id
        }
        question_response_sql = json_to_sql(jsonify({'question_response':
                                                     question_response}))

        cur.execute(question_response_sql)
        conn.commit()
        cur.execute('commit transaction')
        conn.commit()
    else:
        question_response = {
            'question_response_id': question_response_id,
            'answer': response.get('text'),
            'response_id': response.get('response_id'),
            'question_id': question_id
        }
        question_response_sql = json_to_sql(jsonify({'question_response':
                                                     question_response}))
        cur.execute(question_response_sql)
    if response.get('type_id') == 1 or response.get('type_id') == 2:
        cur.execute('select row_to_json(t) from('
                    'select * from options where options.question_id=%s'
                    ' order by option_id ASC'
                    ') t', (question_id,))
        options = cur.fetchall()
        for option in response.get('selected_options'):
            m = hashlib.sha256()
            question_response_encode = question_response_id.encode('utf-8')
            option_id_encode = options[option].get('option_id').encode('utf-8')
            m.update(question_response_encode)
            m.update(option_id_encode)
            selected_option_id = m.hexdigest()

            select_option = {
                'selected_option_id': selected_option_id,
                'question_response_id': question_response_id,
                'option_id': options[option].get('option_id')
            }
            select_option_sql = json_to_sql(
                jsonify({'selected_option': select_option}))
            cur.execute(select_option_sql)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'success'})


@ app.route('/api/surveys/<survey_id>/new_survey_instance', methods=['POST'])
def createSurveyInstance(survey_id):
    response = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select row_to_json(t) from('
                'select * from users where users.user_id=%s'
                ') t', (response.get('user_id'),))
    basic_info = cur.fetchall()
    if(len(basic_info) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'NoUserInfo', 'description': '无该用户'}
        return jsonify({'message': 'fail', 'error': error_info})
    cur.execute('select first_question_id from surveys where surveys.survey_id=%s'
                ')t', (survey_id,))
    first_question_id = cur.fetchall()[0]
    m = hashlib.sha256()
    user_id = response.get('user_id').encode('utf-8')
    time = response.get('time').encode('utf-8')
    m.update(user_id)
    m.update(time)
    response_id = m.hexdigest()
    response['current_question_id'] = first_question_id
    response['survey_id'] = survey_id
    response['response_id'] = response_id
    response_sql = json_to_sql(jsonify({'response': response}))
    cur.execute(response_sql)
    cur.execute('select row_to_json(t) from('
                'select title, description from surveys where surveys.survey_id=%s'
                ')t', (survey_id,))
    msg = cur.fetchall()
    msg['response_id'] = response_id
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'success', 'data': msg})


@ app.route('/api/basic_info', methods=['POST'])
def postBasicInfo():
    response = request.get_json()
    response_sql = json_to_sql(jsonify({'users': response}))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(response_sql)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'success'})


@ app.route('/api/basic_info/<user_id>', methods=['GET'])
def getBasicInfo(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select row_to_json(t) from('
                'select * from users where users.user_id=%s'
                ') t', (user_id,))
    basic_info = cur.fetchall()
    if(len(basic_info) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'NoUserInfo', 'description': '无该用户'}
        return jsonify({'message': 'fail', 'error': error_info})

    cur.close()
    conn.close()
    return jsonify({'message': 'seccess', 'data': basic_info})


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=9999)
