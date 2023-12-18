# 项目报告

**项目名称：** EndoInsightDB - 消化道疾病智慧数据库

## 项目概述

**开发背景：**

- **医学需求：** 鉴于消化道疾病（如胃炎、胃溃疡、肠炎等）对全球人口健康的普遍影响，本项目旨在提高这些疾病的早期发现和治疗效率。
- **技术驱动：** 利用深度学习技术，特别是生成对抗网络（GAN）和扩散模型，进行消化道内镜图像的风格迁移，以提高诊断准确性和疾病认知。

**项目目的**：

- **疾病预警与诊断：** 构建一个智慧数据库，EndoInsightDB，用于存储、处理并分析与消化道疾病相关的数据，以便于进行疾病预警和辅助诊断。
- **教育与科普：** 通过图像风格迁移技术，将健康消化道内镜图像转换为展示特定病变的图像，以提升公众对消化道疾病的认识。

### 技术架构

**1. 前端应用：**
   - **微信小程序：** 用户界面设计，提供问卷填写、图像上传和健康科普信息查阅功能。
   - **用户识别：** 使用微信小程序提供的 UserID 进行用户识别。

**2. 后端服务：**
   - **Flask 服务器：** 作为微信小程序与数据库之间的中介，处理安全验证、请求解析和数据库交互。
   - **数据库管理：** 存储用户问卷信息、消化道内镜图片及相关处理后的数据。

**3. 深度学习模型：**
   - **疾病风险评估：** 从数据库提取用户问卷数据，使用机器学习模型进行疾病风险评估。
   - **图像预测与转换：** 利用生成扩散模型对胃镜图像进行处理，生成病变图像。
   - **系统性能优化：**利用 GPTuner 在数据库端进行了性能调优。

**4. 数据安全与隐私：**
   - **高效处理：** 数据库设计需保证高效性，以适应大量多源异构数据的处理需求。
   - **安全保密：** 鉴于医疗数据的敏感性，确保所有数据的安全和保密性。

### 项目开发动机

**医学背景：**
- **普遍性与严重性：** 消化道疾病广泛影响全球人口健康，某些疾病可能发展为严重健康问题，如胃癌、肝硬化等。
- **早期诊断的重要性：** 消化内镜作为关键的诊断工具，其早期使用可大大提高治愈率。

**项目前身：**
- **初始应用：** 以华西医院提供的数据为基础，开发了用于消化道内镜图像风格迁移的生成对抗模型。

### 项目应用场景

**华西医院消化内科需求：**
- **数据多样性：** 问卷题型包括单选、多选、填空等，需要数据库能够灵活处理各种数据类型。
- **图像处理：** 存储和处理用户上传的消化道内镜图像及其变换后的图像。

## 数据库设计

### 概念设计

我们采用了基于 E-R 模型的数据库设计方法。为 EndoInsightDB 设计的 ER 图如下：

![ER](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031150789.jpg)

下面是 EndoInsightDB 的 ER 图概述及实体解释：

**实体类型**

- **Surveys（问卷）**: 
  - 属性包括问卷题目、描述、创建日期及首尾问题的 `ID`，用于判断问卷的开始和结束。

- **Question_Type（问题类型）**: 
  - 映射问题类型及其 `ID`，如 `type_id` 为 `0`、`1`、`2`分别代表填空、单选、多选类型。便于用户了解问题类型及其 `ID` 对应关系，同时方便类型的拓展。

- **Questions（问题）**: 
  - 表示问卷中的每个问题，包括问题文本、类型和所属问卷信息。

- **Options（选项）**: 
  - 存储选项内容及其所属问题。适用于单选或多选类型的问题。

- **Question_Logic（跳转逻辑）**: 
  - 管理问卷中的问题跳转逻辑，基于用户的答案和当前问题编号，指定下一个问题的编号。

- **Users（用户）**: 
  - 存储用户基本信息（如姓名、性别、体重等）。`user_id` 使用微信提供的唯一 `ID` 进行识别。

- **Image_Responses（图像响应）**: 
  - 用户上传消化道图像后，系统使用预训练的生成对抗网络生成对应的病变图像。每个响应存储一对图像及其上传时间和用户信息。

- **Responses（问卷响应）**: 
  - 当用户开始回答新问卷时创建。记录用户、问卷、响应时间及当前问题编号。与 `question_answers` 实体关联，记录用户对问卷的答案。

