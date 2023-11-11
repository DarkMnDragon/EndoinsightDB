INSERT INTO Users (User_id, username, password_hashed, last_login_time) VALUES ('user123', 'example_user', 'hashed_password_example', '2023-11-03T10:00:00Z');

INSERT INTO Responses (Response_id, Time, Score, User_id, Survey_id) VALUES ('response1', '2023-11-03T10:00:00Z', 'None', 'user123', 1);

INSERT INTO Question_responses (Question_response_id, Answer, Response_id, Question_id) VALUES ('qr1', '', 'response1', 'q3'),
('qr2', '', 'response1', 'q4'),
('qr3', '', 'response1', 'q7'),
('qr4', '', 'response1', 'q8'),
('qr5', '', 'response1', 'q9'),
('qr6', '', 'response1', 'q10'),
('qr7', '', 'response1', 'q12'),
('qr8', '', 'response1', 'q13'),
('qr9', '', 'response1', 'q14'),
('qr10', '', 'response1', 'q15'),
('qr11', '', 'response1', 'q16'),
('qr12', '', 'response1', 'q17'),
('qr13', '', 'response1', 'q26'),
('qr14', '', 'response1', 'q37'),
('qr15', '', 'response1', 'q41'),
('qr16', '', 'response1', 'q51'),
('qr17', '', 'response1', 'q59'),
('qr18', '', 'response1', 'q66'),
('qr19', '', 'response1', 'q82'),
('qr20', '', 'response1', 'q88'),
('qr21', '', 'response1', 'q98'),
('qr22', '', 'response1', 'q110'),
('qr23', '', 'response1', 'q120'),
('qr24', '', 'response1', 'q122'),
('qr25', '', 'response1', 'q123'),
('qr26', '', 'response1', 'q127'),
('qr27', '', 'response1', 'q129'),
('qr28', '', 'response1', 'q130'),
('qr29', '', 'response1', 'q131'),
('qr30', '', 'response1', 'q132'),
('qr31', '', 'response1', 'q136'),
('qr32', '', 'response1', 'q140');

INSERT INTO Selected_options (Selected_option_id, Question_response_id, Option_id) VALUES ('soopt25', 'qr2', 'opt25'),
('soopt26', 'qr2', 'opt26'),
('soopt31', 'qr12', 'opt31'),
('soopt32', 'qr12', 'opt32'),
('soopt33', 'qr12', 'opt33'),
('soopt52', 'qr15', 'opt52'),
('soopt53', 'qr15', 'opt53'),
('soopt54', 'qr15', 'opt54'),
('soopt55', 'qr15', 'opt55'),
('soopt56', 'qr15', 'opt56'),
('soopt57', 'qr15', 'opt57'),
('soopt58', 'qr15', 'opt58'),
('soopt59', 'qr15', 'opt59'),
('soopt60', 'qr15', 'opt60'),
('soopt61', 'qr16', 'opt61'),
('soopt62', 'qr16', 'opt62'),
('soopt63', 'qr16', 'opt63'),
('soopt64', 'qr16', 'opt64'),
('soopt65', 'qr16', 'opt65'),
('soopt66', 'qr16', 'opt66'),
('soopt67', 'qr16', 'opt67'),
('soopt68', 'qr17', 'opt68'),
('soopt69', 'qr17', 'opt69'),
('soopt70', 'qr17', 'opt70'),
('soopt74', 'qr18', 'opt74'),
('soopt75', 'qr18', 'opt75'),
('soopt76', 'qr18', 'opt76'),
('soopt77', 'qr18', 'opt77'),
('soopt89', 'qr19', 'opt89'),
('soopt90', 'qr19', 'opt90'),
('soopt91', 'qr19', 'opt91'),
('soopt94', 'qr20', 'opt94'),
('soopt95', 'qr20', 'opt95'),
('soopt96', 'qr20', 'opt96'),
('soopt97', 'qr20', 'opt97'),
('soopt98', 'qr20', 'opt98'),
('soopt99', 'qr20', 'opt99'),
('soopt100', 'qr20', 'opt100'),
('soopt101', 'qr20', 'opt101'),
('soopt102', 'qr20', 'opt102'),
('soopt103', 'qr21', 'opt103'),
('soopt104', 'qr21', 'opt104'),
('soopt105', 'qr21', 'opt105'),
('soopt106', 'qr21', 'opt106'),
('soopt107', 'qr21', 'opt107'),
('soopt108', 'qr21', 'opt108'),
('soopt109', 'qr21', 'opt109'),
('soopt110', 'qr21', 'opt110'),
('soopt111', 'qr21', 'opt111'),
('soopt112', 'qr21', 'opt112'),
('soopt113', 'qr21', 'opt113'),
('soopt114', 'qr22', 'opt114'),
('soopt115', 'qr22', 'opt115'),
('soopt116', 'qr22', 'opt116'),
('soopt117', 'qr22', 'opt117'),
('soopt118', 'qr22', 'opt118'),
('soopt119', 'qr22', 'opt119'),
('soopt120', 'qr22', 'opt120'),
('soopt121', 'qr22', 'opt121'),
('soopt122', 'qr22', 'opt122'),
('soopt123', 'qr23', 'opt123'),
('soopt124', 'qr23', 'opt124'),
('soopt125', 'qr23', 'opt125'),
('soopt129', 'qr26', 'opt129'),
('soopt130', 'qr26', 'opt130'),
('soopt131', 'qr26', 'opt131');