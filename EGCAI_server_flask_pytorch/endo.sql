--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: image_responses; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.image_responses (
    image_responses_id integer NOT NULL,
    "time" timestamp without time zone,
    input_image bytea,
    predict_image bytea,
    user_id integer
);


ALTER TABLE public.image_responses OWNER TO endo;

--
-- Name: input_type; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.input_type (
    input_type_id integer NOT NULL,
    name character varying(50)
);


ALTER TABLE public.input_type OWNER TO endo;

--
-- Name: options; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.options (
    option_id integer NOT NULL,
    option_text character varying(255),
    question_id integer
);


ALTER TABLE public.options OWNER TO endo;

--
-- Name: question_logic; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.question_logic (
    logic_id integer NOT NULL,
    parent_question_id integer,
    parent_option_id integer,
    child_question_id integer
);


ALTER TABLE public.question_logic OWNER TO endo;

--
-- Name: question_responses; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.question_responses (
    question_response_id integer NOT NULL,
    answer text,
    response_id integer,
    question_id integer
);


ALTER TABLE public.question_responses OWNER TO endo;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.questions (
    question_id integer NOT NULL,
    text character varying(255),
    input_type_id integer,
    survey_id integer
);


ALTER TABLE public.questions OWNER TO endo;

--
-- Name: responses; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.responses (
    response_id integer NOT NULL,
    "time" timestamp without time zone,
    score integer,
    user_id integer,
    survey_id integer
);


ALTER TABLE public.responses OWNER TO endo;

--
-- Name: selected_option; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.selected_option (
    selected_option_id integer NOT NULL,
    question_response_id integer,
    option_id integer
);


ALTER TABLE public.selected_option OWNER TO endo;

--
-- Name: surveys; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.surveys (
    survey_id integer NOT NULL,
    title character varying(255),
    description text,
    date date
);


ALTER TABLE public.surveys OWNER TO endo;

--
-- Name: users; Type: TABLE; Schema: public; Owner: endo
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    usename character varying(255),
    password_hashed character varying(255),
    last_login_time timestamp without time zone
);


ALTER TABLE public.users OWNER TO endo;

--
-- Data for Name: image_responses; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.image_responses (image_responses_id, "time", input_image, predict_image, user_id) FROM stdin;
\.


--
-- Data for Name: input_type; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.input_type (input_type_id, name) FROM stdin;
0	填空
1	单选
2	多选
\.


--
-- Data for Name: options; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.options (option_id, option_text, question_id) FROM stdin;
1	男	2
2	女	2
3	汉族	3
4	其他	3
5	是	13
6	否	13
7	小于一个月	16
8	一个月到半年	16
9	半年到三年	16
10	三年以上	16
11	小于一个月	18
12	一个月到半年	18
13	半年到三年	18
14	三年以上	18
15	是	19
16	已根除	22
17	根除失败	22
18	未根除	22
19	否	19
20	不详	19
21	是	25
22	否	25
23	不详	25
24	高盐	26
25	高糖	26
26	高油	26
27	喜烫食	26
28	喜烟熏食物	26
29	喜油炸食物	26
30	喜腌菜	26
31	喜红肉或加工肉类	26
32	以上均无	26
33	长期不吃早餐	27
34	少食蔬果	27
35	饮食不规律	27
36	暴饮暴食	27
37	吃饭速度快	27
38	吃剩饭菜	27
39	以上均无	27
40	吸烟，未戒	28
41	吸过烟，已戒	28
42	从不吸烟	28
43	喝酒，未戒	34
44	经常	36
45	偶尔	36
46	以前喝，已戒	34
47	经常	40
48	偶尔	40
49	从不喝酒	34
50	不详	34
51	有	44
52	无	44
53	不详	44
54	高血压	49
55	冠心病	49
56	糖尿病	49
57	慢性阻塞性肺部疾病	49
58	慢性心力衰竭	49
59	慢性肾衰	49
60	甲亢	49
61	甲减	49
62	胃炎	50
63	消化性溃疡	50
64	胃食管反流病	50
65	胃癌	50
66	食管癌	50
67	炎症性肠病	50
68	结直肠癌	50
69	胰腺癌	50
70	肝炎	50
71	肝硬化	50
72	胃炎	51
73	消化性溃疡	51
74	胃食管反流病	51
75	胃癌	51
76	食管癌	51
77	炎症性肠病	51
78	结直肠癌	51
79	胰腺癌	51
80	有	52
81	无	52
82	不详	52
83	有	57
84	无	57
85	不详	57
86	是	60
87	否	60
88	非常大	66
89	有点大	66
90	一般	66
91	没有	66
92	不详	66
\.