- **Question_Answers（答案表）**: 
  - 记录用户对每个问题的答案。填空题的答案直接存储，选择题的答案存储在 `selected_option` 中。

- **Selected_Option（选择题答案）**: 
  - 存储单选或多选题的答案，每条记录对应单个问题。

- **Lists（答题链表）**: 
  - 记录每个 `response` 的答题顺序，用于后端实现回退到上一题。答完问卷后清空对应记录。

以下为实体间关系的阐述：

1. **Survey 与 Question的关系**：
   - 每个 Survey（问卷）可以包含多个 Question（问题），而每个  Question 只能属于一个 Survey。这是典型的一对多关系。

2. **Question 与 Question_Type的关系**：
   - 每个 Question 只能对应一种 Question_Type（问题类型，如填空、单选、多选），而一个 Question_Type 可以被多个 Question采用。这同样是一对多的关系。

3. **Question 与 Option的关系**：
   - Question 可能有多个 Option（选项），如在单选或多选题中；或者没有 Option，如在填空题中。因此，这是一对多的关系，其中 Question 与 Option 之间的参与是不对等的：每个 Option 必须属于一个 Question（强制参与），但 Question 可以没有Option（非强制参与）。

4. **Survey 与 Response的关系**：
   - 一个 Survey 可能收到来自多个或单个 User 的 Response（响应），或者没有 Response。每个 Response 只对应一个 Survey，形成一对多的强制参与关系。

5. **User 与 Response的关系**：
   - 一个 User 可能产生多个 Response ，但每个 Response 必定由一个特定的 User 产生。这也是一对多的关系，其中 Response 的参与是强制的。

6. **Response 与 Question_Answer的关系**：
   - 一个 Response 可以关联多个 Question_Answers（问题答案），而每个 Question_Answer  只能属于一个Response。这是一对多关系，Question_Answer 在此关系中强制参与。

7. **Question_Answer 与  Selected_Option 的关系**：
   - Question_Answer 可能与 Selected_Option（选择题答案）有关联，也可能没有（如在填空题中）。而每个 Selected_Option 必定与一个 Question_Answer 有关。这构成一对一的关系，其中Selected_Option 的参与是强制的，而 Question_Answer 是非强制参与。

8. **User 与 Image_Response的关系**：
   - 一个 User 可能上传多张图像，生成多个 Image_Response（图像响应），每个 Image_Response 必定与一个 User 关联。这是一对多的关系，其中 Image_Response 的参与是强制的。

### 逻辑设计

#### 表结构

按照理论课程上学习的构造方法，共建立 12 个表，其中下划线是主码，加粗是外码。

- surveys($\underline{survey\_id}$, title, description, date, first_question_id, last_question_id)
- question_type($\underline{question\_type\_id}$, name)
- questions($\underline{question\_id}$, question_text,  **question_type_id**, **survey\_id**)
- options($\underline{option\_id}$, option_text, **question_id**)
- question_logic($\underline{logic\_id}$, parent_question_id, **parent_option_id**, **child_question_id**)
- users($\underline{user\_id}$, name, sex, nation, ID_number, birthday, phone_number, family_member_phone_number, height, weight, homeplace, last_login_time)
- image_responses($\underline{image\_response\_id}$, time, input_image, predict_image, **user_id**)
- responses($\underline{response\_id}$, time, **user_id**, **survey_id**, current_question_id)
- question_answers($\underline{question\_answer\_id}$, answer, **response_id**, **question_id**)
- selected_option($\underline{selected\_option\_id}$,  **question_answer_id**, **option_id**)
- lists($\underline{list\_id}$, **parent_question_id**, **child_question_id**, **response_id**)

#### 完整性说明

1. **问卷（Surveys）**:
   - 系统为每个问卷分配唯一的 `survey_id` 作为主键。

2. **问题类型（Question_Type）**:
   - 系统为每种问题类型分配唯一的 `question_type_id` 作为主键。

3. **问题（Questions）**:
   - 系统为每个问题分配唯一的 `question_id` 作为主键。
   - `question_type_id` 和 `survey_id` 作为外键，分别引用 `Question_Type` 和 `Surveys` 表中的 `question_type_id` 和 `survey_id`。

