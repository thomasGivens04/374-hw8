import psycopg
import socket
from faker import Faker
import random
from datetime import date, timedelta

CONNSTR = "host=data.cs.jmu.edu port=5432 dbname=sp26 user=givensta password=114027764"

fake = Faker()
random.seed(42)
Faker.seed(42)

def create_tables():
    with psycopg.connect(CONNSTR) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS service_charge CASCADE;")
            cur.execute("DROP TABLE IF EXISTS service_type CASCADE;")
            cur.execute("DROP TABLE IF EXISTS billing CASCADE;")
            cur.execute("DROP TABLE IF EXISTS stay_room CASCADE;")
            cur.execute("DROP TABLE IF EXISTS occupant CASCADE;")
            cur.execute("DROP TABLE IF EXISTS stay CASCADE;")
            cur.execute("DROP TABLE IF EXISTS reservation_room_type CASCADE;")
            cur.execute("DROP TABLE IF EXISTS reservation CASCADE;")
            cur.execute("DROP TABLE IF EXISTS guest CASCADE;")
            cur.execute("DROP TABLE IF EXISTS pricing CASCADE;")
            cur.execute("DROP TABLE IF EXISTS room CASCADE;")
            cur.execute("DROP TABLE IF EXISTS room_type CASCADE;")
            cur.execute("DROP TABLE IF EXISTS season CASCADE;")
            cur.execute("DROP TABLE IF EXISTS guest_category CASCADE;")
            cur.execute("DROP TABLE IF EXISTS hotel_phone CASCADE;")
            cur.execute("DROP TABLE IF EXISTS hotel CASCADE;")
            cur.execute("""
                CREATE TABLE hotel (
                    hotel_id integer NOT NULL PRIMARY KEY,
                    name text NOT NULL,
                    street text NOT NULL,
                    city text NOT NULL,
                    country text NOT NULL,
                    year integer NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE hotel_phone (
                    hotel_id integer NOT NULL,
                    sort integer NOT NULL,
                    phone text NOT NULL,
                    label text,
                    PRIMARY KEY (hotel_id, sort),
	                FOREIGN KEY (hotel_id) REFERENCES hotel
                );
            """)
            cur.execute("""
                CREATE TABLE guest_category (
                    category_id integer PRIMARY KEY,
                    name text NOT NULL UNIQUE,
                    discount_percent numeric(5,2) NOT NULL CHECK (discount_percent >= 0)
                );
            """)
            cur.execute("""
                CREATE TABLE season (
                    season_id integer PRIMARY KEY,
                    hotel_id integer NOT NULL REFERENCES hotel(hotel_id),
                    name text NOT NULL,
                    start_date date NOT NULL,
                    end_date date NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE room_type (
                    room_type_id integer PRIMARY KEY,
                    hotel_id integer NOT NULL REFERENCES hotel(hotel_id),
                    name text NOT NULL,
                    size_sqm integer NOT NULL,
                    capacity integer NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE room (
                    room_id integer PRIMARY KEY,
                    hotel_id integer NOT NULL REFERENCES hotel(hotel_id),
                    room_type_id integer NOT NULL REFERENCES room_type(room_type_id),
                    room_number text NOT NULL,
                    floor integer NOT NULL,
                    UNIQUE (hotel_id, room_number)
                );
            """)
            cur.execute("""
                CREATE TABLE pricing (
                    pricing_id integer PRIMARY KEY,
                    room_type_id integer NOT NULL REFERENCES room_type(room_type_id),
                    season_id integer NOT NULL REFERENCES season(season_id),
                    day_of_week text NOT NULL,
                    price numeric(10,2) NOT NULL,
                    UNIQUE (room_type_id, season_id, day_of_week)
                );
            """)
            cur.execute("""
                CREATE TABLE guest (
                    guest_id integer PRIMARY KEY,
                    first_name text NOT NULL,
                    last_name text NOT NULL,
                    identification_type text NOT NULL,
                    identification_number text NOT NULL,
                    street text NOT NULL,
                    city text NOT NULL,
                    country text NOT NULL,
                    home_phone text,
                    mobile_phone text,
                    category_id integer REFERENCES guest_category(category_id)
                );
            """)
            cur.execute("""
                CREATE TABLE reservation (
                    reservation_id integer PRIMARY KEY,
                    guest_id integer NOT NULL REFERENCES guest(guest_id),
                    hotel_id integer NOT NULL REFERENCES hotel(hotel_id),
                    check_in_date date NOT NULL,
                    check_out_date date NOT NULL,
                    created_on date NOT NULL,
                    CHECK (check_out_date > check_in_date)
                );
            """)
            cur.execute("""
                CREATE TABLE reservation_room_type (
                    reservation_id integer NOT NULL REFERENCES reservation(reservation_id),
                    room_type_id integer NOT NULL REFERENCES room_type(room_type_id),
                    quantity integer NOT NULL CHECK (quantity > 0),
                    PRIMARY KEY (reservation_id, room_type_id)
                );
            """)
            cur.execute("""
                CREATE TABLE stay (
                    stay_id integer PRIMARY KEY,
                    reservation_id integer NOT NULL UNIQUE REFERENCES reservation(reservation_id),
                    start_date date NOT NULL,
                    end_date date NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE occupant (
                    occupant_id integer PRIMARY KEY,
                    stay_id integer NOT NULL REFERENCES stay(stay_id),
                    full_name text NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE stay_room (
                    stay_id integer NOT NULL REFERENCES stay(stay_id),
                    room_id integer NOT NULL REFERENCES room(room_id),
                    PRIMARY KEY (stay_id, room_id)
                );
            """)
            cur.execute("""
                CREATE TABLE billing (
                    bill_id integer PRIMARY KEY,
                    stay_id integer NOT NULL UNIQUE REFERENCES stay(stay_id),
                    total_amount numeric(10,2) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE service_type (
                    service_type_id integer PRIMARY KEY,
                    name text NOT NULL UNIQUE,
                    base_price numeric(10,2) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE service_charge (
                    service_charge_id integer PRIMARY KEY,
                    bill_id integer NOT NULL REFERENCES billing(bill_id),
                    service_type_id integer NOT NULL REFERENCES service_type(service_type_id),
                    charge_date date NOT NULL,
                    quantity integer NOT NULL CHECK (quantity > 0),
                    amount numeric(10,2) NOT NULL
                );
            """)
        conn.commit()