--
-- Data for Name: question_logic; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.question_logic (logic_id, parent_question_id, parent_option_id, child_question_id) FROM stdin;
1	1	0	2
2	2	0	3
3	3	0	4
4	4	0	5
5	5	0	6
6	6	0	7
7	7	0	8
8	8	0	9
9	9	0	10
10	10	0	11
11	11	0	12
12	12	0	13
13	13	5	14
14	13	6	15
15	13	6	16
16	16	0	17
17	17	0	18
18	18	0	19
19	19	15	20
20	19	15	21
21	19	15	22
22	22	0	23
23	23	0	24
24	24	0	25
25	25	0	26
26	26	0	27
27	27	0	28
28	28	40	29
29	28	40	30
30	28	41	31
31	28	41	32
32	28	41	33
33	33	0	34
34	34	43	35
35	34	43	36
36	36	44	37
37	37	0	38
38	34	46	39
39	34	46	40
40	40	47	41
41	41	0	42
42	42	0	43
43	43	0	44
44	44	51	45
45	44	51	46
46	44	51	47
47	44	51	48
48	48	0	49
49	49	0	50
50	50	0	51
51	51	0	52
52	52	80	53
53	52	80	54
54	52	80	55
55	52	80	56
56	56	0	57
57	57	83	58
58	57	83	59
59	59	0	60
60	60	86	61
61	60	86	62
62	60	86	63
63	60	86	64
64	60	86	65
65	65	0	66
\.


--
-- Data for Name: question_responses; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.question_responses (question_response_id, answer, response_id, question_id) FROM stdin;
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.questions (question_id, text, input_type_id, survey_id) FROM stdin;
1	您的姓名是?	0	1
2	您的性别是?	1	1
3	您的民族是?	1	1
4	您的身份证号是?	0	1
5	您的出生年是?	0	1
6	您的出生月是?	0	1
7	您的出生日是?	0	1
8	患者本人电话号码?	0	1
9	家属称呼?	0	1
10	家属电话号码?	0	1
11	您的身高是?	0	1
12	您的体重是?	0	1
13	您是否长期居住于出生地?	1	1
14	家庭住址（省市县街道小区）?	0	1
15	长期居住地地区名称（省市县街道小区）?	0	1
16	居住时长?	1	1
17	出生地地区名称（省市县）?	0	1
18	居住时长?	1	1
19	您是否有过幽门螺旋杆菌（Hp）感染?	1	1
20	确诊时间年?	0	1
21	确诊时间月?	0	1
22	是否根除?	1	1
23	根除完成时间年?	0	1
24	根除完成时间月?	0	1
25	您是否有龋齿（虫牙）、缺齿、口臭?	1	1
26	您的饮食口味偏好是?	2	1
27	您是否存在以下饮食习惯?	2	1
28	您吸烟吗?	1	1
29	吸烟几年?	0	1
30	平均每天几支?	0	1
31	吸烟几年?	0	1
32	平均每天几支?	0	1
33	戒烟几年?	0	1
34	您饮酒吗?	1	1
35	饮酒几年?	0	1
36	饮酒频率?	1	1
37	平均每天多少ml?	0	1
38	饮什么酒?	0	1
39	饮酒几年?	0	1
40	饮酒频率?	1	1
41	平均每天多少ml?	0	1
42	饮什么酒?	0	1
43	戒酒几年?	0	1
44	您是否有长期在吃的药物?	1	1
45	药物具体名称?	0	1
46	剂量?	0	1
47	服用时间?	0	1
48	服用原因?	0	1
49	您现在是否患有以下某种疾病?	2	1
50	您现在是否患有以下某种疾病?	2	1
51	您过去是否患有以下某种疾病?	2	1
52	您是否做过手术?	1	1
53	疾病名称?	0	1
54	手术时间（年）?	0	1
55	手术时间（月）?	0	1
56	手术方式?	0	1
57	您的一级亲属中是否有人患过肿瘤?	1	1
58	称谓（与本人关系）?	0	1
59	肿瘤详细名称（仅*填写一级亲属）?	0	1
60	您是否有确诊的精神疾病（如焦虑、抑郁等）?	1	1
61	疾病具体名称?	0	1
62	疾病严重程度?	0	1
63	病程时间?	0	1
64	治疗措施?	0	1
65	目前状况?	0	1
66	您自我评价精神压力情况是?	1	1
\.


