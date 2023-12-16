## API：

1. 获取用户id - 绑定小程序启动。不在客户端直接使用 `openid`，而是用服务器生成的令牌`user_id`来识别用户。

   1. api： `POST base_url/api/login`

   2. 请求体参数：`res.code`

      ```json
      {
      	"code": "0c3NikGa1g2IyG0hK2Ga1zAfNS3NikGw"
      }
      ```

   3. 响应体参数：返回`user_id`

      ```json
      {
          "message": "success",
           "error": {
              "type": ""
          },
          "data":{
          	"user_id": "123456"
          }
      }
      ```

2. 获取用户基本信息 - 绑定首页个人基础信息按钮 ：如果为第一次创建（即在数据库中没有找到该 `user_id`），在数据库中创建 `user_id` 并返回；否则调用数据库记录，返回曾经填写的个人信息

   1. api ：`POST base_url/api/get_basic_info`

   2. 请求体参数：`user_id`

      ```JSON
      {
      	"user_id": "123456",
        	"jargon": "DeepLeiarning"
      }
      ```

   3. 响应体参数：返回数据库中的曾经记录的个人信息。如果没有信息，返回错误

      | 参数名                     | 类型    | 描述       |
      | -------------------------- | ------- | ---------- |
      | name                       | Text    | 用户姓名   |
      | sex                        | Text    | 用户性别   |
      | nation                     | Text    | 用户民族   |
      | ID_number                  | integer | 身份证号   |
      | birthday                   | Date    | 生日年月日 |
      | phone_number               | integer | 用户手机号 |
      | family_member_phone_number | integer | 家属手机号 |
      | homeplace                  | Text    | 出生地     |
      
      ```json
      // 找到用户信息的响应
      {
          "message": "success",
           "error": {
              "type": ""
          },
          "data":{
          	"name": "xxx",
          	"sex": "男",
              "nation": "汉族",
              "ID_number": "xxx",
              "birthday": "2002-12-23",
              "phone_number": "xxx",
              "family_member_phone_number": "xxx",
              "homeplace": "四川省成都市"
          }
      }
      
      // 没有找到用户信息的响应
      // 添加 HTTP 响应码
      {
          "data": {
          "description": "新用户创建成功",
          "type": "UserCreated"
          },
          "message": "success"
      }
      ```
      
      基本信息的填空栏目直接写死在前端 wxml 中，服务器返回的直接是历史个人信息

3. 更新/提交用户基本信息 - 绑定个人基础信息页面的**提交按钮**，此时保证服务器端已经创建了 `user_id`

   1. api ：`POST base_url/api/update_basic_info`

   2. 请求体参数：

      | 参数名                     | 类型    | 描述                                    |
      | -------------------------- | ------- | --------------------------------------- |
      | jargon                     | Text    | 字符串“DeepLeiarning”，用于校验安全访问 |
      | user_id                    | Text    | 微信提供的 user_id                      |
      | name                       | Text    | 用户姓名                                |
      | sex                        | Text    | 用户性别                                |
      | nation                     | Text    | 用户民族                                |
      | ID_number                  | integer | 身份证号                                |
      | birthday                   | Date    | 生日年月日                              |
      | phone_number               | integer | 用户手机号                              |
      | family_member_phone_number | integer | 家属手机号                              |
      | homeplace                  | Text    | 出生地                                  |
      
      ```json
      {
          "jargon": "DeepLeiarning",
          "user_id": "123456",
          "name": "xxx",
          "sex": "男",
          "nation": "汉族",
          "ID_number": "xxx",
          "birthday": "2002-12-23",
          "phone_number": "xxx",
          "family_member_phone_number": "xxx",
          "homeplace": "四川省成都市"
      }
      ```
      
   3. 响应体参数：

      ```json
      {
          "data": {
              "jargon": "DeepLeiarning",
              "user_id": "123456",
              "name": "xxx",
              "sex": "男",
              "nation": "汉族",
              "ID_number": "xxx",
              "birthday": "2002-12-23",
              "phone_number": "xxx",
              "family_member_phone_number": "xxx",
              "homeplace": "四川省成都市"
          },
          "message": "success",
      }
      
      {
          "message": "fail",
          "error": {
          	"type": "NoUser",
          	"description": "用户不存在"	
          }
      }
      ```
      
      

