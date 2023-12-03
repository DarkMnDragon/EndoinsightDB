## 项目总体说明

### 项目开发动机

#### 医学背景

消化道疾病包括了一系列疾病，如胃炎、胃溃疡、肠炎、肝病、胰腺炎等。这些疾病在全球范围内普遍存在，影响着亿万人的健康。某些消化道疾病可能会发展为严重的健康问题，如胃癌、肝硬化、胰腺癌等，它们对患者的生命构成了重大威胁。适时的预防和治疗对于控制和治愈消化道疾病至关重要，可以减少疾病带来的并发症和死亡率。

消化内镜是一种重要的诊断工具，可以直观地查看消化道内部，发现炎症、溃疡、肿瘤等病变。通过内镜检查，医生能够在早期发现潜在的严重疾病，如早期胃癌或结肠癌，从而及时进行治疗，提高治愈率。

消化道疾病问卷在医学和研究领域具有重要意义。问卷是收集大量患者数据的有效手段，对于临床研究和流行病学研究非常重要。通过分析这些数据，研究人员可以更好地理解消化道疾病的流行趋势、病因和治疗效果。

#### 项目前身

我们根据华西医院提供的患病和健康数据，训练了一个生成对抗模型进行消化道内镜图像的风格迁移，将一张健康的内镜图像转化为患病图像，可以供医生学习或对患者进行警示。扩散模型是一种深度学习技术，通常用于图像生成和风格迁移。在这种应用场景中，该模型可以接收健康的消化道内镜图像，并将其转换为展示特定病变（如炎症、溃疡或肿瘤）的图像。这种转换的目的是向患者展示疾病的严重性，增加他们对健康状况的认识和警觉性。

本项目会将图像处理板块也融合进来，使用数据库进行存储。

### 技术架构

本项目源于华西医院消化内科的实际需求，立足于华西医院实际应用场景，针对消化道疾病开发了疾病预警和诊断的智慧数据库：EndoInsightDB。

本项目使用微信小程序作为前端和用户交互，使用微信小程序提供的用户唯一的UserID在EndoInsightDB中识别用户。用户可以通过微信小程序填写问卷、上传消化道内镜图片、查看健康科普。微信小程序与我们的Flask后端进行交互，Flask后端直接与数据库连接。对于小程序端的请求，Flask后端在完成安全验证和对请求进行解析后再与数据库进行交互，完成问卷信息和图像在数据库的增删查改。此外我们的项目支持疾病风险评估和疾病图像预测。我们从数据库中提取某一用户的问卷填写信息，使用一个机器学习模型，根据用户填写的答案给出疾病风险评估分数。我们的数据库还可以和一个生成扩散模型进行交互，提供患者的胃镜图像并保存预测后的图像。

在本项目的医疗应用场景中，我们需要收集、存储和利用大量多源异构的患者信息。例如疾病问卷题型多样，包含单选、多选、填空等，由此导致数据库需要存储的答案也是多样的。我们还需要在数据库内保存相应用户的胃镜图像及对应转换后的图像。由于该项目的应用场景特殊，我们对数据库内信息的处理需要保证高效、稳定、安全和保密。

## 数据库设计

### 概念设计

我们采用了基于 E-R 模型的数据库设计方法。为EndoInsightDB设计的ER图如下：

![ER](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031150789.jpg)

我们对每一实体逐一进行解释：