4. **选项（Options）**:
   - 系统为每个选项分配唯一的 `option_id` 作为主键。
   - `question_id` 作为外键，引用 `Questions` 表中的 `question_id`。

5. **问题逻辑（Question_Logic）**:
   - 系统为每个问题逻辑分配唯一的 `logic_id` 作为主键。
   - `parent_question_id`、`child_question_id` 和 `parent_option_id` 作为外键，分别引用 `Questions` 表中的 `question_id` 和 `Options` 表中的 `option_id`。

6. **用户（Users）**:
   - 微信小程序为每个用户分配唯一的 `user_id` 作为主键。

7. **图像响应（Image_Responses）**:
   - 系统为每个图像响应分配唯一的 `image_response_id` 作为主键。
   - `user_id` 作为外键，引用 `Users` 表中的 `user_id`。

8. **问卷响应（Responses）**:
   - 系统为每个问卷响应分配唯一的 `response_id` 作为主键。
   - `user_id` 和 `survey_id` 作为外键，分别引用 `Users` 表和 `Surveys` 表中的 `user_id` 和 `survey_id`。

9. **问题答案（Question_Answers）**:
   - 系统为每个问题的答案分配唯一的 `question_answer_id` 作为主键。
   - `response_id` 和 `question_id` 作为外键，分别引用 `Responses` 表和 `Questions` 表中的 `response_id` 和 `question_id`。

10. **选择题选项答案（Selected_Option）**:
    - 系统为每个选择题的选项答案分配唯一的 `selected_option_id` 作为主键。
    - `question_answer_id` 和 `option_id` 作为外键，分别引用 `Question_Answers` 表和 `Options` 表中的 `question_answer_id` 和 `option_id`。

11. **答题记录链表（Lists）**:
    - 系统为每个答题记录分配唯一的 `lists_id` 作为主键。
    - `parent_question_id` 和 `child_question_id` 作为外键，引用 `Questions` 表中的 `question_id`。
    - `response_id` 也作为外键，引用 `Responses` 表中的 `response_id`。

## 功能实现与界面设计

### 基础信息

1. 获取用户基本信息：绑定首页个人基础信息按钮 。

   （1）功能实现：如果为第一次创建（即在数据库中没有找到该 `user_id`），在数据库中创建 `user_id` 并返回；否则调用数据库记录，返回曾经填写的个人信息。

   - api ：`POST base_url/api/get_basic_info`

   - 请求体参数：`user_id`

     ```JSON
     {
     	"user_id": "123456",
       	"jargon": "DeepLeiarning"
     }
     ```

   - 响应体参数：返回数据库中的曾经记录的个人信息。如果没有信息，返回错误。

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
     ```
     
     （2）界面设计：   
     
     ![image-20231203110927571](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031109604.png)

2. 更新/提交用户基本信息 - 绑定个人基础信息页面的**提交按钮**

   （1）功能实现：保证服务器端已经创建了 `user_id`，微信小程序向服务器发送该用户基础信息。

   - api ：`POST base_url/api/update_basic_info`

   - 请求体参数：

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

   - 响应体参数：

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
     
        （2）界面设计：![image-20231203111145631](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031111661.png)

### 问卷部分

#### 问卷管理系统

1. 获取用户id:绑定小程序启动。

   （1）功能实现：不在客户端直接使用 `openid`，而是用服务器生成的令牌`user_id`来识别用户。

   - api： `POST base_url/api/login`

   - 请求体参数：`res.code`

     ```json
     {
     	"code": "0c3NikGa1g2IyG0hK2Ga1zAfNS3NikGw"
     }
     ```

   - 响应体参数：返回`user_id`

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

2. 获取预测疾病问卷首页 - 绑定引导页上某个疾病问卷按钮

   （1）功能实现：数据库创建问卷响应实例，服务器端返回问卷响应 `response_id`，同时初始化当前问题 `current_question_id`。

   - api：`POST base_url/api/surveys/{survey_id}/new_survey_instance`

   - 请求体参数：`user_id, time`

     - `survey_id` 代表问卷类型，即一种问卷一个 `id`

     ```json
     {
         "jargon": "DeepLeiarning",
         "user_id": "123456",
         "time": "2023-11-14 19:59:00"
     }
     ```

   - 响应体参数：

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

   - 注意服务器端验证 `user_id` 的合法性

     1. 如果没有 `user_id`，跳转提交基础信息页面，返回 `error - type = NoUserInfo`

   - 同时在数据库端创建该 `response_id` 的状态 `list`

   - 断线重连：若用户未点击提交按钮退出了微信小程序，再次打开时不应该再次创建`response_id`，此时恢复断线时的`response_id`，得到断线时的`lists`、`current_question_id`

   （2）界面设计：

   ![image-20231203112232462](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031122489.png)

3. 提交单题答案 - 绑定上一题/下一题按钮，即每次换题需提交答案

   （1）功能实现：

   - api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/submit`

   - 请求参数：

   | 参数名           | 类型  | 描述                           |
   | ---------------- | ----- | ------------------------------ |
   | user_id          | Text  | 用户 id                        |
   | response_id      | Text  | 响应 id                        |
   | type_id          | int   | 题目类型 id                    |
   | text             | Text  | 把数字、日期统一为文本传给后端 |
   | selected_options | array | 选择选项数组                   |

   ```json
   // 第一题示例
   {
       "user_id": "123456",
       "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf",
       "type_id": 0,
       "text": "xxx",
       "selected_options": []
   }
   
   // 第二题示例
   {
       "user_id": "123456",
       "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf",
       "type_id": 1,
       "text": "Answer_in_Selected_Option",
       "selected_options": [1]
   }
   
   // 第三题示例
   {
       "user_id": "123456",
       "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf",
       "type_id": 0,
       "text": "xxx",
       "selected_options": []
   }
   ```

   - 响应参数：

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

