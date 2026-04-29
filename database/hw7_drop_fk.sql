ALTER TABLE occupant DROP CONSTRAINT IF EXISTS occupant_guest_fk;
ALTER TABLE occupant DROP CONSTRAINT IF EXISTS occupant_stay_fk;

ALTER TABLE billing DROP CONSTRAINT IF EXISTS billing_stay_fk;

ALTER TABLE reservation DROP CONSTRAINT IF EXISTS reservation_hotel_fk;
ALTER TABLE reservation DROP CONSTRAINT IF EXISTS reservation_stay_fk;
ALTER TABLE reservation DROP CONSTRAINT IF EXISTS reservation_guest_fk;
ALTER TABLE reservation DROP CONSTRAINT IF EXISTS reservation_room_type_fk;

ALTER TABLE guest DROP CONSTRAINT IF EXISTS guest_category_fk;

ALTER TABLE room_type DROP CONSTRAINT IF EXISTS room_type_hotel_fk;

ALTER TABLE room DROP CONSTRAINT IF EXISTS room_hotel_fk;
ALTER TABLE room DROP CONSTRAINT IF EXISTS room_room_type_fk;

ALTER TABLE season DROP CONSTRAINT IF EXISTS season_hotel_fk;

ALTER TABLE room_service DROP CONSTRAINT IF EXISTS room_service_bill_fk;

ALTER TABLE stay DROP CONSTRAINT IF EXISTS stay_hotel_fk;
ALTER TABLE stay DROP CONSTRAINT IF EXISTS stay_room_fk;

ALTER TABLE phone_number DROP CONSTRAINT IF EXISTS phone_number_hotel_fk;

ALTER TABLE pricing DROP CONSTRAINT IF EXISTS pricing_season_fk;