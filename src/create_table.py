from . import connector

mycursor.execute(
"CREATE TABLE IF NOT EXISTS new_words
(
    english VARCHAR(255) PRIMARY KEY,
    vietnamese VARCHAR(255),
    type_word VARCHAR(10),
    sentent_example_english VARCHAR(255),
    sentent_example_vietnamese VARCHAR(255),
    pronounce VARCHAR(255),
    times_typ INT,
    date_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_last_study TIMESTAMP DEFAULT current_timestamp ON UPDATE CURRENT_TIMESTAMP
)")
