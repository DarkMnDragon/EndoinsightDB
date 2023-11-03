

Surveys($\underline{Survey\_id}$, Title, Description, Date)

Questions($\underline{Question\_id}$, Index, Text,  **Input_type_id**, **Survey\_id**)

Input_type($\underline{Input\_type\_id}$, Name)

Options($\underline{Option\_id}$, option_text, **Question_id**)

Users($\underline{User\_id}$, usename, password_hashed, last_login_time)

Responses($\underline{Response\_id}$, Time, Input_image, Predict_image, Score, **User_id**, **Survey_id**)

Question_responses($\underline{Question\_response\_id}$, Answer, **Response_id**, **Question_id**)

Question_logic($\underline{Logic\_id}$, Parent_question_id, Parent_option_id, Child_question_id)

Selected_option($\underline{Selected\_option\_id}$,  **Question_response_id**, **Option_id**)

