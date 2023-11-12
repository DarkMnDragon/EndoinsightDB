-- Creating tables
CREATE TABLE Surveys (
  Survey_id INT PRIMARY KEY,
  Title VARCHAR(255),
  Description TEXT,
  Date DATE
);

CREATE TABLE Input_type (
  Input_type_id INT PRIMARY KEY,
  Name VARCHAR(50)
);

CREATE TABLE Questions (
  Question_id INT PRIMARY KEY,
  Text VARCHAR(255),
  Input_type_id INT,
  Survey_id INT,
  FOREIGN KEY (Input_type_id) REFERENCES Input_type(Input_type_id),
  FOREIGN KEY (Survey_id) REFERENCES Surveys(Survey_id)
);

CREATE TABLE Options (
  Option_id INT PRIMARY KEY,
  option_text VARCHAR(255),
  Question_id INT,
  FOREIGN KEY (Question_id) REFERENCES Questions(Question_id)
);

CREATE TABLE Question_logic (
  Logic_id INT PRIMARY KEY,
  Parent_question_id INT,
  Parent_option_id INT,
  Child_question_id INT,
  FOREIGN KEY (Parent_question_id) REFERENCES Questions(Question_id),
  FOREIGN KEY (Child_question_id) REFERENCES Questions(Question_id)
);

-- Inserting data
INSERT INTO Surveys (Survey_id, Title, Description, Date) VALUES (1, '问卷调查', '', '2023-11-03');

INSERT INTO Input_type (Input_type_id, Name) VALUES (0, '填空'),
(1, '单选'),
(2, '多选');


INSERT INTO Questions (Question_id, Text, Input_type_id, Survey_id) VALUES (1, '您的姓名是?', 0, 1),
(2, '您的性别是?', 1, 1),
(3, '您的民族是?', 1, 1),
(4, '您的身份证号是?', 0, 1),
(5, '您的出生年是?', 0, 1),
(6, '您的出生月是?', 0, 1),
(7, '您的出生日是?', 0, 1),
(8, '患者本人电话号码?', 0, 1),
(9, '家属称呼?', 0, 1),
(10, '家属电话号码?', 0, 1),
(11, '您的身高是?', 0, 1),
(12, '您的体重是?', 0, 1),
(13, '您是否长期居住于出生地?', 1, 1),
(14, '家庭住址（省市县街道小区）?', 0, 1),
(15, '长期居住地地区名称（省市县街道小区）?', 0, 1),
(16, '居住时长?', 1, 1),
(17, '出生地地区名称（省市县）?', 0, 1),
(18, '居住时长?', 1, 1),
(19, '您是否有过幽门螺旋杆菌（Hp）感染?', 1, 1),
(20, '确诊时间年?', 0, 1),
(21, '确诊时间月?', 0, 1),
(22, '是否根除?', 1, 1),
(23, '根除完成时间年?', 0, 1),
(24, '根除完成时间月?', 0, 1),
(25, '您是否有龋齿（虫牙）、缺齿、口臭?', 1, 1),
(26, '您的饮食口味偏好是?', 2, 1),
(27, '您是否存在以下饮食习惯?', 2, 1),
(28, '您吸烟吗?', 1, 1),
(29, '吸烟几年?', 0, 1),
(30, '平均每天几支?', 0, 1),
(31, '吸烟几年?', 0, 1),
(32, '平均每天几支?', 0, 1),
(33, '戒烟几年?', 0, 1),
(34, '您饮酒吗?', 1, 1),
(35, '饮酒几年?', 0, 1),
(36, '饮酒频率?', 1, 1),
(37, '平均每天多少ml?', 0, 1),
(38, '饮什么酒?', 0, 1),
(39, '饮酒几年?', 0, 1),
(40, '饮酒频率?', 1, 1),
(41, '平均每天多少ml?', 0, 1),
(42, '饮什么酒?', 0, 1),
(43, '戒酒几年?', 0, 1),
(44, '您是否有长期在吃的药物?', 1, 1),
(45, '药物具体名称?', 0, 1),
(46, '剂量?', 0, 1),
(47, '服用时间?', 0, 1),
(48, '服用原因?', 0, 1),
(49, '您现在是否患有以下某种疾病?', 2, 1),
(50, '您现在是否患有以下某种疾病?', 2, 1),
(51, '您过去是否患有以下某种疾病?', 2, 1),
(52, '您是否做过手术?', 1, 1),
(53, '疾病名称?', 0, 1),
(54, '手术时间（年）?', 0, 1),
(55, '手术时间（月）?', 0, 1),
(56, '手术方式?', 0, 1),
(57, '您的一级亲属中是否有人患过肿瘤?', 1, 1),
(58, '称谓（与本人关系）?', 0, 1),
(59, '肿瘤详细名称（仅*填写一级亲属）?', 0, 1),
(60, '您是否有确诊的精神疾病（如焦虑、抑郁等）?', 1, 1),
(61, '疾病具体名称?', 0, 1),
(62, '疾病严重程度?', 0, 1),
(63, '病程时间?', 0, 1),
(64, '治疗措施?', 0, 1),
(65, '目前状况?', 0, 1),
(66, '您自我评价精神压力情况是?', 1, 1);