4. 获取下一题序号、题目和选项 - 绑定：下一题按钮 & 问卷首页的问卷开始按钮。

   （1）功能实现：前端逻辑下一题时，先判断提交答案的 `message==success`，成立则返回下一题题目信息，否则提示先提交选择当前问题。

   - api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/next_question`

     1. 这里的 `question_id` 为当前问题 `id`，不是显示的 `id`

     2. 前端隐式记录 `question_id`，此处是为了验证

   - 请求参数：`user_id`, `response_id`

     1. 需要根据这两个 `id` 在数据库唯一查询下一题是什么

        ```json
        {
            "user_id": "123456",
            "response_id": "78683cd93019e18240413b5d3cf2b5500c80428bb9aff10f9c09f7b1beddb4cf"
        }
        ```

   - 响应参数：

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

   （2）界面设计：

   ![image-20231203113200503](https://cdn.jsdelivr.net/gh//LucasQAQ/PicGo@master/images/202312121040695.png)

5. 获取上一题序号、题目和选项 - 绑定：上一题按钮 & 问卷首页的问卷开始按钮。

   （1）功能实现：用户点击上一题时，前端**不用**判断提交答案的 `message==success`。前端存下`is_first_question`，如果为真，则不显示上一题按钮。

   - api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/previous_question`

     1. 这里的 `question_id` 为当前问题 `id`，不是显示的 `id`

     2. 前端隐式记录 `question_id`,此处是为了验证

   - 请求参数：`user_id`, `response_id`

     1. 需要根据这两个 `id` 在数据库唯一查询上一题是什么

        ```json
        {
            "user_id": "lucasqaq",
            "response_id": "b6c275cd5575de8514918de3ede7673ef696ed35aa201df80afd1931357333e1"
        }
        ```

   - 响应参数：

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

   （2）界面设计：

6. 结束本次问卷 - 绑定在结束问卷提交按钮上。

   （1）功能实现：回收`lists`数据库资源，结束本次问卷。

   - api：`POST base_url/api/surveys/{survey_id}/end_survey`

   - 请求参数：`user_id`, `response_id`

     ```json
     {
         "user_id": "afsd",
         "response_id": "1231sfas"
     }
     ```

   - 响应参数：

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

   （2）界面设计：

      ![image-20231203113755618](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031137648.png)

#### 问卷解析系统

后端实现了添加新问卷的半自动化系统。

1. 用户手动填写包含问卷各个问题题面和选项的 txt 文件，并用提示符 `+` 标记条件问题逻辑，提示符 `^*#` 等标记问题类型。

![](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031144908.png)

2. 使用 C++ 读取 txt 文件信息，通过多个堆栈获得条件问题逻辑，并生成数据库表 question_logic($\underline{logic\_id}$, parent_question_id, **parent_option_id**, **child_question_id**)，输出为 `json` 文件