def make_hotels():
    hotels = []
    for hotel_id in range(1, 6):
        hotels.append((
            hotel_id,
            fake.company() + " Hotel",
            fake.street_address(),
            fake.city(),
            fake.country(),
            random.randint(1900, 2023)
        ))
    return hotels


def make_hotel_phones(hotels):
    rows = []
    for hotel in hotels:
        hotel_id = hotel[0]
        phone_count = random.randint(1, 3)
        for sort in range(1, phone_count + 1):
            rows.append((
                hotel_id,
                sort,
                fake.phone_number(),
                random.choice(["Front Desk", "Reservations", "Security"])
            ))
    return rows


def make_guest_categories():
    return [
        (1, "VIP", 15.00),
        (2, "Government", 10.00)
    ]


def make_seasons(hotels):
    rows = []
    season_id = 1
    for hotel in hotels:
        hotel_id = hotel[0]
        rows.append((season_id, hotel_id, "Regular Season", date(2026, 2, 1), date(2026, 5, 31)))
        season_id += 1
        rows.append((season_id, hotel_id, "Festival Season", date(2026, 6, 1), date(2026, 8, 31)))
        season_id += 1
    return rows


def make_room_types(hotels):
    rows = []
    room_type_id = 1
    templates = [
        ("Single", 20, 1),
        ("Double", 30, 4),
        ("Suite", 45, 5),
    ]
    for hotel in hotels:
        hotel_id = hotel[0]
        for name, size, capacity in templates[:2]:
            rows.append((room_type_id, hotel_id, name, size, capacity))
            room_type_id += 1
    return rows


def make_rooms(room_types):
    rows = []
    room_id = 1
    for room_type in room_types:
        room_type_id, hotel_id, name, _, _ = room_type
        for i in range(1, 4):
            floor = random.randint(1, 8)
            room_number = f"{floor}{i:02d}"
            rows.append((room_id, hotel_id, room_type_id, room_number, floor))
            room_id += 1
    return rows


def make_pricing(room_types, seasons):
    rows = []
    pricing_id = 1
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    season_by_hotel = {}
    for season in seasons:
        season_id, hotel_id, season_name, _, _ = season
        season_by_hotel.setdefault(hotel_id, []).append((season_id, season_name))

    for rt in room_types:
        room_type_id, hotel_id, name, _, _ = rt
        base = {
            "Single": 90,
            "Double": 140,
            "Suite": 220
        }.get(name, 120)

        for season_id, season_name in season_by_hotel[hotel_id]:
            seasonal_bump = 40 if "Festival" in season_name else 0
            for day in days:
                weekend_bump = 25 if day in ("Fri", "Sat", "Sun") else 0
                variation = random.randint(0, 15)
                price = base + seasonal_bump + weekend_bump + variation
                rows.append((pricing_id, room_type_id, season_id, day, price))
                pricing_id += 1
    return rows


