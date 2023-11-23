import os
import json
import traceback
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify
# import image_process
from flask_cors import CORS
from utils.json_to_sql import json_to_sql
import hashlib

app = Flask(__name__)
CORS(app)

app.debug = True

@app.errorhandler(Exception)
def handle_exception(e):
    # 获取完整的错误堆栈
    tb = traceback.format_exc()

    # 构建错误响应
    response = {
        "error": str(e),
        "traceback": tb,
        "description": "服务器端发生错误，请检查服务器日志以获取更多信息。"
    }
    return jsonify(response), 500

def check(cur, table, id_name, table_id):
    s = 'select %s from %s where %s.%s=' % (id_name, table, table, id_name)
    if type(table_id) == int:
        s = s + str(table_id)  # 如果table_id是整数，直接添加
    else:
        s = s + '\'' + table_id + '\''  # 如果table_id不是整数，添加引号后再添加
    cur.execute(s)
    res = cur.fetchall()
    # 检查查询结果，如果没有记录，返回0；否则返回1
    if (len(res) == 0):
        return 0
    else:
        return 1


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='Endo',
                            user='endo',
                            password='endo')
    return conn


@ app.route('/api/surveys/<survey_id>/end_survey/', methods=['POST'])
def end_survey(survey_id):
    response = request.get_json()
    survey_id = int(survey_id)  # 将survey_id转换为整数
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    # 检查survey_id, user_id, 和response_id是否在相应的数据库表中存在
    if (check(cur, 'surveys', 'survey_id', survey_id) == 0 or
       check(cur, 'users', 'user_id', user_id) == 0 or
       check(cur, 'responses', 'response_id', response_id) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'InvalidData', 'description': '提供数据不正确'}
        return jsonify({'message': 'fail', 'error': error_info})   # 返回错误信息

    cur.execute('select last_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    cur_list = cur.fetchall()
    last_question_id = cur_list[0][0]
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    cur_list = cur.fetchall()
    current_question_id = cur_list[0][0]
    if current_question_id != last_question_id:
        error_info = {'type': 'InvalidData', 'description': '未填写所有问题，无法交卷'}
        return jsonify({'message': 'fail', 'error': error_info})
    else:
        current_question_id = -1
        cur.execute('update responses set current_quesion_id=-1',
                    ' where response_id=%s', (response_id, ))
        conn.commit()

    cur.close()
    conn.close()
    return jsonify({'message': 'success'})  # 返回成功信息


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/previous_question',
            methods=['POST'])
def getPreviousQuestion(survey_id, question_id):
    response = request.get_json()
    survey_id = int(survey_id)
    question_id = int(question_id)
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    # 获取当前问题的 ID
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()[0][0]
    # 如果当前问题 ID 与请求中的问题 ID 不匹配，则返回错误信息
    if current_question_id != question_id:
        cur.close()
        conn.close()
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})

    cur.execute('select first_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    first_question_id = cur.fetchall()[0][0]
    if current_question_id == first_question_id:
        error_info = {'type': 'InvalidData', 'description': '前面没有题目啦'}
        cur.close()
        conn.close()
        return jsonify({'message': 'fail', 'error': error_info})

    # 获取上一个问题的 ID 和链表ID
    cur.execute('SELECT list_id, parent_question_id '
                'FROM lists '
                'WHERE lists.child_question_id=%s AND'
                ' lists.response_id=%s',
                (question_id, response_id)
                )
    cur_list = cur.fetchall()[0]
    list_id, previous_question_id = cur_list

    # 获取上一个问题的文本和类型
    cur.execute('select question_text, type_id from questions '
                'where questions.question_id=%s',
                (previous_question_id, )
                )
    cur_list = cur.fetchall()[0]
    question_text, type_id = cur_list

    # 获取上一个问题的选项
    cur.execute('select * from options '
                'where options.question_id=%s',
                (previous_question_id,)
                )
    cur_list = cur.fetchall()
    previous_question_options = cur_list
    option_num = len(previous_question_options)
    options_text = []
    for previous_question_option in previous_question_options:
        options_text.append(previous_question_option[1])

    # 获取之前选择的答案
    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, previous_question_id)
                )
    question_response_before = cur.fetchall()[0]
    hist_text = question_response_before[1]

    # 获取之前选择的选项
    cur.execute('select * from selected_option '
                'where question_response_id=%s',
                (question_response_before[0], )
                )
    hist_options = []
    options_before = cur.fetchall()
    for option_before in options_before:
        hist_options.append(option_before[2])

    # 检查是否为第一个问题
    if first_question_id == previous_question_id:
        is_first_question = True
    else:
        is_first_question = False

    # 准备返回的数据
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

    # 更新链表
    cur.execute('delete from lists where list_id=%s',
                (list_id,)
                )
    conn.commit()

    # 更新当前问题编号
    cur.execute('update responses '
                'set current_question_id=%s '
                'where response_id=%s', (previous_question_id, response_id)
                )
    conn.commit()
    cur.close()
    conn.close()

    # 返回成功消息和数据
    return jsonify({'msg': 'success', 'data': data})


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/next_question',
            methods=['POST'])