- surveys是问卷实体型，它的属性包含问卷的题目、描述、创建日期以及第一个和最后一个问题的id以判定问卷是否开始和结束。
- question_type是问题类型和其类型id的映射实体型。例如：type_id为0、1、2分别代表问题类型为填空、单选、多选。question_type实体方便了对问题的类型这个属性的管理，方便用户更清晰明了地获取题目的所有类型和type_id的对应关系并且便于不断拓展问题类型。
- questions是问卷里每个问题的实体型，它的属性指明了问题的文本、问题的类型和问题所归属的问卷。
- options是选项实体型，它存储该属性的内容以及该选项所归属的问题。目前的版本中，每个选项所归属的问题都必定为单选或多选。
- question_logic为跳转逻辑实体型。提供了问卷中问题的跳转逻辑。根据本题的编号和用户选择的答案，给出下一个问题的编号应当是什么。
-  users为用户实体型，它储存了用户的基本信息，如姓名、性别、体重等。user_id使用微信所提供的用户id，可以可以唯一地识别用户。
-  image_responses为消化道图像响应实体型。用户上传一张消化道图像，我们会调用提前训练好的生成对抗网络来生成一张对应的病变图像以警示患者。每一个响应都会存储一对对应的图像，并且记录图片上传时间和所属用户。
- responses为问卷响应实体型。当一个用户开始回答一个新问卷的时候，就会创建一个新的实体。该实体除了记录了用户、问卷、响应时间以外还记录了用户当前正处于哪个题目。也就是说一个responses实体记录了一个用户对一个问卷的答题状态。通过与对应问卷实体的属性做对比来判定是否允许用户提交问卷和继续跳转上一题。此外一个responses实体可能和多个question_responses实体对应，表示用户对该问卷已回答问题的答案。
- question_answers是答案表实体型，记录了用户对每个问题提交的答案。其中若题目类型为填空，则answer属性为用户所填写答案。若为单选或多选，则用户的选择保存在selected_option里，answer里不存答案。
- selected_option为选择题答案实体型，存放单条选择题答案，粒度为单个题目。
- lists为答题链表实体型。记录了每个response的实际答题顺序，便于用户回退到上一题。动态更新，用户答完问卷后即可情况对应response_id的记录。



结合ER图，对实体型之间的联系进行解释：

- 一个survey可以有多个question，但一个question只能归属于一个survey。是一对多联系。
- 一个question只能是一种question_type（填空、单选、多选），但可能多种问题都可能属于一个question_type。是一对多联系。
- 一个question可能有多个option（选择题），也可以一个option也没有（填空题）。所以是非强制参与联系。但每个option都一定属于某个问题，是强制参与联系。question和option构成一对多联系。
- 一个survey可能有来自多个用户或者一个用户的response或者没有response。一个response只能是对一个问卷的响应并且必须和一个问卷对应，是强制参与联系。survey和response构成一对多联系。 
- 一个user可能产生多个response，一个response必须也只能由一个user产生。是一对多联系，且response强制参与。
- 一个response可能有多个question_answers及多个问题答案对。一个question_answer一定且只属于一个response。是一对多联系，question_answer强制参与。
- 一个question_answer不一定和某个selected_option有联系（填空题不会存选项答案），但一个selected_option必然和一个question_answer建立联系。是一对一联系，selected_option强制参与，question_answer非强制参与。
- 一个user可以上传多张图像从而生成多个image_response，一个image_response必定属于某个user。是一对多联系且image_responses强制参与。

### 逻辑设计

#### 表结构

按照理论课程上学习的构造方法，共建立 12 个表，其中下划线是主码，加粗是外码。

surveys($\underline{survey\_id}$, title, description, date, first_question_id, last_question_id)

question_type($\underline{question\_type\_id}$, name)

questions($\underline{question\_id}$, question_text,  **question_type_id**, **survey\_id**)

options($\underline{option\_id}$, option_text, **question_id**)

question_logic($\underline{logic\_id}$, parent_question_id, **parent_option_id**, **child_question_id**)

users($\underline{user\_id}$, name, sex, nation, ID_number, birthday, phone_number, family_member_phone_number, height, weight, homeplace, last_login_time)

image_responses($\underline{image\_response\_id}$, time, input_image, predict_image, **user_id**)

responses($\underline{response\_id}$, time, **user_id**, **survey_id**, current_question_id)

