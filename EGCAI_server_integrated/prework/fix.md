1. last_login_time

2. with cursor():

  ```python
  @ app.route('/api/basic_info/<user_id>', methods=['GET'])
     def getBasicInfo(user_id):
     conn = get_db_connection()
     if not conn:
         return jsonify({'message': 'Database Connection Error'}), 500
  
     with conn.cursor() as cur:
         cur.execute('SELECT row_to_json(t) FROM (SELECT * FROM users WHERE user_id = %s) t', (user_id,))
         basic_info = cur.fetchone()
  
     if basic_info is None:
         return jsonify({'message': 'No user info found for the provided user ID', 'error': {'type': 'NoUserInfo', 'description': '无该用户'}}), 404
  
     return jsonify({'message': 'success', 'data': basic_info}), 200
  ```

3. ```json
   @ app.route('/api/surveys/<survey_id>/new_survey_instance', methods=['POST'])
   def createSurveyInstance(survey_id):
       survey_id = int(survey_id)
       response = request.get_json()
       user_id = response.get('user_id')
   ```

4. 

```json
with get_db_connection() as conn, conn.cursor() as cur:
    # 检查用户信息是否存在
    cur.execute('SELECT 1 FROM users WHERE user_id = %s', (user_id,))
    if cur.fetchone() is None:
        return jsonify({'message': 'fail', 'error': {'type': 'NoUserInfo', 'description': '无该用户'}}), 404

    # 生成唯一的 response_id
    m = hashlib.sha256()
    user_id_str = str(user_id).encode('utf-8')
    m.update(user_id_str)
    response_id = m.hexdigest()

    # 插入新的 response 记录
    response_data = {
        'current_question_id': 0,
        'survey_id': survey_id,
        'response_id': response_id,
        # 其他需要的字段
    }
    response_sql = json_to_sql({'responses': [response_data]})
    cur.execute(response_sql)
    conn.commit()

    # 获取调查问卷的标题和描述
    cur.execute('SELECT title, description FROM surveys WHERE survey_id = %s', (survey_id,))
    survey_info = cur.fetchone()
    if survey_info is None:
        return jsonify({'message': 'fail', 'error': {'type': 'NoSurveyFound', 'description': '未找到问卷'}}), 404

return jsonify({'message': 'success', 'data': {'response_id': response_id, 'title': survey_info[0], 'description': survey_info[1]}})
```

4. question_responses改question_answers