4. 获取预测疾病问卷首页 - 绑定引导页上某个疾病问卷按钮，创建问卷实例（数据库端），服务器端返回问卷 `response_id`，同时初始化当前问题 `current_question_id`

   1. api：`POST base_url/api/surveys/{survey_id}/new_survey_instance`

   2. 请求体参数：`user_id, time`

      - `survey_id` 代表问卷类型，即一种问卷一个 `id`

      ```json
      {
          "jargon": "DeepLeiarning",
          "user_id": "123456",
          "time": "2023-11-14 19:59:00"
      }
      ```

   3. 响应体参数：

      ```json
      // 成功请求问卷
      {
          "message": "success",
          "error": {
              "type": ""
          },
          "data": {
              "type": "Create New Response",
              "title": "疾病预测问卷",
              "description": "请您认真填写以下问题...",
              "response_id": "d90212cd427292d1b04d9353ac08ee75ae126444c2c271aea57da543e018df09" // 服务器生成的新响应ID,注意此处为字符串
          }
      }
      
      // 断线重连
      {
          "message": "success",
          "error": {
              "type": ""
          },
          "data": {
              "type": "Reconnection",
              "response_id": "d90212cd427292d1b04d9353ac08ee75ae126444c2c271aea57da543e018df09", // 问卷中断时的响应id,注意此处为字符串,
              "question_id": 13,
              "question_text": "xxx",
              "type_id": 1,
              "option_num": 4,
              "options_text": ["选项1", "选项2", "选项3", "选项4"],
              "submit_before": true,
              "hist_text": "历史文本回答",
              "hist_options": [1, 3],
              "is_last_question": false,
              "is_first_question": false
          }
      }
      
      // 没有填写基本信息，跳转基本信息填写页面
      {
          "error": {
              "description": "无该用户",
              "type": "NoUserInfo"
          },
          "message": "fail"
      }
      ```

   4. 注意服务器端验证 `user_id` 的合法性

      1. 如果没有 `user_id`，跳转提交基础信息页面，返回 `error - type = NoUserInfo`

   5. 同时在数据库端创建该 `response_id` 的状态 `list`

   6. 断线重连：若用户未点击提交按钮退出了微信小程序，再次打开时不应该再次创建response_id，此时恢复断线时的response_id，得到断线时的lists、current_question_id

5. 提交单题答案 - 绑定上一题/下一题按钮，即每次换题需提交答案

   1. api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/submit`

   3. 请求参数：

      | 参数名           | 类型  | 描述                           |
      | ---------------- | ----- | ------------------------------ |
      | user_id          | Text  | 用户id                         |
      | response_id      | Text  | 响应id                         |
      | type_id          | int   | 题目类型id                     |
      | text             | Text  | 把数字、日期统一为文本传给后端 |
      | selected_options | array | 选择选项数组                   |
      
      ```json
      // 填空题示例
      {
          "user_id": "123456",
          "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf",
          "type_id": 0,
          "text": "xxx",
          "selected_options": []
      }
      
      // 选择题示例
      {
          "user_id": "123456",
          "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf",
          "type_id": 1,
          "text": "Answer_in_Selected_Option",
          "selected_options": [1]
      }
      
      
      ```
      
   4. 响应参数：

      ```json
      // 请求成功
      {
          "message": "success",
          "error": {
              "type": ""
          }
      }
      
      // 请求失败
      {
          "message": "fail",
          "error": {
              "type": "InvalidData",
              "description": "提供的数据不正确" 
          }
          // 后续完善具体错误类型
          //"error": {
          //      "type": "EmptyData",
          //     "description": "没有填写答案" 
          //}
      }
      ```

6. 获取下一题序号、题目和选项 - 绑定：下一题按钮 & 问卷首页的问卷开始按钮。前端逻辑下一题时，先判断提交答案的 `message==success`，否则提示先提交选择当前问题

   1. api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/next_question`

      1. 这里的 `question_id` 为当前问题 `id`，不是显示的 `id`
      2. 前端隐式记录 `question_id`，此处是为了验证

   2. 请求参数：`user_id`, `response_id`

      1. 需要根据这两个 `id` 在数据库唯一查询下一题是什么

         ```json
         {
             "user_id": "123456",
             "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf"
         }
         ```

   3. 响应参数：

   | 参数名           | 类型        | 描述                       |
   | ---------------- | ----------- | -------------------------- |
   | question_id      | int         | 下一题序号                 |
   | question_text    | Text        | 题面                       |
   | type_id          | int         | 题目类型id                 |
   | option_num       | int         | 选择题选项数               |
   | options_text     | array[Text] | 选项题面                   |
   | submit_before    | bool        | 是否已经提交过答案         |
   | hist_text        | Text        | 历史文本回答（如果有）     |
   | hist_options     | array       | 历史选择选项数组（如果有） |
   | is_last_question | bool        | 是否为最后一个问题         |

   ```json
   {
       "message": "success",
       "error": {
           "type": "",
       },
       "data": {
           "question_id": 13,
           "question_text": "xxx",
           "type_id": 1,
           "option_num": 4,
           "options_text": ["选项1", "选项2", "选项3", "选项4"],
           "submit_before": true,
           "hist_text": "历史文本回答",
           "hist_options": [1, 3],
           "is_last_question": false
       }
   }
   
   {
       "message": "fail",
       "error": {
           "type": "InvalidData",
           "description": "后面没有题目啦" 
       }
   }
   {
       "message": "fail",
       "error": {
           "type": "NoMatching",
           "description": "问题编号不匹配" 
       }
   }
   {
       "message": "fail",
       "error": {
           "type": "Invalid Operation",
           "description": "未提交本题答案" 
       }
   }
   ```

   4. 前端判断是否最后一题：

      ```javascript
      function handleQuestionResponse(response) {
          // 显示问题内容
          displayQuestion(response.data.question_text);
      	...
          // 根据是否为最后一题，更新按钮显示
          if (response.data.is_last_question) {
              displaySubmitButton();
          } else {
              displayNextQuestionButton();
          }
      }
      ```

