create database pycard;

CREATE TABLE pycard.users (
	id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE pycard.flashcards (
    flashcard_id varchar(255) NOT NULL,
    flashcard_name varchar(255),
    completed_decks int,
    score int,
    heart_count int,
    start_time varchar(255),
    remaining_time varchar(255),
    total_decks int,
    user_id int,
    PRIMARY KEY (flashcard_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE pycard.cards (
    card_id int NOT NULL AUTO_INCREMENT,
    card_name varchar(255),
    card_description varchar(255),
    card_answer varchar(255),
    flashcard_id varchar(255),
    PRIMARY KEY (card_id),
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(flashcard_id)
);

insert into pycard.users(username,password) values('admin','admin')

SHOW DATABASES
DROP DATABASE pycard

select * from pycard.users
select * from pycard.flashcards
select * from pycard.cards