3. 通过 Python 脚本，将 `json` 文件转换为需要的 `sql` 代码，并更新数据库

### 生图部分

「胃癌图像预测生成」是一款基于深度学习技术的医学辅助诊断工具。该系统能够让用户上传自己的胃镜图像，并迅速通过后端的深度学习模型进行分析处理，生成图像中可能患癌的区域预测。此功能的设计初衷是为了给予用户一个直观的警示，提醒他们关注胃部健康，并在必要时寻求专业医生的帮助。

#### 功能流程

1. **图像上传**：用户通过系统界面上传自己的胃镜图像。系统支持常见的图像格式，如 JPG、PNG 等。该图片可在华西医院的诊断报告中获得。

2. **预测处理**：上传的图像会被发送到服务器端，深度学习模型会对图像进行详尽的分析，识别出潜在的异常区域。

3. **结果展示**：处理完成后，系统会在界面上展示原始图像与预测图像。预测图像中可能的癌变区域将以高亮或标记的形式显示，便于用户识别和理解。

4. **警示作用**（主要）：通过对比原始图像和预测图像，用户能够直观地了解到潜在的风险区域。系统的这一功能，不仅能够提高用户对胃癌风险的认识，也鼓励他们进行进一步的医学检查。

#### 提醒声明

- 本系统生成的预测结果仅供参考，不能替代专业医生的诊断。
- 用户应保持定期的胃部健康检查，早发现、早治疗。

### 科普部分

我们的健康知识科普功能致力于为用户提供准确、实用的医疗健康信息。通过此功能，用户可以轻松获取到各种医学科普知识，内容涵盖疾病预防、身体健康、心理调适、生活方式调整等多个方面。用户仅需简单点击感兴趣的主题，即可阅读相关的科普文章，学习如何保持健康的生活习惯，以及如何识别和应对常见的健康问题。这一功能不仅能够增强用户的健康意识，还能帮助他们在必要时作出明智的健康决策。

## 系统性能优化

我们根据 EndoInsightDB 的应用场景，在数据库端进行了性能调优，期望在资源受限的情况下让数据库发挥出最大的性能。

我们发现，EndoInsightDB 的部署资源相当有限，其应用场景比较单一，涉及到的 SQL 查询也比较固定，查询比较简单。符合 OLTP 任务特征。

我们针对该任务设计了一个两阶段的调优流程。大体上讲，第一阶段是对整个  DBMS 软件进行系统层面的调优，粒度是整个 workload，这里我们直接使用 TPC-C 的 benchmark，以吞吐量作为优化目标。第二阶段是针对具体 query 进行调优,粒度是单条 SQL 语句。在我们的应用场景中，SQL 语句的模板是固定的，只有谓词会不断变化。我们针对单个 SQL 模板，探索最适合它的执行计划来优化其查询执行时间。

总的来说，我们的两阶段优化粒度是从粗到细，优化目标是从吞吐量到查询延迟，全部采用离线调优，之后再实际部署。值得注意的是，第一阶段给出的配置需要数据库系统重启才能生效，所以一旦实际部署，就不再轻易更改。第二阶段的配置可以针对单个 query 生效，在运行时随时改变。

### DBMS 系统参数调优（第一阶段）

本阶段对整个 DBMS 软件进行系统层面的调优。我们介绍了该领域目前的研究情况，和相关工作，选取 $5$ 种方法进行 $100$ 轮迭代实验，挑选搜索到的最优配置部署到 EndoInsightDB  。

#### DBMS 调优背景

数据库管理系统有很多配置参数，被叫做旋钮。配置旋钮（knobs）控制着数据库系统的许多方面（如查询优化器、内存管理、日志和缓存设置等），旋钮值的不同组合会显著影响系统的健壮性、性能和资源使用。

从广义上讲，“配置旋钮（configuration knobs）”表示数据库中值可以调整并可能对数据库性能产生影响的的旋钮，具体可以分为 $7$ 类：Access Control、Query Optimizer、Query Executor、Background Processes、Resource (CPU)、Resource (Memory)以及Resource (Disk)

一般来说，旋钮调优的目的是通过有效地调整旋钮的值，以满足某些调优目标。调优的目标有两个方面，一方面用户需要配置数据库以获得高性能（如吞吐量、延迟）；另一方面数据库供应商要求在不牺牲性能的前提下，提高资源利用率（如I/O和内存使用）或降低维护成本。

