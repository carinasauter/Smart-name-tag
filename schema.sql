drop table if exists users;

CREATE TABLE users (
    user_id integer PRIMARY KEY,
    username text not null,
    email text not null,
    password_hash text not null,
    full_name text
    title text,
    company text,
    linked_in text,
    resume text, 
    interests text
);

drop table if exists contacts;
CREATE TABLE contacts (
    contact_id integer PRIMARY KEY,
    user1 integer not null, 
    user2 integer not null
)