def make_guests():
    rows = []
    for guest_id in range(1, 11):
        first = fake.first_name()
        last = fake.last_name()
        rows.append((
            guest_id,
            first,
            last,
            random.choice(["Passport", "Driver License"]),
            fake.bothify(text="??########"),
            fake.street_address(),
            fake.city(),
            fake.country(),
            fake.phone_number(),
            fake.phone_number(),
            random.choice([1, 2, None])
        ))
    return rows


def make_reservations(guests, hotels):
    rows = []
    reservation_id = 1

    hotel_ids = [h[0] for h in hotels]

    # one reservation for each guest
    for guest in guests:
        guest_id = guest[0]
        hotel_id = random.choice(hotel_ids)
        check_in = date(2026, random.randint(2, 8), random.randint(1, 20))
        nights = random.choice([1, 2, 3, 4])
        check_out = check_in + timedelta(days=nights)
        created_on = check_in - timedelta(days=random.randint(5, 60))
        rows.append((reservation_id, guest_id, hotel_id, check_in, check_out, created_on))
        reservation_id += 1

    # extra reservations for 2 guests
    for guest_id in [1, 2]:
        hotel_id = random.choice(hotel_ids)
        check_in = date(2026, random.randint(6, 8), random.randint(1, 20))
        nights = random.choice([2, 3])
        check_out = check_in + timedelta(days=nights)
        created_on = check_in - timedelta(days=random.randint(5, 40))
        rows.append((reservation_id, guest_id, hotel_id, check_in, check_out, created_on))
        reservation_id += 1

    return rows


def make_reservation_room_types(reservations, room_types):
    rows = []
    room_types_by_hotel = {}
    for rt in room_types:
        room_type_id, hotel_id, name, _, _ = rt
        room_types_by_hotel.setdefault(hotel_id, []).append(room_type_id)

    for i, res in enumerate(reservations, start=1):
        reservation_id, _, hotel_id, check_in, check_out, _ = res
        available = room_types_by_hotel[hotel_id]

        # first 2 reservations: multiple room types
        if i in [1, 2]:
            chosen = random.sample(available, 2)
            rows.append((reservation_id, chosen[0], 1))
            rows.append((reservation_id, chosen[1], 1))

        # next 2 reservations: multiple rooms of same type
        elif i in [3, 4]:
            chosen = random.choice(available)
            rows.append((reservation_id, chosen, 2))

        else:
            chosen = random.choice(available)
            quantity = random.choice([1, 1, 1, 2])
            rows.append((reservation_id, chosen, quantity))

    return rows


def make_stays(reservations):
    rows = []
    stay_id = 1
    for res in reservations[:3]:
        reservation_id, _, _, check_in, check_out, _ = res
        rows.append((stay_id, reservation_id, check_in, check_out))
        stay_id += 1
    return rows


def make_occupants(stays, reservations, guests):
    guest_lookup = {g[0]: f"{g[1]} {g[2]}" for g in guests}
    res_lookup = {r[0]: r for r in reservations}

    rows = []
    occupant_id = 1
    for stay in stays:
        stay_id, reservation_id, _, _ = stay
        res = res_lookup[reservation_id]
        guest_id = res[1]

        # payer is always an occupant in this sample
        rows.append((occupant_id, stay_id, guest_lookup[guest_id]))
        occupant_id += 1

        # plus 0-3 accompanying people
        extras = random.randint(0, 3)
        for _ in range(extras):
            rows.append((occupant_id, stay_id, fake.name()))
            occupant_id += 1
    return rows


def make_stay_rooms(stays, reservation_room_types, rooms):
    rows = []

    rooms_by_type = {}
    for room in rooms:
        room_id, hotel_id, room_type_id, room_number, floor = room
        rooms_by_type.setdefault(room_type_id, []).append(room_id)

    res_rt_lookup = {}
    for reservation_id, room_type_id, quantity in reservation_room_types:
        res_rt_lookup.setdefault(reservation_id, []).append((room_type_id, quantity))

    for stay in stays:
        stay_id, reservation_id, _, _ = stay
        needed = res_rt_lookup[reservation_id]

        for room_type_id, quantity in needed:
            available = rooms_by_type[room_type_id][:quantity]
            for room_id in available:
                rows.append((stay_id, room_id))

    return rows