我们根据时间整理了这个领域的代表性工作，如图所示，主要有三类。最开始是人类专家手动调优。之后逐渐总结出一些规则经验，结合领域知识，发明了基于规则的调优方法。而近几年出现的最强的调优系统大多是基于机器学习的方法，主要是贝叶斯优化和强化学习。  

![avatar](/Users/darkmoonbook/Downloads/works.png)

我们从中选取最近的五个有代表性的基于机器学习的方法进行自动调优。

#### 实验

我们使用 [SMAC](https://github.com/automl/SMAC3) 实现了基于随机森林和高斯过程的贝叶斯优化，DDPG和DB-BERT的代码来自[itrummer](https://github.com/itrummer/dbbert)， GPTuner也使用 [开源代码](https://github.com/SolidLao/GPTuner)。TPCC使用 [benchbase](****)版本。我们将 TPCC 的 `scale factor` 设为 $200$，将 `arrival rate` 设为 `unlimited` 以便于充分测试吞吐量。调优参数的选择来自 `GPTuner`，由 `GPT` 进行选取。我们对每一种方法都进行了 $100$ 轮迭代，发现找到的最好的配置能将吞吐量提升约 $14\%$。我们给出对应的配置:

```json
{
​     "archive_mode": "always",

​      "autovacuum_analyze_scale_factor": 0.1,

​      "autovacuum_freeze_max_age": 200000000,

​      "autovacuum_max_workers": 18,

​      "autovacuum_vacuum_scale_factor": 25.15,

​      "bgwriter_delay": 2507,

​      "bgwriter_lru_multiplier": 2.0,

​      "checkpoint_completion_target": 0.9,

​      "checkpoint_timeout": 465,

​      "commit_delay": 0,

​      "commit_siblings": 5,

​      "deadlock_timeout": 1000,

​      "default_statistics_target": 100,

​      "max_parallel_workers": 8,

​      "max_replication_slots": 10,

​      "max_wal_size": 12250,

​      "max_worker_processes": 14,

​      "min_wal_size": 80,

​      "random_page_cost": 4.0,

​      "seq_page_cost": 1.0,

​      "shared_buffers": 2578129,

​      "track_activity_query_size": 1024,

​      "vacuum_cost_limit": 200,

​      "wal_sync_method": "open_datasync",

​      "wal_writer_delay": 5100,

​      "work_mem": 4096,

​      "effective_io_concurrency": 1,

​      "join_collapse_limit": 8,

​      "log_rotation_size": 10240,

​      "max_standby_streaming_delay": 30000,

​      "max_wal_senders": 10
}
```

### Query plan 优化（第二阶段）

目前很多 DBSM 支持为每条 SQL 都提供「hint」，如 SQL Server。不同的 hint 会导致执行优化器对同一个 query 产生不同的执行计划，从而导致 query 不同的执行效率。基于这个观察，我们希望为每个具体的 query 都能找到好的 hint 来修改其执行计划，进而缩短其查询时间。

在这里我们将 hint 定义为是否启用某个算子。我们将问题建模为多臂老虎机问题，我们针对是否禁用 $6$ 个算子进行组合（有 $2^6$ 种组合方式）以此定义了搜索空间。我们假设查询的模板一定的情况下，谓词的改变不会显著影响查询时间，我们希望对于每个查询模板找到最好的那个 hint 组合。 我们选取的六个算子对应的hint分别是：

```python
["enable_nestloop", "enable_hashjoin", "enable_mergejoin", "enable_seqscan", "enable_indexscan", "enable_indexonlyscan"]
```

它们均为布尔类型的参数，将它们设为"on"和"off"来分别启用和禁用对应的算子。

我们用贝叶斯优化来对每个 query 模板进行 $16$ 轮探索，选取其中最优的 hint 组合存储下来。EndoInsightDB 将利用 query 模板和 hint 的对应信息，在实际部署时，根据 query 匹配模板，进而改变默认的执行计划来提升查询性能。

代码提供在``./HintTuner``目录下，修改``./configs/postgres.ini``来连接到你的数据库实例。要优化的query请放到``./sql``目录下。优化过程会保存在``./BO_test``目录下。可使用该指令运行：`PYTHONPATH=src python3 src/run.py -seed=1` 。
