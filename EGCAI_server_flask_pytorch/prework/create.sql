CREATE TABLE surveys (
      survey_id INT PRIMARY KEY,
      title VARCHAR(255),
      description TEXT,
      date DATE,
      first_question_id INT,
      last_question_id INT

);

CREATE TABLE input_type (
      type_id INT PRIMARY KEY,
      name VARCHAR(50)
    
);

CREATE TABLE questions (
      question_id INT PRIMARY KEY,
      question_text VARCHAR(255),
      type_id INT,
      survey_id INT,
      FOREIGN KEY (type_id) REFERENCES input_type(type_id),
      FOREIGN KEY (survey_id) REFERENCES surveys(survey_id)
    
);

CREATE TABLE options (
      option_id INT PRIMARY KEY,
      option_text VARCHAR(255),
      question_id INT,
      FOREIGN KEY (question_id) REFERENCES questions(question_id)
    
);

CREATE TABLE question_logic (
      logic_id INT PRIMARY KEY,
      parent_question_id INT,
      parent_option_id INT,
      child_question_id INT,
      FOREIGN KEY (parent_question_id) REFERENCES questions(question_id),
      FOREIGN KEY (child_question_id) REFERENCES questions(question_id)
    
);


CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    sex VARCHAR(10),
    nation VARCHAR(50),
    ID_number VARCHAR(18),
    birthday DATE,
    phone_number VARCHAR(20),
    family_member_phone_number VARCHAR(20),
    height INT,
    weight INT,
    homeplace VARCHAR(100)
);

CREATE TABLE image_responses (
      image_responses_id INT PRIMARY KEY,
      time TIMESTAMP,
      input_image BYTEA,
      predict_image BYTEA,
      user_id VARCHAR(255),
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    
);

CREATE TABLE responses (
      response_id VARCHAR(255) PRIMARY KEY,
      time TIMESTAMP,
      user_id VARCHAR(255),
      survey_id INT,
      current_question_id INT,
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      FOREIGN KEY (survey_id) REFERENCES surveys(survey_id) 
    
);

CREATE TABLE question_responses (
      question_response_id VARCHAR(255) PRIMARY KEY,
      answer TEXT,
      response_id VARCHAR(255),
      question_id INT,
      FOREIGN KEY (response_id) REFERENCES responses(response_id),
      FOREIGN KEY (question_id) REFERENCES questions(question_id) 
    
);

CREATE TABLE selected_option (
      selected_option_id VARCHAR(255) PRIMARY KEY,
      question_response_id VARCHAR(255),
      option_id INT,
      FOREIGN KEY (question_response_id) REFERENCES question_responses(question_response_id),
      FOREIGN KEY (option_id) REFERENCES options(option_id) 
    
);

CREATE TABLE lists (
      list_id VARCHAR(255) PRIMARY KEY,
      parent_question_id INT,
      child_question_id INT,
      response_id VARCHAR(255),
      FOREIGN KEY (parent_question_id) REFERENCES questions(question_id),
      FOREIGN KEY (child_question_id) REFERENCES questions(question_id),
      FOREIGN KEY (response_id) REFERENCES responses(response_id)
);
	