def getNextQuestion(survey_id, question_id):
    response = request.get_json()
    survey_id = int(survey_id)
    question_id = int(question_id)
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')

    # 获取当前问题的 ID
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    cur_list = cur.fetchall()
    current_question_id = cur_list[0][0]

    # 如果当前问题 ID 与请求中的问题 ID 不匹配，则返回错误信息
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        cur.close()
        conn.close()
        return jsonify({'message': 'fail', 'error': error_info})

    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, current_question_id)
                )
    cur_list = cur.fetchall()
    question_response_before = ()
    if cur_list:
        question_response_before = cur_list[0]
    if current_question_id != 0 and len(question_response_before) == 0:
        error_info = {'type': "Invalid Operation", 'description': '未提交本题答案'}
        cur.close()
        conn.close()
        return jsonify({'message': 'fail', 'error': error_info})
    cur.execute('select last_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    cur_list = cur.fetchall()
    last_question_id = cur_list[0][0]
    if current_question_id == last_question_id:
        error_info = {'type': "InvalidData", 'description': '后面没有题目啦'}
        cur.close()
        conn.close()
        return jsonify({'message': 'fail', 'error': error_info})
    # 根据当前问题 ID 获取下一个问题的 ID
    if current_question_id == 0:
        # 如果当前问题 ID 为 0，则获取第一个问题的 ID
        cur.execute('select first_question_id from surveys where '
                    'surveys.survey_id={}'.format(survey_id,))
        first_question_id = cur.fetchall()
        next_question_id = first_question_id[0][0]
    else:
        # 否则，根据逻辑确定下一个问题的 ID
        cur.execute('select type_id from questions '
                    'where questions.question_id=%s',
                    (current_question_id, )
                    )
        type_id = cur.fetchall()[0][0]
        cur.execute('select question_response_id from question_responses '
                    'where response_id=%s and question_id=%s',
                    (response_id, current_question_id)
                    )
        question_response_id = cur.fetchall()[0][0]
        cur.execute('select option_id from selected_option '
                    'where question_response_id=%s',
                    (question_response_id, )
                    )
        cur_list = cur.fetchall()
        if cur_list:
            option_id = cur_list[0][0]
        else:
            option_id = 0
        cur.execute('SELECT Child_question_id '
                    'FROM Question_logic AS ql '
                    'WHERE ql.Parent_question_id=%s AND'
                    ' ql.Parent_option_id=%s',
                    (question_id, option_id)
                    )
        next_question_id = cur.fetchall()[0][0]

    # 获取下一个问题的详细信息
    cur.execute('select question_text, type_id from questions '
                'where questions.question_id=%s',
                (next_question_id, )
                )
    cur_list = cur.fetchall()
    question_text, type_id = cur_list[0]
    cur.execute('select * from options '
                'where options.question_id=%s',
                (next_question_id,)
                )
    next_question_options = cur.fetchall()
    option_num = len(next_question_options)
    options_text = []
    for next_question_option in next_question_options:
        options_text.append(next_question_option[1])

    # 获取之前提交的答案，如果有的话
    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, next_question_id)
                )
    cur_list = cur.fetchall()
    question_response_before = ()
    if cur_list:
        question_response_before = cur_list[0]
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

    # 检查是否为最后一个问题
    if last_question_id == next_question_id:
        is_last_question = True
    else:
        is_last_question = False

    # 准备返回的数据
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

    # 更改当前问题编号
    cur.execute('update responses '
                'set current_question_id=%s '
                'where response_id=%s', (next_question_id, response_id)
                )
    conn.commit()

    # 更新链表
    if current_question_id != 0:
        m = hashlib.sha256()
        question_id_encode = str(current_question_id).encode('utf-8')
        next_question_id_encode = str(next_question_id).encode('utf-8')
        response_id_encode = response_id.encode('utf-8')
        m.update(question_id_encode)
        m.update(next_question_id_encode)
        m.update(response_id_encode)
        list_id = m.hexdigest()
        list_ = []
        list_dict = {}
        list_dict['list_id'] = list_id
        list_dict['parent_question_id'] = current_question_id
        list_dict['child_question_id'] = next_question_id
        list_dict['response_id'] = response_id
        list_.append(list_dict)
        list_sql = json_to_sql({'lists': list_})
        cur.execute(list_sql)
        conn.commit()
    cur.close()
    conn.close()
    return jsonify({'msg': 'success', 'data': data})