question_answers($\underline{question\_answer\_id}$, answer, **response_id**, **question_id**)

selected_option($\underline{selected\_option\_id}$,  **question_answer_id**, **option_id**)

lists($\underline{list\_id}$, **parent_question_id**, **child_question_id**, **response_id**)



#### 完整性说明

1. 问卷（surveys）

系统为每一问卷分配独一无二的survey_id作为主码。

2. 问题类型（question_type)

系统为每一类型问题分配独一无二的question_type_id作为主码。

3. 问题（questions）

系统为每一问题分配独一无二的question_id作为主码。

question_type_id和survey_id均为外码，分别参照question_type和surveys表中的question_type_id和survey_id。

4. 选项（options）

系统为每一选项分配独一无二的option_id作为主码。

question_id作为外码，参照questions表中的question_id。

5. 问题逻辑（question_logic)

系统为每一问题逻辑分配独一无二的logic_id作为主码。

parent_question_id和child_question_id均为外码，参照questions表中的question_id。parent_option_id也做外码，参照options表中的option_id。

6. 用户（users）

微信小程序为每个用户分配独一无二的user_id作为主码。

7. 图像响应（image_responses)

系统为每一图像响应分配独一无二的image_response_id作为主码。

User_id作为外码，参照users表中的user_id。

8. 问卷响应（responses）

系统为每一问卷响应分配独一无二的response_id作为主码。

user_id 和 survey_id均为外码，分别参照user表和surveys表中的user_id和survey_id。

9. 问题答案（question_answers）

系统为每一问题的答案分配独一无二的question_answer_id作为主码。

response_id 和 question_id 均作为外码分别参照responses表和questions表中的response_id 和 question_id。

10. 选择题选项答案（selected_option）

系统为每一选择题的选项答案分配独一无二的selected_option_id作为主码。

question_answer_id 和 option_id 均作为外码分别参照question_answers表和options表中的question_answer_id 和 option_id。

11. 答题记录链表（lists）

系统为每一答题记录分配独一无二的lists_id作为主码。Parent_question_id和child_question_id都作为外码参照questions表中的question_id。

response_id也作为外码参照responses表中的response_id。

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
     }
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


   （2）界面设计：

   ![image-20231203111145631](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031111661.png)

### 问卷部分

#### 问卷管理系统

1. 获取预测疾病问卷首页 - 绑定引导页上某个疾病问卷按钮

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

2. 提交单题答案 - 绑定上一题/下一题按钮，即每次换题需提交答案

   （1）功能实现：

   - api：`POST base_url/api/surveys/{survey_id}/questions/{question_id}/submit`

   - 请求参数：

   | 参数名           | 类型  | 描述                           |
   | ---------------- | ----- | ------------------------------ |
   | user_id          | Text  | 用户id                         |
   | response_id      | Text  | 响应id                         |
   | type_id          | int   | 题目类型id                     |
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

3. 获取下一题序号、题目和选项 - 绑定：下一题按钮 & 问卷首页的问卷开始按钮。

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

   ![image-20231203113200503](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031132531.png)

4. 获取上一题序号、题目和选项 - 绑定：上一题按钮 & 问卷首页的问卷开始按钮。

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

5. 结束本次问卷 - 绑定在结束问卷提交按钮上。

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

1. 用户手动填写包含问卷各个问题题面和选项的txt文件，并用提示符`+`标记条件问题逻辑，提示符`^*#`等标记问题类型。

![](https://cdn.jsdelivr.net/gh/LucasQAQ/PicGo@master/images/202312031144908.png)

2. 使用C++读取txt文件信息，通过多个堆栈获得条件问题逻辑，并生成数据库表question_logic($\underline{logic\_id}$, parent_question_id, **parent_option_id**, **child_question_id**)，输出为json文件。

3. 通过python脚本，将json文件转换为需要的sql代码，并更新数据库。

### 生图部分

### 科普部分

## 系统性能优化

