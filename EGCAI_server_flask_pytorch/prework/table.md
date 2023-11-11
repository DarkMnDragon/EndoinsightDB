

Surveys($\underline{Survey\_id}$, Title, Description, Date)

Input_type($\underline{Input\_type\_id}$, Name)

Questions($\underline{Question\_id}$, Text,  **Input_type_id**, **Survey\_id**)

Options($\underline{Option\_id}$, option_text, **Question_id**)

Question_logic($\underline{Logic\_id}$, Parent_question_id, Parent_option_id, Child_question_id)

Users($\underline{User\_id}$, usename, password_hashed, last_login_time)

Image_responses($\underline{Image\_responses\_id}$, Time, Input_image, Predict_image, **User_id**)

Responses($\underline{Response\_id}$, Time,  Score, **User_id**, **Survey_id**)

Question_responses($\underline{Question\_response\_id}$, Answer, **Response_id**, **Question_id**)

Selected_option($\underline{Selected\_option\_id}$,  **Question_response_id**, **Option_id**)