@app.route('/api/surveys/<survey_id>/questions/<question_id>/submit',
           methods=['POST'])
def submit(survey_id, question_id):
    response = request.get_json()
    survey_id = int(survey_id)
    question_id = int(question_id)
    user_id = response.get('user_id')
    response_id = response.get('response_id')
    type_id = response.get('type_id')
    conn = get_db_connection()
    cur = conn.cursor()

    # 检查是否在相应的数据库表中存在
    if (check(cur, 'surveys', 'survey_id', survey_id) == 0 or
       check(cur, 'questions', 'question_id', question_id) == 0 or
       check(cur, 'users', 'user_id', user_id) == 0 or
       check(cur, 'responses', 'response_id', response_id) == 0 or
       check(cur, 'input_type', 'type_id', type_id) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'InvalidData', 'description': '提供数据不正确'}
        return jsonify({'message': 'fail', 'error': error_info})

    # 检查是否有答案文本
    if not response.get('text'):
        error_info = {'type': 'EmptyData', 'description': '没有填写答案'}
        return jsonify({'message': 'fail', 'error': error_info})
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()
    current_question_id = current_question_id[0][0]

    # 检查当前问题 ID 是否匹配
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})

    # 生成问题回应的唯一 ID
    m = hashlib.sha256()
    response_id_encode = response.get('response_id').encode('utf-8')
    question_id_encode = str(question_id).encode('utf-8')
    m.update(response_id_encode)
    m.update(question_id_encode)
    question_response_id = m.hexdigest()

    # 检查是否之前已提交过答案
    cur.execute('select question_response_id from question_responses '
                'where question_response_id=%s',
                (question_response_id,)
                )
    submit_before = cur.fetchall()
    if len(submit_before) != 0:
        # 如果之前提交过，则先删除旧的答案和选项
        cur.execute('begin transaction')
        conn.commit()
        cur.execute('delete from selected_option where '
                    'question_response_id=%s',
                    (question_response_id,)
                    )
        conn.commit()
        cur.execute('delete from question_responses where '
                    'question_response_id=%s',
                    (question_response_id,)
                    )
        conn.commit()

        # 插入新的答案
        question_response = {
            'question_response_id': question_response_id,
            'answer': response.get('text'),
            'response_id': response.get('response_id'),
            'question_id': question_id
        }
        response_list = []
        response_list.append(question_response)
        question_response_sql = json_to_sql({'question_responses':
                                             response_list})

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
        response_list = []
        response_list.append(question_response)
        question_response_sql = json_to_sql({'question_responses':
                                             response_list})
        cur.execute(question_response_sql)
        conn.commit()

    # 如果问题类型是选择题，则插入选择的选项
    if response.get('type_id') == 1 or response.get('type_id') == 2:
        cur.execute('select row_to_json(t) from('
                    'select * from options where options.question_id=%s'
                    ' order by option_id ASC'
                    ') t', (question_id,))
        options = cur.fetchall()
        for option in response.get('selected_options'):
            m = hashlib.sha256()
            question_response_encode = question_response_id.encode('utf-8')
            option_id_encode = str(
                options[option][0].get('option_id')).encode('utf-8')
            m.update(question_response_encode)
            m.update(option_id_encode)
            selected_option_id = m.hexdigest()

            select_option = {
                'selected_option_id': selected_option_id,
                'question_response_id': question_response_id,
                'option_id': options[option][0].get('option_id')
            }
            response_list = []
            response_list.append(select_option)
            select_option_sql = json_to_sql(
                {'selected_option': response_list})
            print(response_list)
            cur.execute(select_option_sql)
            conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'success'})