INSERT INTO Options (Option_id, option_text, Question_id) VALUES (1, '男', 2),
(2, '女', 2),
(3, '汉族', 3),
(4, '其他', 3),
(5, '是', 13),
(6, '否', 13),
(7, '小于一个月', 16),
(8, '一个月到半年', 16),
(9, '半年到三年', 16),
(10, '三年以上', 16),
(11, '小于一个月', 18),
(12, '一个月到半年', 18),
(13, '半年到三年', 18),
(14, '三年以上', 18),
(15, '是', 19),
(16, '已根除', 22),
(17, '根除失败', 22),
(18, '未根除', 22),
(19, '否', 19),
(20, '不详', 19),
(21, '是', 25),
(22, '否', 25),
(23, '不详', 25),
(24, '高盐', 26),
(25, '高糖', 26),
(26, '高油', 26),
(27, '喜烫食', 26),
(28, '喜烟熏食物', 26),
(29, '喜油炸食物', 26),
(30, '喜腌菜', 26),
(31, '喜红肉或加工肉类', 26),
(32, '以上均无', 26),
(33, '长期不吃早餐', 27),
(34, '少食蔬果', 27),
(35, '饮食不规律', 27),
(36, '暴饮暴食', 27),
(37, '吃饭速度快', 27),
(38, '吃剩饭菜', 27),
(39, '以上均无', 27),
(40, '吸烟，未戒', 28),
(41, '吸过烟，已戒', 28),
(42, '从不吸烟', 28),
(43, '喝酒，未戒', 34),
(44, '经常', 36),
(45, '偶尔', 36),
(46, '以前喝，已戒', 34),
(47, '经常', 40),
(48, '偶尔', 40),
(49, '从不喝酒', 34),
(50, '不详', 34),
(51, '有', 44),
(52, '无', 44),
(53, '不详', 44),
(54, '高血压', 49),
(55, '冠心病', 49),
(56, '糖尿病', 49),
(57, '慢性阻塞性肺部疾病', 49),
(58, '慢性心力衰竭', 49),
(59, '慢性肾衰', 49),
(60, '甲亢', 49),
(61, '甲减', 49),
(62, '胃炎', 50),
(63, '消化性溃疡', 50),
(64, '胃食管反流病', 50),
(65, '胃癌', 50),
(66, '食管癌', 50),
(67, '炎症性肠病', 50),
(68, '结直肠癌', 50),
(69, '胰腺癌', 50),
(70, '肝炎', 50),
(71, '肝硬化', 50),
(72, '胃炎', 51),
(73, '消化性溃疡', 51),
(74, '胃食管反流病', 51),
(75, '胃癌', 51),
(76, '食管癌', 51),
(77, '炎症性肠病', 51),
(78, '结直肠癌', 51),
(79, '胰腺癌', 51),
(80, '有', 52),
(81, '无', 52),
(82, '不详', 52),
(83, '有', 57),
(84, '无', 57),
(85, '不详', 57),
(86, '是', 60),
(87, '否', 60),
(88, '非常大', 66),
(89, '有点大', 66),
(90, '一般', 66),
(91, '没有', 66),
(92, '不详', 66);

INSERT INTO Question_logic (Logic_id, Parent_question_id, Parent_option_id, Child_question_id) VALUES (1, 1, 0, 2),
(2, 2, 0, 3),
(3, 3, 0, 4),
(4, 4, 0, 5),
(5, 5, 0, 6),
(6, 6, 0, 7),
(7, 7, 0, 8),
(8, 8, 0, 9),
(9, 9, 0, 10),
(10, 10, 0, 11),
(11, 11, 0, 12),
(12, 12, 0, 13),
(13, 13, 5, 14),
(14, 13, 6, 15),
(15, 13, 6, 16),
(16, 16, 0, 17),
(17, 17, 0, 18),
(18, 18, 0, 19),
(19, 19, 15, 20),
(20, 19, 15, 21),
(21, 19, 15, 22),
(22, 22, 0, 23),
(23, 23, 0, 24),
(24, 24, 0, 25),
(25, 25, 0, 26),
(26, 26, 0, 27),
(27, 27, 0, 28),
(28, 28, 40, 29),
(29, 28, 40, 30),
(30, 28, 41, 31),
(31, 28, 41, 32),
(32, 28, 41, 33),
(33, 33, 0, 34),
(34, 34, 43, 35),
(35, 34, 43, 36),
(36, 36, 44, 37),
(37, 37, 0, 38),
(38, 34, 46, 39),
(39, 34, 46, 40),
(40, 40, 47, 41),
(41, 41, 0, 42),
(42, 42, 0, 43),
(43, 43, 0, 44),
(44, 44, 51, 45),
(45, 44, 51, 46),
(46, 44, 51, 47),
(47, 44, 51, 48),
(48, 48, 0, 49),
(49, 49, 0, 50),
(50, 50, 0, 51),
(51, 51, 0, 52),
(52, 52, 80, 53),
(53, 52, 80, 54),
(54, 52, 80, 55),
(55, 52, 80, 56),
(56, 56, 0, 57),
(57, 57, 83, 58),
(58, 57, 83, 59),
(59, 59, 0, 60),
(60, 60, 86, 61),
(61, 60, 86, 62),
(62, 60, 86, 63),
(63, 60, 86, 64),
(64, 60, 86, 65),
(65, 65, 0, 66);