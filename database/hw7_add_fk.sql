ALTER TABLE guest
ADD CONSTRAINT guest_category_fk
FOREIGN KEY (category)
REFERENCES cat_discount(type);

ALTER TABLE occupant
ADD CONSTRAINT occupant_guest_fk
FOREIGN KEY (guest_id)
REFERENCES guest(id);

ALTER TABLE occupant
ADD CONSTRAINT occupant_stay_fk
FOREIGN KEY (stay_id)
REFERENCES stay(id);

ALTER TABLE billing
ADD CONSTRAINT billing_stay_fk
FOREIGN KEY (stay_id)
REFERENCES stay(id);

ALTER TABLE reservation
ADD CONSTRAINT reservation_hotel_fk
FOREIGN KEY (hotel_id)
REFERENCES hotel(id);

ALTER TABLE reservation
ADD CONSTRAINT reservation_stay_fk
FOREIGN KEY (stay_id)
REFERENCES stay(id);

ALTER TABLE reservation
ADD CONSTRAINT reservation_guest_fk
FOREIGN KEY (guest_id)
REFERENCES guest(id);

ALTER TABLE room
ADD CONSTRAINT room_hotel_fk
FOREIGN KEY (hotel_id)
REFERENCES hotel(id);

ALTER TABLE room
ADD CONSTRAINT room_room_type_fk
FOREIGN KEY (hotel_id, room_type)
REFERENCES room_type(hotel_id, type);

ALTER TABLE season
ADD CONSTRAINT season_hotel_fk
FOREIGN KEY (hotel_id)
REFERENCES hotel(id);

ALTER TABLE pricing
ADD CONSTRAINT pricing_season_fk
FOREIGN KEY (hotel_id, season)
REFERENCES season(hotel_id, name);

ALTER TABLE room_service
ADD CONSTRAINT room_service_bill_fk
FOREIGN KEY (bill_id)
REFERENCES billing(id);

ALTER TABLE stay
ADD CONSTRAINT stay_hotel_fk
FOREIGN KEY (hotel_id)
REFERENCES hotel(id);

ALTER TABLE stay
ADD CONSTRAINT stay_room_fk
FOREIGN KEY (room_num, hotel_id)
REFERENCES room(room_num, hotel_id);

ALTER TABLE phone_number
ADD CONSTRAINT phone_number_hotel_fk
FOREIGN KEY (hotel_id)
REFERENCES hotel(id);