7. 获取上一题序号、题目和选项 - 绑定：上一题按钮 & 问卷首页的问卷开始按钮。前端逻辑上一题时，**不用**判断提交答案的 `message==success`

   1. api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/previous_question`

      1. 这里的 `question_id` 为当前问题 `id`，不是显示的 `id`
      2. 前端隐式记录 `question_id`,此处是为了验证

   2. 请求参数：`user_id`, `response_id`

      1. 需要根据这两个 `id` 在数据库唯一查询上一题是什么

         ```json
         {
             "user_id": "lucasqaq",
             "response_id": "b6c275cd5575de8514918de3ede7673ef696ed35aa201df80afd1931357333e1"
         }
         ```

   3. 响应参数：

      | 参数名            | 类型        | 描述             |
      | ----------------- | ----------- | ---------------- |
      | question_id       | int         | 上一题id         |
      | question_text     | Text        | 题面             |
      | type_id           | int         | 题目类型id       |
      | option_num        | int         | 选择题选项数     |
      | options_text      | array[Text] | 选项题面         |
      | hist_text         | Text        | 历史文本回答     |
      | hist_options      | array       | 历史选择选项数组 |
      | is_first_question | bool        | 是否为第一个问题 |

      ```json
      {
          "message": "success",
          "error": {
              "type": "",
          },
          "data": {
              "pre_question_id": 124,
              "question_text": "xxx",
              "type_id": 2,
              "option_num": 4,
              "options_text": ["选项1", "选项2", "选项3", "选项4"],
              "hist_text": "历史文本回答",
              "hist_options": [1, 3],
              "is_first_question": false
          }
      }
      
      {
          "message": "fail",
          "error": {
              "type": "InvalidData",
              "description": "前面没有题目啦" 
          }
      }
      ```

   4. 前端存下`is_first_question`，如果为真，则不显示上一题按钮

8. 结束本次问卷 - 绑定在结束问卷按钮上，提示已自己检查

   1. api：`POST base_url/api/surveys/{survey_id}/end_survey`

   2. 请求参数：`user_id`, `response_id`

      ```json
      {
          "user_id": "afsd",
          "response_id": "1231sfas"
      }
      ```

   3. 响应参数：

      ```json
      {
          "message" : "success",
          "error": {
              "type": "",
          }
      }
      
      {
          "message": "fail",
          "error": {
              "type": "InvalidData",
              "description": "提供数据不正确" 
          }
      }
      
      {
          "message": "fail",
          "error": {
              "type": "InvalidData",
              "description": "未填写所有问题，无法交卷" 
          }
      }
      ```
      

   
