create database if not exists hacknao1500;
use hacknao1500;
CREATE TABLE IF NOT EXISTs 	units(
	unit_code VARCHAR(255) PRIMARY KEY NOT NULL,
	unit_topic VARCHAR(255) NOT NULL,
	date_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	date_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS new_words
(
	`order` INT,
    english VARCHAR(255) PRIMARY KEY ,
    vietnamese VARCHAR(255) NOT NULL,
    type_word VARCHAR(10) NOT NULL,
    sentent_example_english VARCHAR(255),
    sentent_example_vietnamese VARCHAR(255),
    unit_code VARCHAR(255) NOT NULL,
    pronounce VARCHAR(255),
    right_times INT default 0,
    wrong_times INT default 0,
    date_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_last_study TIMESTAMP DEFAULT current_timestamp ON UPDATE CURRENT_TIMESTAMP
);


ALTER TABLE new_words drop primary key, add primary key (english,unit_code);
alter table new_words
ADD FOREIGN KEY (unit_code) REFERENCES units(unit_code);


create table paragraph(
	id int primary key auto_increment,
	topic varchar(255)
);

create table sentences_paragraph(
	id int primary key auto_increment,
	english varchar(255),
    vietnamese varchar(255),
    paragraph_id int references paragraph(`id`) on delete cascade,
    sentence_order int,
    constraint `unique_paragraph_id_order` unique(paragraph_id,sentence_order)
);

create table words_paragraph(
	id int primary key auto_increment,
    english varchar(255),
    vietnamese varchar(255),
    number_of int default 1,
    paragraph_id int references paragraph(`id`) on delete cascade
);