@app.route('/api/surveys/<survey_id>/new_survey_instance', methods=['POST'])
def createSurveyInstance(survey_id):
    
    def jsonify_error(error_type, description):
        return jsonify({'message': 'fail', 'error': {'type': error_type, 'description': description}}), 403
    
    def user_exists(cursor, user_id):
        cursor.execute('SELECT 1 FROM users WHERE user_id = %s', (user_id,))
        return cursor.fetchone() is not None
    
    def check_response_stop(cursor, user_id):
        cursor.execute('SELECT * FROM responses WHERE user_id=%s AND current_question_id != -1', (user_id,))
        return cursor.fetchone()
    
    def generate_response_id(user_id, timestamp):
        m = hashlib.sha256()
        m.update(user_id.encode('utf-8'))
        m.update(timestamp.encode('utf-8'))
        return m.hexdigest()
    
    def handle_reconnection(cur, response_stopped, response, survey_id):
        response_id, current_question_id = response_stopped[0], response_stopped[4]
        print(f"Reconnection, response_id={response_id}, current_question_id={current_question_id}")

        if current_question_id == 0:
            return initialize_response(cur, response, survey_id, response_id, reconnection=True)

        return retrieve_question_data(cur, survey_id, response_id, current_question_id)
    
    def initialize_response(cur, response, survey_id, response_id, reconnection=False):
        response['current_question_id'] = 0
        response['survey_id'] = survey_id
        response['response_id'] = response_id
        response_sql = json_to_sql({'responses': [response]})
        if not reconnection:
            cur.execute(response_sql)

        cur.execute('SELECT title, description FROM surveys WHERE survey_id = %s', (survey_id,))
        survey_info = cur.fetchone()

        if survey_info is None:
            return jsonify_error('NoSurvey', '调查问卷不存在')

        return jsonify({
            'message': 'success',
            'data': {
                'response_id': response_id,
                'type': 'Create New Response',
                'title': survey_info[0],
                'description': survey_info[1]
            }
        })

    def handle_new_response(cur, response, user_id, survey_id):
        response_id = generate_response_id(user_id, response.get('time'))
        return initialize_response(cur, response, survey_id, response_id, reconnection=False)
    
    def retrieve_question_data(cur, survey_id, response_id, current_question_id):
        # 获取当前问题的详细信息
        cur.execute('SELECT question_text, type_id FROM questions WHERE question_id = %s', (current_question_id, ))
        question_info = cur.fetchone()
        question_text, type_id = question_info

        # 获取问题的所有选项
        cur.execute('SELECT option_text FROM options WHERE question_id = %s', (current_question_id, ))
        options = cur.fetchall()
        options_text = [option[0] for option in options]

        # 检查之前是否已经提交过答案
        cur.execute('SELECT * FROM question_responses WHERE response_id = %s AND question_id = %s', (response_id, current_question_id))
        previous_response = cur.fetchone()
        submit_before, hist_text, hist_options = False, '', []
        if previous_response:
            submit_before = True
            hist_text = previous_response[1]

            # 获取之前选择的选项
            cur.execute('SELECT option_id FROM selected_option WHERE question_response_id = %s', (previous_response[0], ))
            selected_options = cur.fetchall()
            hist_options = [option[0] for option in selected_options]

        # 检查是否为最后一个问题
        cur.execute('SELECT last_question_id FROM surveys WHERE survey_id = %s', (survey_id, ))
        is_last_question = cur.fetchone()[0] == current_question_id

        # 检查是否为第一个问题
        cur.execute('SELECT first_question_id FROM surveys WHERE survey_id = %s', (survey_id, ))
        is_first_question = cur.fetchone()[0] == current_question_id

        # 构建返回的数据
        data = {
            'type': 'Reconnection',
            'response_id': response_id,
            'question_id': current_question_id,
            'question_text': question_text,
            'type_id': type_id,
            'options_text': options_text,
            'submit_before': submit_before,
            'hist_text': hist_text,
            'hist_options': hist_options,
            'is_last_question': is_last_question,
            'is_first_question': is_first_question
        }

        return jsonify({
            'message': 'success',
            'data': data
        })

    response = request.get_json()
    survey_id = int(survey_id)
    user_id = response.get('user_id')
    jargon = response.get('jargon')
    if jargon != 'DeepLeiarning':
        return jsonify_error('InvalidAccess', '非法访问')
    if 'jargon' in response:
        del response['jargon']

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            if not user_exists(cur, user_id):
                return jsonify_error('NoUserInfo', '无该用户')

            response_stopped = check_response_stop(cur, user_id)
            if response_stopped:
                return handle_reconnection(cur, response_stopped, response, survey_id)
            else:
                return handle_new_response(cur, response, user_id, survey_id)

