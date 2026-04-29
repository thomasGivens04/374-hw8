"""Create fake data for the the hotel DB."""

import random
from faker import Faker
from pprint import pprint

fake = Faker()


def make_hotels():
    hotels = []
    for hotel_id in range(1, 21):
        h = []
        h.append(hotel_id)
        h.append(fake.color_name() + " Hotel")
        h.append(fake.street_address())
        h.append(fake.city())
        h.append(fake.country())
        h.append(random.randint(1900, 2024))
        hotels.append(h)
    return hotels


def make_hotel_phones(hotels):
    hotel_phones = []
    for h in hotels:
        # a hotel has between 1 and 4 phone numbers
        phones = random.randint(1, 4)
        # phones+1 because the end of the range is not inclusive
        for sort in range(1, phones + 1):
            hp = []
            hp.append(h[0])  # hotel_id
            hp.append(sort)
            hp.append(fake.phone_number())
            # make a random choice from a list
            hp.append(random.choice(["", "Front Desk", "Reservations", "Security"]))
            hotel_phones.append(hp)
    return hotel_phones


if __name__ == "__main__":
    hotels = make_hotels()
    hotel_phones = make_hotel_phones(hotels)
    pprint(hotels, width=100)
    pprint(hotel_phones)