def make_billing(stays, reservation_room_types, reservations, room_types, seasons, pricing):
    rows = []
    bill_id = 1

    # quick lookup
    pricing_lookup = {}
    for pricing_id, room_type_id, season_id, day_of_week, price in pricing:
        pricing_lookup[(room_type_id, season_id, day_of_week)] = float(price)

    season_lookup = {}
    for season_id, hotel_id, name, start_date, end_date in seasons:
        season_lookup.setdefault(hotel_id, []).append((season_id, start_date, end_date))

    res_lookup = {r[0]: r for r in reservations}
    res_rt_lookup = {}
    for reservation_id, room_type_id, quantity in reservation_room_types:
        res_rt_lookup.setdefault(reservation_id, []).append((room_type_id, quantity))

    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for stay_id, reservation_id, start_date, end_date in stays:
        _, guest_id, hotel_id, _, _, _ = res_lookup[reservation_id]
        total = 0.0

        current = start_date
        while current < end_date:
            day_name = weekday_names[current.weekday()]
            season_id = None
            for sid, s_start, s_end in season_lookup[hotel_id]:
                if s_start <= current <= s_end:
                    season_id = sid
                    break

            for room_type_id, quantity in res_rt_lookup[reservation_id]:
                total += pricing_lookup[(room_type_id, season_id, day_name)] * quantity

            current += timedelta(days=1)

        rows.append((bill_id, stay_id, round(total, 2)))
        bill_id += 1

    return rows


def make_service_types():
    return [
        (1, "Breakfast", 18.00),
        (2, "Spa Visit", 65.00),
        (3, "Room Service Meal", 32.00),
    ]


def make_service_charges(billing_rows, service_types):
    rows = []
    service_charge_id = 1
    for bill_id, stay_id, total_amount in billing_rows:
        how_many = random.randint(1, 3)
        for _ in range(how_many):
            service_type = random.choice(service_types)
            service_type_id = service_type[0]
            base_price = float(service_type[2])
            quantity = random.randint(1, 2)
            amount = round(base_price * quantity, 2)
            rows.append((
                service_charge_id,
                bill_id,
                service_type_id,
                fake.date_between(start_date="-60d", end_date="today"),
                quantity,
                amount
            ))
            service_charge_id += 1
    return rows


def insert_many(sql, rows):
    with psycopg.connect(CONNSTR) as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
        conn.commit()


if __name__ == "__main__":
    create_tables()

    hotels = make_hotels()
    hotel_phones = make_hotel_phones(hotels)
    categories = make_guest_categories()
    seasons = make_seasons(hotels)
    room_types = make_room_types(hotels)
    rooms = make_rooms(room_types)
    pricing = make_pricing(room_types, seasons)
    guests = make_guests()
    reservations = make_reservations(guests, hotels)
    reservation_room_types = make_reservation_room_types(reservations, room_types)
    stays = make_stays(reservations)
    occupants = make_occupants(stays, reservations, guests)
    stay_rooms = make_stay_rooms(stays, reservation_room_types, rooms)
    billing = make_billing(stays, reservation_room_types, reservations, room_types, seasons, pricing)
    service_types = make_service_types()
    service_charges = make_service_charges(billing, service_types)

    insert_many("INSERT INTO hotel VALUES (%s, %s, %s, %s, %s, %s)", hotels)
    insert_many("INSERT INTO hotel_phone VALUES (%s, %s, %s, %s)", hotel_phones)
    insert_many("INSERT INTO guest_category VALUES (%s, %s, %s)", categories)
    insert_many("INSERT INTO season VALUES (%s, %s, %s, %s, %s)", seasons)
    insert_many("INSERT INTO room_type VALUES (%s, %s, %s, %s, %s)", room_types)
    insert_many("INSERT INTO room VALUES (%s, %s, %s, %s, %s)", rooms)
    insert_many("INSERT INTO pricing VALUES (%s, %s, %s, %s, %s)", pricing)
    insert_many("INSERT INTO guest VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", guests)
    insert_many("INSERT INTO reservation VALUES (%s, %s, %s, %s, %s, %s)", reservations)
    insert_many("INSERT INTO reservation_room_type VALUES (%s, %s, %s)", reservation_room_types)
    insert_many("INSERT INTO stay VALUES (%s, %s, %s, %s)", stays)
    insert_many("INSERT INTO occupant VALUES (%s, %s, %s)", occupants)
    insert_many("INSERT INTO stay_room VALUES (%s, %s)", stay_rooms)
    insert_many("INSERT INTO billing VALUES (%s, %s, %s)", billing)
    insert_many("INSERT INTO service_type VALUES (%s, %s, %s)", service_types)
    insert_many("INSERT INTO service_charge VALUES (%s, %s, %s, %s, %s, %s)", service_charges)

    print("Database created and loaded.")