@app.route('/api/update_basic_info', methods=['POST'])
def updateBasicInfo():
    data = request.get_json()
    user_id = data.get('user_id')
    jargon = data.get('jargon')

    # 验证 jargon
    if jargon != 'DeepLeiarning':
        return jsonify({'message': 'fail', 'error': {'type': 'InvalidAccess', 'description': '非法访问'}}), 403

    conn = get_db_connection()
    cur = conn.cursor()

    # 检查 user_id 是否存在
    cur.execute('SELECT 1 FROM users WHERE user_id = %s', (user_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({'message': 'fail', 'error': {'type': 'NoUser', 'description': '用户不存在'}}), 404

    # 删除 data 中的 jargon 键
    if 'jargon' in data:
        del data['jargon']

    # 准备 SQL 更新语句
    try:
        update_parts = ', '.join(
            [f"{key} = %s" for key in data if key != 'user_id'])
        values = tuple(data[key] for key in data if key != 'user_id')
        response_sql = f"UPDATE users SET {update_parts} WHERE user_id = %s;"
        values += (data['user_id'],)
        cur.execute(response_sql, values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'message': 'fail', 'error': {'type': 'SQL Error', 'description': str(e)}}), 500

    cur.execute(
        'SELECT row_to_json(t) FROM (SELECT * FROM users WHERE user_id=%s) t', (user_id,))
    basic_info = cur.fetchone()

    cur.close()
    conn.close()

    # 检查是否查询到数据
    if basic_info:
        # 直接返回第一个元素，因为 fetchone() 返回的是单个结果
        return jsonify({'message': 'success', 'data': basic_info[0]}), 200
    else:
        # 处理未查询到数据的情况
        return jsonify({'message': 'fail', 'error': 'No data found for user_id'}), 404


@app.route('/api/get_basic_info', methods=['POST'])
def getBasicInfo():
    data = request.get_json()
    user_id = data.get('user_id')
    jargon = data.get('jargon')
    # 验证 jargon
    if jargon != 'DeepLeiarning':
        return jsonify({'message': 'fail', 'error': {'type': 'InvalidAccess', 'description': '非法访问'}}), 403

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # 执行 SQL 查询以获取指定用户 ID 的基本信息
        cur.execute(
            'SELECT row_to_json(t) FROM (SELECT * FROM users WHERE user_id=%s) t', (user_id,))
        basic_info = cur.fetchall()

        # 检查是否找到了用户信息
        if len(basic_info) == 0:
            # 用户不存在，创建新用户
            cur.execute('INSERT INTO users (user_id) VALUES (%s)', (user_id,))
            conn.commit()
            info = {'type': 'UserCreated', 'description': '新用户创建成功'}
            return jsonify({'message': 'success', 'data': info}), 201

        else:
            # 用户存在，返回用户信息
            return jsonify({'message': 'success', 'data': basic_info[0]}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'fail', 'error': {'type': 'DatabaseError', 'description': str(e)}}), 500

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
