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

CREATE TABLE Users (
      User_id INT PRIMARY KEY,
      usename VARCHAR(255),
      password_hashed VARCHAR(255),
      last_login_time TIMESTAMP
    
);

CREATE TABLE Image_responses (
      Image_responses_id INT PRIMARY KEY,
      Time TIMESTAMP,
      Input_image BYTEA,
      Predict_image BYTEA,
      User_id INT,
      FOREIGN KEY (User_id) REFERENCES Users(User_id)
    
);

CREATE TABLE Responses (
      Response_id INT PRIMARY KEY,
      Time TIMESTAMP,
      Score INT,
      User_id INT,
      Survey_id INT,
      FOREIGN KEY (User_id) REFERENCES Users(User_id),
      FOREIGN KEY (Survey_id) REFERENCES Surveys(Survey_id) 
    
);

CREATE TABLE Question_responses (
      Question_response_id INT PRIMARY KEY,
      Answer TEXT,
      Response_id INT,
      Question_id INT,
      FOREIGN KEY (Response_id) REFERENCES Responses(Response_id),
      FOREIGN KEY (Question_id) REFERENCES Questions(Question_id) 
    
);

CREATE TABLE Selected_option (
      Selected_option_id INT PRIMARY KEY,
      Question_response_id INT,
      Option_id INT,
      FOREIGN KEY (Question_response_id) REFERENCES Question_responses(Question_response_id),
      FOREIGN KEY (Option_id) REFERENCES Options(Option_id) 
    
);