--
-- Data for Name: responses; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.responses (response_id, "time", score, user_id, survey_id) FROM stdin;
\.


--
-- Data for Name: selected_option; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.selected_option (selected_option_id, question_response_id, option_id) FROM stdin;
\.


--
-- Data for Name: surveys; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.surveys (survey_id, title, description, date) FROM stdin;
1	问卷调查		2023-11-03
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: endo
--

COPY public.users (user_id, usename, password_hashed, last_login_time) FROM stdin;
\.


--
-- Name: image_responses image_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.image_responses
    ADD CONSTRAINT image_responses_pkey PRIMARY KEY (image_responses_id);


--
-- Name: input_type input_type_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.input_type
    ADD CONSTRAINT input_type_pkey PRIMARY KEY (input_type_id);


--
-- Name: options options_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (option_id);


--
-- Name: question_logic question_logic_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.question_logic
    ADD CONSTRAINT question_logic_pkey PRIMARY KEY (logic_id);


--
-- Name: question_responses question_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.question_responses
    ADD CONSTRAINT question_responses_pkey PRIMARY KEY (question_response_id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (question_id);


--
-- Name: responses responses_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.responses
    ADD CONSTRAINT responses_pkey PRIMARY KEY (response_id);


--
-- Name: selected_option selected_option_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.selected_option
    ADD CONSTRAINT selected_option_pkey PRIMARY KEY (selected_option_id);


--
-- Name: surveys surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.surveys
    ADD CONSTRAINT surveys_pkey PRIMARY KEY (survey_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: image_responses image_responses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.image_responses
    ADD CONSTRAINT image_responses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: options options_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(question_id);


--
-- Name: question_logic question_logic_child_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.question_logic
    ADD CONSTRAINT question_logic_child_question_id_fkey FOREIGN KEY (child_question_id) REFERENCES public.questions(question_id);


--
-- Name: question_logic question_logic_parent_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.question_logic
    ADD CONSTRAINT question_logic_parent_question_id_fkey FOREIGN KEY (parent_question_id) REFERENCES public.questions(question_id);


--
-- Name: question_responses question_responses_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.question_responses
    ADD CONSTRAINT question_responses_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(question_id);


--
-- Name: question_responses question_responses_response_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.question_responses
    ADD CONSTRAINT question_responses_response_id_fkey FOREIGN KEY (response_id) REFERENCES public.responses(response_id);


--
-- Name: questions questions_input_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_input_type_id_fkey FOREIGN KEY (input_type_id) REFERENCES public.input_type(input_type_id);


--
-- Name: questions questions_survey_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_survey_id_fkey FOREIGN KEY (survey_id) REFERENCES public.surveys(survey_id);


--
-- Name: responses responses_survey_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.responses
    ADD CONSTRAINT responses_survey_id_fkey FOREIGN KEY (survey_id) REFERENCES public.surveys(survey_id);


--
-- Name: responses responses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.responses
    ADD CONSTRAINT responses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: selected_option selected_option_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.selected_option
    ADD CONSTRAINT selected_option_option_id_fkey FOREIGN KEY (option_id) REFERENCES public.options(option_id);


--
-- Name: selected_option selected_option_question_response_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: endo
--

ALTER TABLE ONLY public.selected_option
    ADD CONSTRAINT selected_option_question_response_id_fkey FOREIGN KEY (question_response_id) REFERENCES public.question_responses(question_response_id);


--
-- PostgreSQL database dump complete
--

