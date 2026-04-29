DROP TABLE IF EXISTS room_service CASCADE;
DROP TABLE IF EXISTS phone_number CASCADE;
DROP TABLE IF EXISTS billing CASCADE;
DROP TABLE IF EXISTS reservation CASCADE;
DROP TABLE IF EXISTS occupant CASCADE;
DROP TABLE IF EXISTS stay CASCADE;
DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS pricing CASCADE;
DROP TABLE IF EXISTS season CASCADE;
DROP TABLE IF EXISTS room_type CASCADE;
DROP TABLE IF EXISTS cat_discount CASCADE;
DROP TABLE IF EXISTS guest CASCADE;
DROP TABLE IF EXISTS hotel CASCADE;

CREATE TABLE hotel (
    id int PRIMARY KEY,
    name text,
    address text,
    phone_number varchar,
    features varchar
);

CREATE TABLE guest (
    id int PRIMARY KEY,
    id_type text,
    address text,
    home_phone text,
    mobile_phone text,
    category varchar
);

CREATE TABLE cat_discount (
    type varchar PRIMARY KEY,
    percentage text
);

CREATE TABLE room_type (
    hotel_id int,
    type varchar,
    size int,
    capacity int,
    room_features varchar,
    price int,
    PRIMARY KEY (hotel_id, type)
);

CREATE TABLE room (
    room_num int,
    hotel_id int,
    floor_num int,
    room_type varchar,
    PRIMARY KEY (room_num, hotel_id)
);

CREATE TABLE season (
    hotel_id int,
    name varchar,
    start_date date,
    end_date date,
    PRIMARY KEY (hotel_id, name)
);

CREATE TABLE pricing (
    hotel_id int,
    season varchar,
    day_of_week varchar,
    cost int,
    PRIMARY KEY (hotel_id, season, day_of_week)
);

CREATE TABLE reservation (
    id int PRIMARY KEY,
    hotel_id int,
    stay_id int,
    guest_id int,
    start_date date,
    end_date date,
    num_rooms int,
    room_type varchar
);

CREATE TABLE stay (
    id int PRIMARY KEY,
    hotel_id int,
    start_date date,
    end_date date,
    room_num int
);

CREATE TABLE occupant (
    guest_id int,
    stay_id int,
    name text,
    PRIMARY KEY (guest_id, stay_id, name)
);

CREATE TABLE billing (
    id int PRIMARY KEY,
    stay_id int,
    total int
);

CREATE TABLE room_service (
    bill_id int,
    cost int,
    PRIMARY KEY (bill_id, cost)
);

CREATE TABLE phone_number (
    hotel_id int,
    type text,
    number text,
    PRIMARY KEY (hotel_id, number)
);